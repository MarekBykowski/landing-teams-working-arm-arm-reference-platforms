#!/usr/bin/env python3

"""
 " Copyright (c) 2019, Arm Limited. All rights reserved.
 " Author: Ash Wilding <ash.wilding@arm.com>
 "
 " SPDX-License-Identifier: BSD-3-Clause
 "
 " Redistribution and use in source and binary forms, with or without
 " modification, are permitted provided that the following conditions are met:
 "
 " * Redistributions of source code must retain the above copyright notice, this
 "   list of conditions and the following disclaimer.
 "
 " * Redistributions in binary form must reproduce the above copyright notice,
 "   this list of conditions and the following disclaimer in the documentation
 "   and/or other materials provided with the distribution.
 "
 " * Neither the name of the copyright holder nor the names of its
 "   contributors may be used to endorse or promote products derived from
 "   this software without specific prior written permission.
 "
 " THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 " AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 " IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 " ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
 " LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 " CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
 " SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
 " INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
 " CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 " ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 " POSSIBILITY OF SUCH DAMAGE.
"""

"""
 " If running on Python < 3.5, we'll hit syntax errors further down the script
 " before getting a chance to programmatically query version_info from sys.
 "
 " By deliberately invoking the syntax error here, we can at least print a
 " helpful message to the user.
"""
x=["foo", "bar"]
vsn_check = "{}{}".format(*x, "if you can see this, you need Python 3.5+")

import argparse
import bz2
import collections, ctypes
import gzip
import hashlib
import logging
import math
import os
import platform
import re
import shutil, subprocess, sys
import tarfile, threading, time
import urllib.error, urllib.request
import zipfile

HOST = platform.system()
assert HOST in ["Windows", "Linux"], "script requires Windows or Linux"
if HOST=="Windows":
    import ctypes


###
 # Database structure describing each available software stack configuration.
 #
 # Keys defined by a node are inherited by that node's children, unless the
 # child overrides it by defining the same key. Keys inherited by a node are
 # also inherited by that node's children using the same mechanism.
 #
 # Example:
 #
 #      "people": {
 #          "surname": "Smith",
 #          "john": {
 #              "name": "John",
 #          },
 #          "jane": {
 #              "name": "Jane",
 #          },
 #          "alexa": {
 #              "name": "Alexa",
 #              "surname": "Smith-Doe",
 #          },
 #      },
 #
 #      Lookup "people.john.surname"  --> "Smith"
 #      Lookup "people.jane.surname"  --> "Smith"
 #      Lookup "people.alexa.surname" --> "Smith-Doe"
 #
 # Keys can cross-reference other keys in the database by "{wrapping}" in curly
 # braces. A single key may comprise multiple cross-references.
 #
 # Example:
 #
 #      "arm": {
 #          "release": "18.10",
 #          "url": "https://example.com/",
 #          "title": "Arm Platforms Software {release}",
 #      }
 #      "something": {
 #          "url": "{arm.url}/path/to/{arm.release}/123.zip",
 #      }
 #
 #      Lookup "arm.title" --> "Arm Platforms Software 18.10"
 #      Lookup "something.url" --> "https://example.com/path/to/18.10/123.zip"
 #
 # Keys can comprise both forward-references and backward-references.
 #
 # Example:
 #
 #      "thing": {
 #          "url": "https://example.com",
 #          "name0": "AAA",
 #          "name: "{name0}-{name1}.zip",
 #
 #          "variant1": {
 #              "name1": "111",
 #          }
 #
 #          "variant2": {
 #              "name1": "222",
 #          }
 #
 #          "variant3": {
 #              "name0": "BBB",
 #              "name1": "333",
 #          }
 #      }
 #
 # Here each variant backward-references "url" --> "https://example.com"
 #
 # However, they each inherit key "name" which is dynamically resolved using
 # the "name0" and "name1" defined by the particular child being referenced:
 #
 #      Lookup "thing.variant1.name" --> "AAA-111.zip"
 #      Lookup "thing.variant2.name" --> "AAA-222.zip"
 #      Lookup "thing.variant3.name" --> "BBB-333.zip"
 #
 # Cross-references can use the special "@" character to refer to the platform
 # key passed to the lookup function.
 #
 # Example:
 #
 #      "fedora": {
 #          "name": "Fedora Server",
 #          "url": "https://path.to.fedora/server/images/{@.fedora.vsn}",
 #      }
 #      "p": {
 #          "board": {
 #              "name": "Example Board",
 #              "fedora": {
 #                  "vsn": "27",
 #              },
 #          },
 #          "model": {
 #              "name": "Example Model",
 #              "fedora": {
 #                  "vsn": "28",
 #              },
 #          },
 #      }
 #
 #      Lookup "fedora.url" with plat="p.board" -->
 #          "https://path.to.fedora/server/images/27"
 #      Lookup "fedora.url" with plat="p.model" -->
 #          "https://path.to.fedora/server/images/28"
 #
 # So far all examples have been string substitutions, however cross-references
 # can also point at other dicts and lists by prefixing the {curly} braces with
 # a hash/pound sign #:
 #
 #      "p.board": {
 #          "name": "Example board platform",
 #          "k": [
 #              "k.kernel1", "k.kernel2",
 #          ],
 #      },
 #      "p.model": {
 #          "name": "Example model platform",
 #          "k": "#{p.board.k}",
 #      }
 #
 #      Lookup "p.model.k" --> ["k.kernel1", "k.kernel2"]
 #
 # Finally, keys exactly matching string "null" will return Python's None.
###
ARMPLATDB = {
  "arm": {
    "rel": "19.10", "pbrel": "{rel}", "mrel": "ARMLT-{rel}",
    "cms": "developer.arm.com",
  },

  "linaro": {
    "lt": "Linaro/ArmLT",
    "url": "releases.linaro.org",
  },

  "pkgs": {
    "apt": {
      "common": [
        "acpica-tools", "autoconf", "bc", "bison", "bridge-utils",
        "build-essential", "curl", "device-tree-compiler", "expect", "flex",
        "g++-multilib", "gcc-multilib", "genext2fs", "gperf", "libc6:i386",
        "libssl-dev", "libstdc++6:i386", "libncurses5:i386", "libxml2",
        "libxml2-dev", "libxml2-utils", "libxml-libxml-perl", "make",
        "openssh-server", "openssh-client", "python", "python-pip", "uuid-dev",
      ],

      "m": [
        "automake", "android-tools-adb", "android-tools-fastboot", "cython",
        "kernelshark", "libfreetype6-dev", "libpng-dev", "libtool",
        "net-tools", "nmap",  "openjdk-8-jdk", "pkg-config", "python-dev",
        "python-mako", "python-matplotlib", "python-nose", "python-numpy",
        "python-pip", "python-wand", "python-wrapt", "screen", "sshpass",
        "trace-cmd", "tree",
      ],

      "i": [
        "autoconf", "doxygen", "fuseext2", "locales", "mtools", "wget",
        "zip", "zlib1g:i386", "zlib1g-dev:i386",
      ],
    },

    "pip": {
      "m": [
        "IPython", "bart-py", "devlib", "jupyter", "nose", "pandas", "pexpect",
        "psutil", "pyserial", "trappy", "wheel",
      ],
    },
  },

  ###
   # Platforms that can be chosen by the user.
   #
   # Each platform must define:
   #
   #    name: display name printed in menus
   #    type: type of platform from "m"obile, "i"nfrastructure, or "null"
   #    murl: URL of git repository containing platform's manifests
   #    mrel: branch of git repository containing platform's manifests
   #    pdir: build script directory
   #    k: list of supported kernels (or "null")
   #    fs: list of supported userspace filesystems (or "null")
   #    fw: list of supported firmware & test suites (or "null")
   #    pb: list of supported prebuilt configurations (or "null")
   #    pburl: location of platform's prebuilt archives
   #    includes: list of other included software components (or "null")
   #    deps: list of required downloads (such as compilers)
   #    pihooks: list of post-init hook functions to run (see class pihooks)
   #    docs: location of the platform's documentation
   #
   # Further, platforms advertising support for certain kernels and userspace
   # filesystems must define additional keys.
   #
   # If advertising support for k.ack, the platform must define:
   #
   #    ack.manifest: repo manifest file name e.g. "pinned-juno.xml"
   #
   # If advertising support for any variant of fs.oe, the platform must define:
   #
   #    oe.rel: OpenEmbedded release
   #    oe.vsn: OpenEmbedded version
   #    oe.url: URL of OpenEmbedded downloads
   #    oe.md5name: MD5 checksum file name
   #
   # If advertising support for fs.android, the platform must define:
   #
   #    android.rel: Android release
   #    android.codename: Android code name e.g. Marshmallow, Oreo, Pie
   #    android.url: URL of Android downloads
   #    android.rootfs: root filesystem image name
   #    android.ramdisk.dir: ramdisk destination directory
   #
  ###
  "p": {
    "name": "Platforms",

    ### Default keys inherited by all platforms and optionally overridden
    "murl": "https://git.linaro.org/landing-teams/working/arm/arm-reference-platforms-manifest",
    "mrel": "{arm.mrel}",
    "pbrel": "{arm.pbrel}",
    "pburl": "{linaro.url}/members/arm/platforms/{pbrel}",
    "docs": "https://community.arm.com/oss-platforms/w/docs/",
    "build": "arm",
    "bsgroup": "configs",
    "pihooks": "null",
    "type": "null",
    "ack": {
      "manifest": "pinned-ack.xml",
    },

    ### Boards
    "board": {
      "name": "Development boards",

      ### Juno
      "juno": {
        "name": "Juno",
        "type": "m",
        "includes": [
          "oc.mb", "oc.scp", "oc.tfa", "oc.optee", "oc.uboot",
        ],

        ### Juno with 64-bit SW
        "64b": {
          "name": "Juno with 64-bit software stack",
          "pdir": "juno",
          "deps": [
            "dl.tool.gcc.a64", "dl.tool.gcc.a32",
          ],
          "ack": {
            "manifest": "pinned-juno.xml",
          },
          "android": {
            "rel": "19.01",
            "codename": "Pie",
            "rootfs": "juno.img.bz2",
            "url": "{linaro.url}/members/arm/android/juno/{rel}",
            "ramdisk": {
              "dir": "prebuilts/android/juno",
            },
          },
          "oe": {
            "rel": "17.01",
            "vsn": "5.2_20170127-761",
            "url": "{linaro.url}/openembedded/juno-lsk/{rel}",
            "md5name": "{dl.img.oe.name}.md5",
          },
          "k": [
            "k.ack", "k.latest"
          ],
          "fs": [
            "fs.busybox", "fs.oe.mini", "fs.oe.lamp", "fs.android",
          ],
          "fw": [
            "fw.edkii",
          ],
          "pb": [
            "pb.ack.android",
            "pb.latest.busybox",
            "pb.latest.oe.mini",
            "pb.latest.oe.lamp",
            "pb.edkii",
          ],
        },

        ### Juno with 32-bit SW
        "legacy": {
          "name": "Juno with legacy 32-bit software stack",
          "pdir": "juno32",
          "deps": [
            "dl.tool.gcc.a64", "dl.tool.gcc.a32",
          ],
          "oe": {
            "rel": "15.07",
            "vsn": "4.9_20150725-725",
            "url": "{linaro.url}/openembedded/vexpress-lsk/{rel}",
          },
          "k": [
            "k.ack", "k.latest",
          ],
          "fs": [
            "fs.busybox", "fs.oe.alip",
          ],
          "fw": "null",
          "pb": [
            "pb.ack.busybox",
            "pb.latest.busybox",
            "pb.latest.oe.alip",
          ],
        },
      },

      ### Neoverse N1 System Development Platform
      "n1sdp": {
        "name": "Neoverse N1 SDP",
        "type": "i",
        "includes": [
          "oc.mb", "oc.scp", "oc.tfa", "fw.edkii", "oc.grub",
        ],
        "pdir": "n1sdp",
        "bsgroup": "platforms",
        "mrel": "???",
        "tagkey": "N1SDP",
        "pburl": "https://git.linaro.org/landing-teams/working/arm/n1sdp-board-firmware.git/snapshot/",
        "pbrel": "N1SDP-2019.09.13",
        "docs": "docs/{pdir}",
        "pihooks": [
          "build_script__ubuntu_patches", "pcie_fix", "mv_grub",
        ],
        "deps": [
          "dl.tool.gcc.scp.7", "dl.tool.gcc.a64",
        ],
        "k": [
          "k.mainline"
        ],
        "linux": {
          "vsn": "5.2.8",
        },
        "fs": [
          "fs.ubuntu", "fs.busybox",
        ],
        "fw": "null",
        "pb": [
          "pb.ubuntu",
        ],
      },

      ### TC2
      "tc2": {
        "name": "TC2",
        "type": "m",
        "pdir": "tc2",
        "deps": [
          "dl.tool.gcc.a32",
        ],
        "android": {
          "rel": "6.0-15.11",
          "codename": "Marshmallow",
          "rootfs": "vexpress.img.bz2",
          "url": "{linaro.url}/android/reference-lcr/vexpress/{rel}",
          "ramdisk": {
            "dir": "prebuilts/android/tc2",
          },
        },
        "oe": "#{p.board.juno.legacy.oe}",
        "k": "#{p.board.juno.legacy.k}",
        "fs": [
          "fs.busybox", "fs.oe.alip", "fs.android",
        ],
        "fw": [
          "fw.edkii",
        ],
        "pb": "null",
      },
    },

    ### Fixed Virtual Platforms (FVPs)
    "fvp": {
      "name": "Fixed Virtual Platforms (FVPs)",

      ### Armv8 architecture FVPs
      "v8a": {
        "name": "Armv8 architecture",
        "type": "m",
        "pdir": "fvp",
        "includes": [
          "oc.tfa", "oc.optee",
        ],

        ### Armv8-A Base Platform
        "base": {
          "name": "Armv8-A Base Platform",
          "descr": "11.3.30+ (Rev C)",

          ### Armv8-A Base Platform with 64-bit SW
          "64b": {
            "name": "Armv8-A Base Platform with 64-bit software stack",
            "deps": [
              "dl.tool.gcc.a64", "dl.tool.gcc.a32",
            ],
            "descr": "null",
            "android": {
              "rel": "7.0-16.10",
              "codename": "Nougat",
              "rootfs": "fvp.img.bz2",
              "url": "{linaro.url}/android/reference-lcr/fvp/{rel}",
              "ramdisk": {
                "dir": "prebuilts/android/fvp",
              },
            },
            "oe": {
              "rel": "15.09",
              "vsn": "4.9_20150912-729",
              "url": "{linaro.url}/openembedded/juno-lsk/{rel}",
              "md5name": "MD5SUMS.txt",
            },
            "k": [
              "k.ack", "k.latest",
            ],
            "fs": [
              "fs.busybox", "fs.oe.mini", "fs.oe.lamp", "fs.android",
            ],
            "fw": [
              "fw.edkii",
            ],
            "pb": [
              "pb.ack.android",
              "pb.latest.oe.mini",
              "pb.latest.oe.lamp",
              "pb.ack.busybox",
              "pb.latest.busybox",
              "pb.edkii",
            ],
          },

          ### Armv8-A Base Platform with 32-bit SW
          "legacy": {
            "name": "Armv8-A Base Platform with legacy 32-bit software stack",
            "pdir": "fvp32",
            "deps": [
              "dl.tool.gcc.a32",
            ],
            "descr": "null",
            "oe": "#{p.board.juno.legacy.oe}",
            "k": "#{p.board.juno.legacy.k}",
            "fs": "#{p.board.juno.legacy.fs}",
            "fw": "null",
            "pb": "#{p.board.juno.legacy.pb}",
          },
        },

        ### Foundation Model
        "fndn": {
          "name": "Armv8-A Foundation Model",
          "descr": "11.3.30+",

          ### Foundation Model with 64-bit SW
          "64b": {
            "name": "Armv8-A Foundation Model with 64-bit software stack",
            "deps": [
              "dl.tool.gcc.a64", "dl.tool.gcc.a32",
            ],
            "descr": "null",
            "android": "#{p.fvp.v8a.base.64b.android}",
            "oe": "#{p.fvp.v8a.base.64b.oe}",
            "k": "#{p.fvp.v8a.base.64b.k}",
            "fs": "#{p.fvp.v8a.base.64b.fs}",
            "fw": "#{p.fvp.v8a.base.64b.fw}",
            "pb": "#{p.fvp.v8a.base.64b.pb}",
          },
        },
      },

      ### System Guidance
      "sg": {
        "name": "System Guidance",
        "deps": [
          "dl.tool.gcc.a64", "dl.tool.gcc.a32", "dl.tool.gcc.scp.5",
        ],

        ### System Guidance for Mobile (SGM)
        "m": {
          "name": "System Guidance for Mobile (SGM)",
          "type": "m",
          "includes": [
            "oc.scp", "oc.tfa", "oc.optee", "oc.uboot",
          ],

          ### SGM-775
          "775": {
            "name": "SGM-775",
            "pdir": "sgm775",
            "android": {
              "rel": "(built from source)",
              "codename": "Oreo",
            },
            "k": [
              "k.ack.sgm775",
            ],
            "fs": [
              "fs.android.bfs", "fs.busybox",
            ],
            "pb": [
              "pb.ack.busybox", "pb.ack.android.big",
            ],
            "fw": "null",
          },
        },
      },
    },

    ### Corstone
    "corstone": {
      "name": "Corstone Foundation IP",

      ### Corstone-700
      "700": {
        "name": "Corstone-700",
        "pdir": "corstone700",
        "mrel": "???",
        "tagkey": "CORSTONE-700",
        "knowntag": "CORSTONE-700-2019.09.23",
        "build": "yocto",
        "docs": "docs/{pdir}",
        "platsw": {
          "manifest": "{pdir}.xml",
        },
        "k": "null",
        "fs": "null",
        "fw": [
          "fw.platsw",
        ],
        "pb": "null",
        "includes": [
          "oc.tfa", "oc.uboot", "oc.tiny", "oc.cmsis",
        ],
        "excludes": [
          "fw.platsw", # Hide it from final configuration summary
        ],
      },
    },

    ### DesignStart
    "ds": {
      "name": "DesignStart",

      ### Cortex-A5 DesignStart
      "a5": {
        "name": "Cortex-A5 DesignStart",
        "pdir": "ca5ds",
        "mrel": "???",
        "tagkey": "CA5-DESIGNSTART",
        "knowntag": "{tagkey}-2019.09.16",
        "build": "yocto",
        "docs": "docs/{pdir}",
        "platsw": {
          "manifest": "{pdir}.xml",
        },
        "k": "null",
        "fs": "null",
        "fw": [
          "fw.platsw",
        ],
        "pb": "null",
        "includes": [
          "oc.tfa", "oc.uboot", "oc.tiny",
        ],
        "excludes": [
          "fw.platsw", # Hide it from final configuration summary
        ],
      },
    },

    ### All supported platforms
    ### Platforms need to be in this list to appear in the menus
    "all": [
      "p.board.juno.64b", "p.board.juno.legacy", "p.board.tc2",
      "p.fvp.v8a.base.64b", "p.fvp.v8a.base.legacy", "p.fvp.v8a.fndn.64b",
      "p.fvp.sg.m.775", "p.board.n1sdp", "p.corstone.700", "p.ds.a5",
    ],
  },

  ###
   # Kernels that can be chosen by the user.
   #
   # Each kernel must define:
   #
   #    name: display name printed in menus
   #    manifest: repo manifest file name
   #    fs: list of supported userspace filesystems
   #
   # Kernels may optionally define:
   #
   #    descr: description printed in menus
   #
   # Note: the list of userspace filesystems actually presented to the user is
   # the intersection between what both the platform and kernel support.
   #
   # Some kernels are surfaced through multiple manifests for the same platform,
   # for example k.ack on sgm775 through either sgm775.xml (for BusyBox) or
   # sgm775-android.xml (for Android).
   #
   # Instead of defining manifest and fs, these kernels must define:
   #
   #    map: dict mapping supported userspace filesystems to repo manifests
   #
  ###
  "k": {
    "name": "Linux kernel & userspace filesystem",
    "priority": 51,

    ### Android Common Kernel (ACK)
    "ack": {
      "name": "{linaro.lt} Android Common Kernel",
      "manifest": "{@.ack.manifest}",
      "fs": [
        "fs.busybox",
        "fs.oe.alip",
        "fs.oe.mini",
        "fs.oe.lamp",
        "fs.android",
        "fs.android.bfs",
      ],

      ### SGM-775 variants for running BusyBox or Android respectively
      "sgm775": {
          "maps": {
            "fs.busybox": "sgm775.xml",
            "fs.android.bfs": "sgm775-android.xml",
          },
      },
    },

    ### Latest landing team kernel
    "latest": {
      "name": "{linaro.lt} Latest Stable Kernel",
      "manifest": "pinned-latest.xml",
      "fs": [
        "fs.busybox", "fs.oe.alip", "fs.oe.mini", "fs.oe.lamp",
      ],
    },

    ### Mainline Linux
    "mainline": {
      "name": "Mainline Kernel",
      "manifest": "pinned-{@.pdir}.xml",
      "fs": [
        "fs.busybox", "fs.fedora", "fs.ubuntu",
      ],
    },
  },


  ###
   # Filesystems that can be chosen by the user.
   #
   # Each filesystem must define:
   #
   #    name: display name printed in menus
   #    script: build script file name
   #
   # Filesystems may optionally define:
   #
   #    descr: description printed in menus
   #    deps: list of required downloads
  ###
  "fs": {
    "priority": 61,

    ### Android
    "android": {
      "name": "Android {@.android.codename}",
      "script": "android",
      "deps": [
        "dl.img.android.rootfs", "dl.img.android.ramdisk"
      ],

      ### Build from source variant
      "bfs": {
        "deps": "null",
      },
    },

    ### BusyBox
    "busybox": {
      "name": "BusyBox",
      "script": "busybox",
    },

    ### OpenEmbedded
    "oe": {
      "name": "OpenEmbedded",
      "script": "oe",

      ### ALIP variant
      "alip": {
        "name": "OpenEmbedded ALIP",
        "deps": [
          "dl.img.oe.alip",
        ],
      },

      ### Minimal variant
      "mini": {
        "name": "OpenEmbedded Minimal",
        "deps": [
          "dl.img.oe.mini"
        ],
      },

      ### LAMP variant
      "lamp": {
        "name": "OpenEmbedded LAMP",
        "deps": [
          "dl.img.oe.lamp"
        ],

        ### N1SDP variant syncs a rootfs.tar from manifest then builds .img
        "n1sdp": {
          "deps": "null",
        },
      },
    },

    ### Fedora Server
    "fedora": {
      "name": "Fedora Server",
       # Fedora doesn't have a build script; we just need to get UEFI installed
       # and then boot the iso. Unfortunately SGI platforms don't have a fw.edkii
       # config so we'll need to build a kernel and userspace filesystem even
       # though it won't be used. Use BusyBox as it has no deps and builds fast.
      "script": "busybox",
      "deps": [
        "dl.img.fedora",
      ],
    },

    ### Ubuntu Server
    "ubuntu": {
      "name": "Ubuntu Server",
      "script": "ubuntu",
      "deps": [
        "dl.rootfs.ubuntu",
      ],
    },
  },


  ###
   # Other software stacks that can be chosen by the user, including firmware and
   # test suites.
   #
   # Each fw must define:
   #
   #    name: display name printed in menus
   #    manifest: repo manifest file name
   #
   # If a fw is built using the Arm build scripts, it must define:
   #
   #    stubfs: build script file name
   #
   # A fw may optionally define:
   #
   #    descr: description printed in menus
  ###
  "fw": {
    "name": "Other",

    ### EDK II UEFI
    "edkii" : {
      "name": "EDK II UEFI",
      "priority": 31,
      "stubfs": "uefi",
      "manifest": "pinned-{stubfs}.xml",
      "excludes": [
        "oc.uboot",
      ],
    },

    ### Platform-specific software stack e.g. for Corstone-700
    "platsw": {
      "name": "{@.name} software stack",
      "priority": 31,
      "manifest": "{@.platsw.manifest}",
    },
  },


  ###
   # Prebuilt configurations that can be chosen by the user.
   #
   # Each prebuilt configuration must define:
   #
   #    name: display name printed in menus
   #    deps: list of required downloads
  ###
  "pb": {

    ### Ubuntu
    "ubuntu": {
      "name": "{k.mainline.name} + {fs.ubuntu.name}",
      "deps": [
        "dl.archive.ubuntu",
      ],
      "includes": [
        "k.mainline", "fs.ubuntu",
      ],
    },

    ### ACK configs
    "ack": {
      "name0": "{k.ack.name}",

      ### U-Boot + ACK + Android
      "android": {
        "name": "{name0} + {fs.android.name}",
        "deps": [
          "dl.img.android.rootfs", "dl.archive.ack.android",
        ],
        "includes": [
          "oc.uboot", "k.ack", "fs.android",
        ],

        ### Debug variant
        "debug": {
          "deps": [
            "dl.img.android.rootfs",
            "dl.archive.ack.android",
            "dl.archive.ack.android.debug",
          ],
        },

        ### Fully-packaged variant (already contains rootfs image)
        "big": {
          "name": "{name0} + {fs.android.name}",
          "deps": [
            "dl.archive.ack.android",
          ],
        },
      },

      ### U-Boot + ACK + BusyBox
      "busybox": {
        "name": "{name0} + {fs.busybox.name}",
        "deps": [
          "dl.archive.ack.busybox"
        ],
        "includes": [
          "oc.uboot", "k.ack", "fs.busybox",
        ],
      },
    },

    ### Latest landing team kernel configs
    "latest": {
      "name0": "{k.latest.name}",

      ### U-Boot + latest-armlt + BusyBox
      "busybox": {
        "name": "{name0} + {fs.busybox.name}",
        "deps": [
          "dl.archive.latest.busybox"
        ],
        "includes": [
          "oc.uboot", "k.latest", "fs.busybox",
        ],

        ### EDK II UEFI + Mainline variant
        "edkii": {
          "name0": "{fw.edkii.name}",
          "deps": [
            "dl.archive.latest.busybox.edkii"
          ],
          "includes": [
            "fw.edkii", "k.mainline.pb", "fs.busybox",
          ],
        },
      },

      ### latest-armlt + OpenEmbedded
      "oe": {

        ### ALIP variant
        "alip": {
          "name": "{name0} + {fs.oe.alip.name}",
          "deps": [
            "dl.img.oe.alip", "dl.archive.latest.oe",
          ],
          "includes": [
            "oc.uboot", "k.latest", "fs.oe.alip",
          ],
        },

        ### Minimal variant
        "mini": {
          "name": "{name0} + {fs.oe.mini.name}",
          "deps": [
            "dl.img.oe.mini", "dl.archive.latest.oe",
          ],
          "includes": [
            "oc.uboot", "k.latest", "fs.oe.mini",
          ],

          ### Minimal Debug variant
          "debug": {
            "deps": [
              "dl.img.oe.mini",
              "dl.archive.latest.oe",
              "dl.archive.latest.oe.debug",
            ],
          },
        },

        ### LAMP variant
        "lamp": {
          "name": "{name0} + {fs.oe.lamp.name}",
          "deps": [
            "dl.img.oe.lamp", "dl.archive.latest.oe",
          ],
          "includes": [
            "oc.uboot", "k.latest", "fs.oe.lamp",
          ],

          "edkii": {
            "name": "{k.mainline.name} + {fs.oe.lamp.name}",
            "deps": [
              "dl.archive.latest.oe.edkii",
            ],
            "includes": [
              "fw.edkii", "k.mainline", "fs.oe.lamp",
            ],
          },

          ### LAMP Debug variant
          "debug": {
            "deps": [
              "dl.img.oe.lamp",
              "dl.archive.latest.oe",
              "dl.archive.latest.oe.debug",
            ],
          },
        },
      },
    },

    ### Standalone EDK II UEFI
    "edkii": {
      "name": "{fw.edkii.name}",
      "deps": [
        "dl.archive.edkii",
      ],
      "includes": [
        "fw.edkii",
      ],
    },
  },


  ###
   # Other software components that are included based on the user's choices.
  ###
  "oc": {

    ### Motherboard firmware
    "mb": {
      "name": "Motherboard firmware",
      "priority": 0,
    },

    ### Trusted Firmware-A
    "tfa": {
      "name": "Trusted Firmware-A",
      "priority": 11,
    },

    ### SCP-firmware
    "scp": {
      "name": "SCP-firmware",
      "priority": 12,
    },

    ### OP-TEE
    "optee": {
      "name": "OP-TEE ",
      "priority": 21,
    },

    ### GNU GRUB
    "grub": {
      "name": "GRUB",
      "priority": 41,
    },

    ### U-Boot
    "uboot": {
      "name": "U-Boot",
      "priority": 41,
      "excludes": [
        "fw.edkii",
      ],
    },

    ### Tiny Linux
    "tiny": {
      "name": "Tiny Linux distribution (based on Poky-Tiny)",
      "priority": 60,
    },

    ### CMSIS
    "cmsis": {
      "name": "Arm CMSIS",
      "priority": 51,
    },
  },


  ###
   # Downloads.
   #
   # Each download must define:
   #
   #    name: file name
   #    url: base URL
   #    dir: destination directory, relative to <workspace> root
   #
   # Downloads may optionally define:
   #
   #    md5name: md5 checksum file name
   #
   # The actual URL used to download the file is "{url}/{name}". Similarly, the
   # actual URL used to download the md5 checksum file is "{url}/{md5name}".
  ###
  "dl": {
    "extract": "true", # Default behaviour is to extract recognised archive formats

    ### Tools
    "tool": {

      ### Compilers
      "gcc": {
        "rel": "6.2-2016.11",
        "vsn": "6.2.1-2016.11",
        "url":"http://{linaro.url}/components/toolchain/binaries/{rel}/{tuple}",
        "name": "gcc-linaro-{vsn}-x86_64_{tuple}.tar.xz",
        "md5name": "{name}.asc",
        "dir": "tools/gcc",

        ### a32 compiler
        "a32": {
          "tuple": "arm-linux-gnueabihf",
        },

        ### a64 compiler
        "a64": {
          "tuple": "aarch64-linux-gnu",
        },

        ### SCP/MCP compilers (GNU-RM)
        "scp": {
          "tuple": "arm-none-eabi",
          "name": "gcc-{tuple}-{vsn}-linux.tar.bz2",

          ### GNU-RM 5
          "5": {
            "url": "https://launchpad.net/gcc-arm-embedded/{rel}/+download",
            "md5name": "{name}/+md5",
            "rel": "5.0/5-2016-q3-update",
            "vsn": "5_4-2016q3-20160926",
          },

          ### GNU-RM 7
          "7": {
            "url": "{arm.cms}/-/media/Files/downloads/gnu-rm/{rel}",
            "md5name": "null",
            "rel": "7-2018q2",
            "vsn": "7-2018-q2-update",
          },
        },
      },

      ### Repo
      "repo": {
        "name": "repo",
        "dir": "tools",
        "url": "storage.googleapis.com/git-repo-downloads",
      },
    },

    ### Images
    "img": {
      "dir": ".",  # Unless overridden, images are extracted to workspace <root>

      ### Android
      "android": {
        "url": "{@.android.url}",
        "md5name": "MD5SUMS",
        "rootfs": {
          "name": "{@.android.rootfs}",
        },
        "ramdisk": {
          "name": "ramdisk.img",
          "dir": "{@.android.ramdisk.dir}"
        },
      },

      ### OpenEmbedded
      "oe": {
        "url": "{@.oe.url}",
        "name": "{name0}-openembedded_{name1}-{name2}-gcc-{@.oe.vsn}.img.gz",

        ### ALIP image
        "alip": {
          "name0": "lsk-vexpress",
          "name1": "alip",
          "name2": "armv7a",
          "md5name":"null",
        },

        ### Minimal image
        "mini": {
          "name0": "lt-vexpress64",
          "name1": "minimal",
          "name2": "armv8",
          "md5name": "{@.oe.md5name}",
        },

        ### LAMP image
        "lamp": {
          "name0": "lt-vexpress64",
          "name1": "lamp",
          "name2": "armv8",
          "md5name": "{@.oe.md5name}",
        },
      },

      ### Fedora Server
      "fedora": {
        "url0": "https://dl.fedoraproject.org/pub/fedora-secondary/releases",
        "url": "{url0}/{@.fedora.rel}/Server/aarch64/iso/",
        "name": "Fedora-Server-dvd-aarch64-{@.fedora.vsn}.iso",
      },
    },

    ### Filesystem archives
    "rootfs": {
      "ubuntu": {
        "url": "http://cdimage.ubuntu.com/ubuntu-base/bionic/daily/current",
        "name": "bionic-base-arm64.tar.gz",
        "dir": "build-scripts/prebuilts/ubuntu",
        "extract": "false",
      },
    },

    ### Prebuilt archives
    "archive": {
      "url": "{@.pburl}",
      "md5name": "MD5SUMS.txt",
      "dir": "{basename}",
      "name0": "{@.pdir}",
      "name3": "uboot",
      "basename": "{name0}-{name1}-{name2}-{name3}",
      "name": "{basename}.{fmt}",
      "fmt": "zip",

      ### ACK based archives
      "ack": {
        "name1": "ack",

        ### ACK + Android
        "android": {
          "name2": "{fs.android.script}",

          ### Debug variant
          "debug": {
            "name3": "debug",
            "fmt": "tar.xz",
          },
        },

        ### ACK + BusyBox
        "busybox": {
          "name2": "{fs.busybox.script}",
        },
      },

      ### latest-armlt based archives
      "latest": {
        "name1": "latest",

        ### U-Boot + latest-armlt + BusyBox
        "busybox": {
          "name2": "{fs.busybox.script}",

          ### Replace U-Boot with UEFI
          "edkii": {
            "name3": "{fw.edkii.stubfs}",
          },
        },

        ### latest-armlt + OE
        "oe": {
          "name2": "{fs.oe.script}",

          ### Debug variant
          "debug": {
            "name3": "debug",
            "fmt": "tar.xz",
          },

          ### EDK II UEFI variant
          "edkii": {
            "name3": "uefi",
          },
        },
      },

      ### Standalone EDK II UEFI archive
      "edkii": {
        "basename": "{name0}-{fw.edkii.stubfs}",
      },

      ### Ubuntu
      "ubuntu": {
        "basename": "{@.pdir}-board-firmware-{@.pbrel}",
        "fmt": "tar.gz",
        "md5name": "null",
      },
    },
  },
}


"""
 " See documentation of ARMPLATDB.
"""
class Database(dict):
    def lookup( self, key, plat=None, noneAllowed=False ):
        log.debug("looking {} (plat={}, nA={})".format(key, plat, noneAllowed))
        def subPlat(k):
            try:
                return k.replace("@", plat) if "@" in k else k
            except TypeError:
                script.abort("lookup key={} with invalid plat={}"
                             .format(key, plat))
        # We assimilate keys into d at each level of lookup, allowing for keys
        # to be inherited and overridden by later levels.
        d = {}
        assimilate = lambda src: [d.update({k:v}) for k,v in src.items()]
        assimilate(self)
        # Perform recursive lookup
        (lookupLvl, item) = (d, None)
        for k in subPlat(key).split("."):
            item = lookupLvl[k] if k in lookupLvl else d[k] if k in d else None
            if item is None:
                break
            # Handle cross-references
            if isinstance(item, str) and item.startswith("#"):
                if item.count("{")==item.count("}")==1:
                    (l, r) = (item.find("{"), item.find("}"))
                    item = Database(d).lookup(item[l+1:r], plat)
            # Prepare for next level of lookup
            if isinstance(item, dict):
                item = Database(item)
                lookupLvl = item
                assimilate(lookupLvl)
        # String items have special behaviour
        if isinstance(item, str):
            log.debug("got {}".format(item))
            if "{{{}}}".format(key) == item:
                script.abort("recursive lookup 111")
            if "null" == item:
                item = None
            elif "true" == item:
                item = True
            elif "false" == item:
                item = False
            else:
                item = subPlat(item)
                if not item.count("{")==item.count("}"):
                    script.abort(("lookup of key={} with plat={} gives item={} "
                                  "with imbalanced number of {{ and }}")
                                  .format(key, plat, item))
                while "{" in item:
                    (l, r) = (item.find("{"), item.find("}"))
                    search, replace = item[l+1:r], item[l:r+1]
                    sub = Database(d).lookup(search, plat)
                    old_item = item
                    item = item.replace(replace, sub)
                    log.debug("substitution of {}='{}' in {} gave {}"
                              .format(replace, sub, old_item, item))
                    if item == old_item:
                        log.debug("detected possible recursion")
                        log.debug("attempting lookup again using root database")
                        sub = dblu(search, plat)
                        item = old_item.replace(replace, sub)
                        log.debug("resubstitution of {}='{}' in {} gave {}"
                                  .format(replace, sub, old_item, item))
                        if item == old_item:
                            script.abort("recursive lookup")
        if item is None and not noneAllowed:
            log.info(d)
            script.abort("lookup of {} (plat={}) returns None but nA=False"
                         .format(key, plat))
        return item


    def multilookup( self, root, keys, plat=None, noneAllowed=False ):
        return [self.lookup(root+"."+k, plat, noneAllowed) for k in keys]


"""
 " Cast ARMPLATDB into an actual Database instance, then define shorthand
 " wrappers for lookup and multi-key lookup.
"""
ARMPLATDB = Database(ARMPLATDB)

def dblu( key, plat=None, noneAllowed=False ):
    return ARMPLATDB.lookup(key, plat, noneAllowed)

def dblum( root, keys, plat=None, noneAllowed=False ):
    return ARMPLATDB.multilookup(root, keys, plat, noneAllowed)


"""
 " Script initialisation and configuration.
"""
class script:
    def init():
        # Parse arguments
        p = argparse.ArgumentParser()
        p.add_argument("-D", help="Debug mode", action="store_true")
        p.add_argument("--qa_mode", help="for Arm internal QA purposes",
                       action="store_true")
        p.add_argument("--no_check_apt_deps", action="store_true",
                       help="do not check for APT package dependencies")
        p.add_argument("--force_unknown_tag", action="store_true",
                       help="for Arm internal use")
        args = p.parse_args()
        (script.qa_mode, script.no_check_apt_deps, script.force_unknown_tag) = \
            (args.qa_mode, args.no_check_apt_deps, args.force_unknown_tag)
        # Configure logging
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        fmt = logging.Formatter("%(levelname)s: %(message)s")
        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG if args.D else logging.INFO)
        console.setFormatter(fmt)
        logfile = logging.FileHandler("log.txt", "w")
        logfile.setLevel(logging.DEBUG)
        logfile.setFormatter(fmt)
        logger.addHandler(console)
        logger.addHandler(logfile)
        log.info("date is {}".format(time.strftime('%Y-%m-%d %H:%M:%S')))
        log.info("running on {} host".format(HOST))
        # Other setup
        script.aborts = []
        sh.init()


    """
     " Start a QA session where we attempt to fetch every download and sync
     " every repo manifest defined in ARMPLATDB; this helps to identify URLs
     " that have have gone stale since the previous release / QA run.
    """
    def start_qa():
        script.qa_t0 = time.time()


    """
     " End a QA session, printing useful diagnostics.
    """
    def end_qa( hard_aborted=False ):
        t = time.time() - script.qa_t0
        hrs = math.floor(t / 3600)
        mins = math.floor((t % 3600) / 60)
        secs = math.floor((t % 3600) % 60)
        logfn = log.info if len(script.aborts)==0 else log.error
        msg = ("QA run {} after {}hrs {}mins {}secs"
               .format('completed' if not hard_aborted else 'HARD ABORTED',
                        hrs, mins, secs))
        wall = "#"*len(msg)
        logfn(wall)
        logfn(msg)
        logfn("Total number of aborts: {}".format(len(script.aborts)))
        logfn(wall)
        logfn("QA result: " + ('SUCCESS' if len(script.aborts)==0 else 'FAIL'))
        logfn(wall)
        return len(script.aborts)


    def abort( e=None, hard=True ):
        if e:
            log.error("")
            log.error(str(e))
        script.aborts.append(str(e) if e else "<<empty abort : see full log>>")
        do_exit = True
        if script.qa_mode:
            if hard:
                script.end_qa(hard_aborted=True)
            else:
                do_exit = False
        if do_exit:
            sys.exit(e.errno if hasattr(e, "errno") else -1)


"""
 " Convenience wrappers around logging operations.
"""
class log:
    def debug( msg ): logging.getLogger(__name__).debug(msg)
    def info ( msg ): logging.getLogger(__name__).info (msg)
    def warn ( msg ): logging.getLogger(__name__).warn (msg)
    def error( msg ): logging.getLogger(__name__).error(msg)


"""
 " Convenience wrappers around shell and file I/O operations.
"""
class sh:
    """
     " All file I/O operations are performed relative to <workspace> root; if
     " the script resident directory and the current working directory differ
     " then we need to user to clarify which they want to be their <workspace>.
    """
    def init():
        (srd, cwd) = (sh.fmtpath(sys.path[0])+"/", sh.fmtpath(os.getcwd())+"/")
        if HOST=="Linux":
            (srd, cwd) = ("/"+srd, "/"+cwd)
        sh.cwd = cwd if cwd==srd else \
            prompt("Current working dir differs from script resident dir.\n"
                   "## Please specify which to initialize as your workspace",
                   [
                     choice(cwd, descr="working", meta=cwd),
                     choice(srd, descr="script", meta=srd)
                   ]
            ).meta
        try:
            os.chdir(sh.cwd)
        except OSError as e:
            script.abort(e)
        sh.dld = sh.mkdir("downloads", hidden=True)+"/"
        sh.filename = __file__.rsplit("/" if HOST=="Linux" else "\\")[-1]
        sh.repod = ".repo/"
        check_empty_ws()


    """
     " Use unified '/' path delimiter regardless of host OS.
    """
    def fmtpath( p ):
        p = p.replace("\\", "/")
        while "//" in p:
            p = p.replace("//", "/")
        return p.strip().lstrip("/").rstrip("/")


    """
     " try/except wrapper around caller-provided func(), with optional logging
    """
    def _op( func, *paths, extra=None, silent=False ):
        paths = [sh.fmtpath(p) for p in paths]
        if not silent:
            log.info("{} {} {}".format(func, *paths, extra if extra else ''))
        try:
            return func(*paths) if not extra else func(*paths, extra)
        except OSError as e:
            script.abort(e)


    def mkdir( p, hidden=False ):
        if hidden:
            slash = p.rfind("/")
            p = "{}.{}".format(p[:slash+1], p[slash+1:])
        if not sh._op(os.path.isdir, p, silent=True):
            sh._op(os.makedirs, p)
        if hidden and HOST=="Windows":
            ret = sh._op(ctypes.windll.kernel32.SetFileAttributesW, p,
                         extra=0x2) # 0x2 == FILE_ATTRIBUTE_HIDDEN
            if 0==ret:
                script.abort(ctypes.WinError())
        return p


    def rmdir( p ):
        if sh._op(os.path.isdir, p):
            sh._op(shutil.rmtree, p)


    def cp( src, dstdir ):
        sh._op(shutil.copy, src, dstdir)
        return "{}/{}".format(dstdir, src.split('/')[-1])


    def mv( src, dstdir, rename=None ):
        dstfile = rename if rename else src.split('/')[-1]
        dst = "{}/{}".format(dstdir, dstfile)
        sh._op(shutil.move, src, dst)


    def rm( p ):
        if sh._op(os.path.isfile, p):
            sh._op(os.remove, p)


    """
     " Extract an archive that has standardised extractall() function.
     " This applies to tar and zip.
    """
    def _std_extract( func, src, dstdir, *args, **kwargs ):
        (src, dstdir) = (sh.fmtpath(src), sh.fmtpath(dstdir))
        log.info("{} {} {}".format(func, src, dstdir))
        try:
            with func(src, *args, **kwargs) as f:
                f.extractall(dstdir)
        except OSError as e:
            script.abort(e)
        return dstdir


    """
     " Extract an archive that can be treated as a binary stream.
     " This applies to gzip and bz2.
    """
    def _bin_extract( func, src, dstdir, extn ):
        (src, dstdir) = (sh.fmtpath(src), sh.fmtpath(dstdir))
        dst = "{}/{}".format(dstdir, src.split('/')[-1][:-len(extn)])
        log.info("{} {} {}".format(func, src, dst))
        try:
            with func(src, "rb") as inf:
                with open(dst, "wb") as outf:
                    while True:
                        chunk = inf.read(0x1000)
                        if not chunk:
                            break
                        outf.write(chunk)
        except OSError as e:
            script.abort(e)
        return dst


    def _tarxf( src, dstdir ):
        return sh._std_extract(tarfile.open, src, dstdir, "r:xz", errorlevel=1)


    def _tarxjf( src, dstdir ):
        return sh._std_extract(tarfile.open, src, dstdir, "r:bz2", errorlevel=1)


    def _tarxzf( src, dstdir ):
        return sh._std_extract(tarfile.open, src, dstdir, "r:gz", errorlevel=1)


    def _unzip( src, dstdir ):
        return sh._std_extract(zipfile.ZipFile, src, dstdir, "r")


    def _gunzip( src, dstdir ):
        return sh._bin_extract(gzip.open, src, dstdir, ".gz")


    def _bunzip2( src, dstdir ):
        return sh._bin_extract(bz2.BZ2File, src, dstdir, ".bz2")


    """
     " Extract an archive to a directory, falling back on regular copy if the
     " file is not recognised as an archive. Pass extract=False to also force
     " recognised archives to be copied instead of extracted.
    """
    def extract_or_copy( src, dstdir, extract=True ):
        sh.mkdir(dstdir)
        ends = lambda s: src.endswith(s)
        if not extract:
            handler = sh.cp
        else:
            handler = sh._tarxf   if ends(".tar.xz") else \
                      sh._tarxjf  if ends(".tar.bz2") else \
                      sh._tarxzf  if ends(".tar.gz") else \
                      sh._unzip   if ends(".zip") else \
                      sh._gunzip  if ends(".gz") and not ends(".tar.gz") else \
                      sh._bunzip2 if ends(".bz2") and not ends(".tar.bz2") else \
                      sh.cp
        return handler(src, dstdir)


    """
     " Generate an MD5 checksum for a file.
    """
    def md5sum( p ):
        p = sh.fmtpath(p)
        log.info("md5sum "+p)
        md5 = hashlib.md5()
        try:
            with open(p, "rb") as f:
                while True:
                    block = f.read(md5.block_size)
                    if not block:
                        break
                    md5.update(block)
        except OSError as e:
            script.abort(e)
        md5 = md5.hexdigest()
        log.info("got hash "+md5)
        return md5


    """
     " Check whether a file's actual MD5 checksum matches what is specified in
     " an MD5 checksum file.
    """
    def md5check( p, sumsp ):
        (p, sumsp) = (sh.fmtpath(p), sh.fmtpath(sumsp))
        (md5, name) = (sh.md5sum(p), p.split("/")[-1])
        log.debug("checking md5 of {} in {}".format(name, sumsp))
        try:
            with open(sumsp, "r") as sumsf:
                rstr = re.compile(r"([^\s]+)\s+"+re.escape(name))
                regex = re.search(rstr, sumsf.read())
        except OSError as e:
            script.abort(e)
        if not regex:
            script.abort("no md5 for {} in {}".format(name, sumsp), hard=False)
            return False
        match = "MATCH" if (regex.group(1) == md5) else "MISMATCH"
        log.info("md5 {} {}".format(match, regex.group(1)))
        return (regex.group(1) == md5)


    """
     " Downloads are saved to a subdir of the hidden .downloads/ dir based on
     " the URL from which they were downloaded.
    """
    def url2dld( url ):
        p = url.lstrip("/").rstrip("/").replace(":","_").replace("/","_")
        while "__" in p:
            p = p.replace("__", "_")
        return "{}/{}".format(sh.dld, p)


    """
     " Download a file from a URL with optional pretty-printed progress.
    """
    def wget( url, name, silent=False ):
        def si( num_bytes ):
            if num_bytes <= 0:
                return "0 B"
            suffixes = ["B", "KiB", "MiB", "GiB"]
            log = int(math.floor(math.log(num_bytes, 1024)))
            size = round(num_bytes / 1024**log, 2)
            return "{:.2f} {}".format(size, suffixes[log])
        dld = sh.url2dld(url)
        url = "{}/{}".format(url, name)
        log.info("wget "+url)
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "https://"+url
            log.debug("url does not specify protocol, defaulting to https")
        try:
            r = urllib.request.urlopen(url)
            log.debug("connected to server")
            try:
                endln = " / "+si(int(r.getheader("Content-Length").strip()))
            except:
                endln = ""
                log.debug("server does not support Content-Length header")
                log.debug("file has unknown length")
            sh.mkdir(dld)
            dst = "{}/{}".format(dld, name.split('/')[-1])
            log.info("opening dst file {}".format(dst))
            with open(dst, "wb") as f:
                progress = 0
                while True:
                    chunk = r.read(0x100000)
                    if not chunk:
                        break
                    f.write(chunk)
                    progress += len(chunk)
                    if not silent:
                        # Recalculate on each iter in case terminal is resized
                        erase = "\r{}\r" \
                          .format(' '*(shutil.get_terminal_size().columns-1))
                        print("{}Fetch {}: {}{}"
                              .format(erase, name, si(progress), endln), end="")
                    sys.stdout.flush()
                if not silent:
                    print() ### for \n\r
            log.info("successfully fetched "+si(progress))
            return True
        except (OSError, urllib.error.HTTPError) as e:
            script.abort(e, hard=False)
            return False


    """
     " Convenience around wget() that checks whether a file has already been
     " successfully downloaded and, if yes, skips the download this time. This
     " is only possible for downloads that define an MD5 checksum file as we
     " cannot just rely on a file with the correct name being present. Simiarly
     "
    """
    def fetch( key, plat=None, force_fresh=False ):
        (url, name, md5name, dstdir, extract) =  \
            dblum(key, ["url","name","md5name","dir","extract"], plat, noneAllowed=True)
        dld = sh.url2dld(url)
        dlfile = "{}/{}".format(dld, name.split('/')[-1])
        if md5name:
            md5file = "{}/{}".format(dld, md5name.split('/')[-1])
            sh.wget(url, md5name, silent=True)
        already_fetched = False
        if sh._op(os.path.isfile, dlfile, silent=True):
            if md5name and sh._op(os.path.isfile, md5file, silent=True):
                if not force_fresh and sh.md5check(dlfile, md5file):
                    already_fetched = True
                    print("Already fetched "+name)
                    sys.stdout.flush()
        if not already_fetched:
            sh.wget(url, name)
            if md5name and sh._op(os.path.isfile, md5file, silent=True):
                if not sh.md5check(dlfile, md5file):
                    script.abort("MD5 mismatch after fetching {} (md5file={})"
                                 .format(dlfile, md5file), hard=False)
        print("Extracting {}".format(name))
        return sh.extract_or_copy(dlfile, dstdir, extract)


    """
     " Sync a repo manifest.
    """
    def reposync( manifest, p, mrel, force_fresh=False,):
        log.info("Attempting to sync "+manifest)
        if force_fresh:
            sh.rmdir(".repo")
        repo = sh.fetch("dl.tool.repo")
        def call_repo(argstr):
            sp = subprocess
            cmdline = ['unbuffer', 'python2', repo] + argstr.split(' ')
            log.info("calling {}".format(" ".join(cmdline)))
            proc = sp.Popen(cmdline, stdout=sp.PIPE, stderr=sp.STDOUT,
                            bufsize=0, universal_newlines=True)
            ln = ""
            while proc.returncode is None:
                ln += os.read(proc.stdout.fileno(), 1).decode("utf-8")
                if ln.endswith("\r") or ln.endswith("\n"):
                    log.info(ln.rstrip("\n"))
                    ln = ""
                proc.poll()
            return proc.returncode
        def init():
            log.info("initialising repo")
            cmd = "init -u {} -b {} -m {}".format(dblu('@.murl', p), mrel, manifest)
            if not 0==call_repo(cmd):
                script.abort("failed to initialise repo")
        def sync():
            log.info("syncing repo")
            if not 0==call_repo("sync -j8 --force-sync"):
                script.abort("failed to sync repo", hard=False)
        init()
        sync()


    """
     " Call an external program, optionally piping the program's stderr to its
     " stdout, and optionally piping the program's stdout to the script's.
    """
    def call( args, err2out=False, pipe2sh=False ):
        log.info("calling {}".format(" ".join(args)))
        sp = subprocess
        stdout = None if pipe2sh else sp.PIPE
        stderr = sp.STDOUT if err2out else None if pipe2sh else sp.PIPE
        with sp.Popen(args, stdout=stdout, stderr=stderr) as p:
            (out, err) = p.communicate()
        strip = lambda s: s.decode("utf-8").strip() if s else ""
        return (p.returncode, strip(out), None if err2out else strip(err))


"""
 " Post-initialisation hooks that may be referenced by platforms in ARMPLATDB.
"""
class pihooks():
    """
     " Download the Ubuntu kernel patches
    """
    def build_script__ubuntu_patches():
        if config.ws.meta=="bfs":
            sh.call(["build-scripts/helpers/ubuntu_get_kernel_patches_init"])

    """
     " Fix PCIe quirk on N1SDP (see docs/n1sdp/pcie-quirk.rst)
    """
    def pcie_fix():
        if config.ws.meta=="bfs":
            os.chdir("n1sdp-pcie-quirk")
            sh.call(["chmod", "a+x", "patch_apply.sh"])
            sh.call(["bash", "patch_apply.sh"])
            os.chdir(sh.cwd)

    """
     " Pull N1SDP grub.img out of board_firmware / prebuilt directory
    """
    def mv_grub():
        if config.ws.meta == "bfs":
            base = "board_firmware"
        else:
            base = dblu("dl.archive.ubuntu.basename", config.p.meta)
            base = "{}/{}".format(base, base)
        sh.mv(base+"/SOFTWARE/grub.img", ".", "grub-ubuntu.img")


"""
 " Class representing a choice in a menu.
"""
class choice():
    def __init__( self, name, meta=None, descr=None, disabled=None,
                  children=None ):
        (self.name, self.meta, self.descr, self.disabled, self.children) = \
            (name, meta, descr, disabled, [])
        if children:
            [self.add(c) for c in children]


    """
     " Add a child node to this choice; see tree_prompt().
    """
    def add( self, child ):
        log.debug("append child "+child.meta)
        self.children.append(child)


    """
     " Generate a tree structure of choices; see tree_prompt().
    """
    def tree( keylist, root, plat=None, gen_root=True ):
        if gen_root:
            root = choice("<root>", meta=root)
        log.debug("tree({})".format(root.meta))
        keylist = list(filter(lambda k: k.startswith(root.meta), keylist))
        if len(keylist)==1 and keylist[0]==root.meta:
            log.debug("{} is leaf node".format(root.meta))
            return None
        keys = []
        for k in keylist:
            log.debug(">>>> "+k)
            key = k[len(root.meta)+1:]
            if "." in key:
                key = key[:key.find(".")]
            keys.append(key)
        keys = ["{}.{}".format(root.meta, k) for k in sorted(list(set(keys)))]
        if len(keys) > 0:
            log.debug("generating child nodes")
            for k in keys:
                log.debug("k="+k)
                root.add(choice(
                    dblu(k+".name", plat), meta=k,
                    descr=dblu(k+".descr", plat, noneAllowed=True)))
            log.debug("crawling child nodes")
            for c in root.children:
                choice.tree(
                    keylist,root.children[root.children.index(c)],plat,False)
        return root


"""
 " Prompt the user to make a selection from a list of choices.
"""
def prompt( title, choices ):
    pad = 3 + max([len(c.name) for c in choices])
    def fmt_choice( c ):
        descr = "-- <DISABLED>" if c.disabled else \
                "-- {}".format(c.descr) if c.descr else ""
        return "{:>2}) {:{}}{}".format(choices.index(c)+1, c.name, pad, descr)
    msg = "\n".join(map(fmt_choice, choices))
    msg = "\n\n## {}:\n\n{}\n\n> ".format(title, msg)
    for ln in msg.splitlines():
        if not ln.startswith(">"):
            log.debug(ln)
    while True:
        try:
            i = int(input(msg))
            if (i < 1) or (i > len(choices)):
                raise ValueError()
            i = i - 1
            if choices[i].disabled:
                print("Not available: {}".format(choices[i].descr))
            else:
                break
        except ValueError:
            print("Expected number in range [1..{}] inclusive.\n"
                  .format(len(choices)))
    log.debug("> {} (meta={})".format(i+1, choices[i].meta))
    return choices[i]


"""
 " Prompt the user to make a select from a tree structure of choices; if the
 " chosen choice has more than one child node, prompt the user to also make a
 " selection from those child nodes (if there is only one child node, that child
 " node is automatically selected). Keep going until we hit a leaf node.
"""
last_only_avail = None
def tree_prompt( title, root ):
    last_only_avail = None
    log.debug("tree_prompt "+title)
    log.debug("root has {} children".format(len(root.children)))
    while root.children:
        if len(root.children)==1:
            root = root.children[0]
            if not last_only_avail == root.name:
              log.info("only available option is "+root.name)
              last_only_avail = root.name
        else:
            root = prompt(title, root.children)
    return root


"""
 " Check whether host system has required APT and PIP packages to build from
 " source for the user's chosen platform.
"""
def check_platform_deps( p ):
    plat_type = dblu("@.type", p, noneAllowed=True)
    apt_deps = dblu("pkgs.apt.common")
    pip_deps = []
    if plat_type in ["i", "m"]:
        def add_platform_specific( tool ):
            new_deps = dblu("pkgs.{}.{}"
                            .format(tool, plat_type), noneAllowed=True)
            return new_deps if new_deps else []
        apt_deps += add_platform_specific("apt")
        pip_deps += add_platform_specific("pip")
    check_apt_deps(apt_deps)
    check_pip_deps(pip_deps)


def _abort_missing_pkgs( lst, cmd ):
    print()
    log.error("the following {} packages are missing:".format(cmd))
    log.error("")
    [log.error(" "+d) for d in lst]
    log.error("")
    log.error("please install these packages using:")
    log.error("")
    log.error("{} {}".format(cmd, " ".join(lst)))
    script.abort()


"""
 " Check whether required APT packages are installed.
 "
 " If running on a non-APT based system (such as YUM or DNF), manually install
 " the equivalent packages then re-run the script with ``--no_check_apt_deps``.
"""
def check_apt_deps( lst ):
    if script.no_check_apt_deps:
        log.debug("skipping APT dependency check")
        return
    try:
        import apt
    except:
        log.error("cannot check package dependencies (failed to import apt)")
        log.error("the following apt packages are required:")
        log.error("")
        [log.error(" "+d) for d in lst]
        log.error("")
        log.error("please install python3-apt or check package dependencies")
        log.error("manually and re-run the script with `--no_check_apt_deps'")
        script.abort()
    log.info("checking APT package dependencies")
    log.debug("required package list: {}".format(lst))
    print("\nChecking APT package dependencies... ", end="")
    sys.stdout.flush()
    cache = apt.Cache()
    try:
        missing = list(filter(lambda d: not cache[d].is_installed, set(lst)))
    except KeyError as e:
        print()
        e = "{}".format(e).split("'")[1]
        log.error("cannot find {} as an installable apt package".format(e))
        log.error("are you running on Windows Subsystem for Linux (WSL)?")
        log.error("WSL is not currently a supported environment")
        log.error("you will need to run on a host that can install "+e)
        script.abort()
    if missing:
        _abort_missing_pkgs(missing, "sudo apt-get install")
    print("OK")


"""
 " Check whether required PIP packages are installed.
"""
def check_pip_deps( lst ):
    log.info("checking PIP package dependencies")
    log.info("required package list: {}".format(lst))
    print("Checking PIP package dependencies... ", end="")
    sys.stdout.flush()
    missing = list(filter(lambda p: sh.call(["pip2", "show", p])[0], lst))
    if missing:
        _abort_missing_pkgs(missing, "pip2 install")
    print("OK")


"""
 " Building some host tools breaks with a host gcc that is too old or too new.
"""
def check_sys_gcc():
    log.info("checking system gcc")
    (_, out, _) = sh.call(["gcc", "-dumpversion"])
    ver = tuple([int(i) for i in out.split(".")])
    if ver < (5,4,0) or ver >= (8,0,0):
        log.error("detected system native gcc version {}.{}.{}"
                  .format(ver[0], ver[1], ver[2]))
        script.abort("please use a version later than 5.4 and earlier than 8.0")


"""
 " Git must be sufficiently configured for repo to work.
"""
def check_git_config():
    log.info("checking git config")
    (_, cfg, _)  = sh.call(["git", "config", "-l"])
    for setting in ["user.name", "user.email", "color.diff"]:
        if not setting in cfg:
            log.error("git is not correctly configured")
            log.error("please ensure the following git configs are set:")
            log.error("")
            log.error("git config --global user.name \"Joe Bloggs\"")
            log.error("git config --global user.email \"jb@example.com\"")
            log.error("git config --global color.diff \"auto\"")
            script.abort()


"""
 " Generate a list of all files and folders in <workspace>.
"""
def get_ws_files():
    filelist = []
    for (_, dirs, files) in os.walk(sh.cwd):
        dirs = [d+"/" for d in dirs]
        filelist += sorted(files + dirs)
        break  # don't recursively walk
    log.debug("found the following files in workspace directory:")
    log.debug(filelist)
    return filelist


"""
 " Get sorted list of tags available for a platform
 " Only available for platforms with special mrel="???"
"""
def get_tags( p ):
    if not dblu("@.mrel",p) == "???":
        script.abort("get_tags() called on platform without mrel='???' ({})".format(p))

    arp_git = "git.linaro.org/landing-teams/working/arm/arm-reference-platforms.git"
    tagkey = dblu("@.tagkey", p)
    os.chdir(sys.path[0])

    def not_in_arp_git_error():
        log.error("workspace sync script is not in a git clone of Arm Reference Platforms")
        log.error("to build from source you need to `git clone {}`".format(arp_git))
        log.error("you *can* run `python3 /path/to/sync_workspace.py` from another directory")
        log.error("but sync_workspace.py itself must reside in a git clone of Arm Reference Platforms")
        script.abort()

    (ret, _, _) = sh.call(["git", "status"])
    if not (ret == 0):
        not_in_arp_git_error()

    (_, remotes, _) = sh.call(["git", "remote", "-v"])
    if not arp_git in remotes:
        not_in_arp_git_error()

    for remote in remotes.splitlines():
        (name, url, direction) = remote.split()
        if arp_git in url and direction == "(fetch)":
            sh.call(["git", "remote", "update", name, "--prune"])
            break

    (_, tags, _) = sh.call(["git", "for-each-ref", "--sort=creatordate", "refs/tags", '--format="%(refname)"'])
    tags = list(filter(lambda t: tagkey in t, tags.replace('"', "").splitlines()))
    tags = [t[t.find(tagkey):] for t in tags]

    os.chdir(sh.cwd)
    return tags


"""
 " Check whether <workspace> is empty and, if not, confirm with user whether
 " it's OK to delete these files/folders and proceed.
"""
def check_empty_ws():
    filelist = get_ws_files()
    if len(filelist) > 0:
        # The directory may be non-empty because we're initialising the workspace
        # inside the cloned arm-reference-platforms/ directory.
        preserve = [
            sh.filename, sh.dld, sh.repod,
            ".git/", "docs/", "log.txt", "readme.rst",
        ]
        for f in preserve:
            if f in filelist:
                filelist.remove(f)

        # If we still have files in the list then we need to check with the user.
        if len(filelist) > 0:
            log.warn("designated workspace is non-empty")
            msg = "Found the following files/folders in your workspace:\n\n - "
            msg += "\n - ".join(filelist)
            msg += "\n\n## Delete these files/folders and proceed?"
            if not prompt(msg, [choice("Yes", True), choice("No", False)]).meta:
                sys.exit(0)
            [sh.rmdir(f) if f.endswith("/") else sh.rm(f) for f in filelist]


"""
 " Decide which software configuration will be downloaded.
"""
class config:
    def query():
        while not config._choose():
            pass


    def sync():
        print("\nFetching and extracting dependencies...\n")
        for d in config.deps:
            sh.fetch(d, plat=config.p.meta)
        if config.manifest:
            force_fresh = False
            finished = False
            arm_build = dblu("@.build", config.p.meta) == "arm"
            while not finished:
                sh.reposync( config.manifest, config.p.meta, config.mrel, force_fresh )
                if not arm_build:
                    finished = True
                else:
                    ### Get list of platform script directories
                    bsgroup = dblu("@.bsgroup", config.p.meta)
                    for (_, dirs, _) in os.walk("build-scripts/"+bsgroup):
                        break  # don't recursively walk

                    ### Get list of filesystem scripts
                    for (_, _, files) in os.walk("build-scripts/filesystems"):
                        break  # don't recursively walk


                    ### If something goes wrong during repo sync (e.g. losing internet connection),
                    ### the build-scripts/platforms and build-scripts/filesystems directories are
                    ### usually either missing or empty, so we can use these as a litmus test for
                    ### a corrupted workspace
                    ok = True
                    try:
                        if not dirs or not files:
                            ok = False
                    except UnboundLocalError:
                        ok = False

                    if ok:
                        ### Cull any scripts/directories not matching chosen config, enabling user to run
                        ### `./build-scripts/build-all.sh all` without needing to pass the platform/filesystem
                        for d in dirs:
                            if not (d=="common" or d==dblu(config.p.meta+".pdir")):
                                sh.rmdir("build-scripts/{}/{}".format(bsgroup, d))
                        preserve = dblu(config.fs.meta+".script") if config.env.meta=="k" else dblu(config.fw.meta+".stubfs")
                        for f in files:
                            if not f==preserve:
                                sh.rm("build-scripts/filesystems/"+f)
                        finished = True
                    else:
                        log.error("detected missing files/folders in build-scripts/ directory")
                        log.error("repo may be in an invalid/corrupt state")
                        log.error("did you lose internet connection during sync?")
                        msg = "Detected potential invalid/corrupt repo state, try to sync again?"
                        if not prompt(msg, [choice("Yes", True), choice("No", False)]).meta:
                            sys.exit(1)
                        [sh.rmdir(f) if f.endswith("/") else sh.rm(f) for f in get_ws_files()]
                        force_fresh = True
        hooks = dblu("@.pihooks", config.p.meta, noneAllowed=True)
        if hooks:
            [pihooks.__dict__[h]() for h in hooks]
        print("\nWorkspace initialised.")
        if config.ws.meta=="bfs":
            if arm_build:
                print("\nTo build:\n")
                print("    chmod a+x <workspace>/build-scripts/build-all.sh")
                print("    <workspace>/build-scripts/build-all.sh all")
                print("\nResulting binaries will be placed in:")
                print("\n    <workspace>/output/{}-{}/".format(
                          dblu("@.pdir", config.p.meta),
                          dblu(config.fs.meta+".script" if config.env.meta=="k" \
                              else config.fw.meta+".stubfs", config.p.meta)))
        print("\nFor more information, see the docs here:")
        print("\n    {}".format(dblu('@.docs', config.p.meta)))
        print("\nVisit our forums for platforms & open source discussions:")
        print("\n    https://community.arm.com/oss-platforms/f")
        print("\nThank you for using Arm Reference Platforms.")


    def _choose():
        config.cfg = []
        config.deps = []
        config.swcs = []
        config.excludes = []
        config.manifest = None
        config._add_cfg("Workspace", sh.cwd)
        config._choose_p()
        config._choose_ws()
        if config.ws.meta=="bfs":
            check_platform_deps(config.p.meta)
            check_git_config()
            check_sys_gcc()
            config._add_deps(config.p.meta)
            config._choose_env()
            if config.env.meta=="k":
                config._choose_k()
                config._choose_fs()
            elif config.env.meta=="fw":
                config._choose_fw()
        elif config.ws.meta=="pbc":
            config._choose_pb()
        msg = "Your chosen configuration is shown below:\n"
        pad = [max([len(row[n]) for row in config.cfg]) for n in [0,1]]
        wall = "\n    +-"+(pad[0]*"-")+"-+-"+(pad[1]*"-")+"-+"
        msg += wall
        for row in config.cfg:
            msg += "\n    | {:<{:}} | {:<{:}} |" \
                   .format(row[0], pad[0], row[1], pad[1])
        msg += wall
        if config.swcs:
            config.excludes = set(config.excludes)
            config.swcs = [x for x in config.swcs if x not in config.excludes]
            config.swcs = sorted(list(set(config.swcs)),
                        key = lambda swc: dblu(swc+".priority", config.p.meta))
            rows = []
            for swc in config.swcs:
                name = dblu(swc+".name", config.p.meta)
                rows.append(name)
            pad = max([len(r) for r in rows])
            wall = "\n    +-"+(pad*"-")+"-+"
            msg += "\n\nThe following software components are included:\n"
            msg += wall
            for r in rows:
                msg += "\n    | {:<{:}} |".format(r, pad)
            msg += wall
        msg += "\n\n## Proceed with this configuration?"
        return prompt(msg, [choice("Yes", True), choice("No", False)]).meta


    def _add_cfg( key, val ):
        config.cfg.append((key, val))


    def _add_deps(key):
        deps = dblu(key+".deps", config.p.meta, noneAllowed=True)
        if deps:
            for d in deps:
                config.deps.append(d)


    def _add_swc(key):
        config.swcs.append(key)
        config._update_includes(key)


    def _update_includes(key):
        incls, excls = dblum(key, ["includes", "excludes"], config.p.meta, True)
        if incls:
            for i in incls:
                config.swcs.append(i)
                config._update_includes(i)
        if excls:
            config.excludes += excls


    def _choose_p():
        log.debug("Building platform choice tree")
        def crawl(root):
            log.debug("crawl({})".format(root.meta))
            num_en_children = 0
            if root.children:
                log.debug("{} is non-leaf".format(root.meta))
                [crawl(c) for c in root.children]
                num_en_children = sum([not p.disabled for p in root.children])
                log.debug("{} has {} enabled children"
                          .format(root.meta, num_en_children))
            pbs = dblu(root.meta+".pb", noneAllowed=True)
            num_pbs = len(pbs) if pbs else 0
            if not root.children:
                log.debug("{} has {} prebuilts".format(root.meta, num_pbs))
            can_init_ws = True
            if num_pbs==0 and not HOST=="Linux":
                can_init_ws = False
                if not root.children:
                    log.debug("not running on Linux")
            log.debug("can_init_ws {}? {}".format(root.meta, can_init_ws))
            if (root.children and num_en_children==0) or not can_init_ws:
                log.debug("disabling node {}".format(root.meta))
                root.disabled = True
                root.descr = "can only build from source for this platform, " \
                             "which requires a Linux host PC"
        ptree = choice.tree(dblu("p.all"), root="p")
        crawl(ptree)
        config.p = tree_prompt("Please select a platform", ptree)
        config._add_cfg("Platform", config.p.name)
        config._update_includes(config.p.meta)


    def _choose_ws():
        (ks,fws,pbs) = dblum(config.p.meta,["k","fw","pb"],config.p.meta,True)
        root = choice("<ws>", meta="ws")
        if (ks or fws) and HOST=="Linux":
            root.add(choice("Build from source", meta="bfs"))
        if pbs:
            root.add(choice("Use prebuilt configuration", meta="pbc"))
        config.ws = tree_prompt("Please specify whether you want to", root)
        config._add_cfg("Type", config.ws.name)


    def _choose_env():
        (ks, fws) = dblum(config.p.meta, ["k","fw"], config.p.meta, True)
        root = choice("<env>", meta="env")
        if ks:
            root.add(choice(dblu("k.name"), meta="k"))
        if fws:
            root.add(choice(dblu("fw.name"), meta="fw"))
        config.env = tree_prompt("Please select an environment", root)


    def _choose_fw():
        p = config.p.meta
        fwtree = choice.tree(dblu(p+".fw", p), "fw", p)
        config.fw = tree_prompt("Please select your firmware", fwtree)
        config._add_cfg("Configuration", config.fw.name)
        config._add_deps(config.fw.meta)
        config._add_swc(config.fw.meta)
        config._update_includes(config.fw.meta)
        config.manifest = dblu(config.fw.meta+".manifest", config.p.meta)
        config._choose_mrel()


    def _choose_k():
        p = config.p.meta
        ktree = choice.tree(dblu(p+".k", p), "k", p)
        config.k = tree_prompt("Please select your kernel", ktree)
        config._add_deps(config.k.meta)
        config._add_swc(config.k.meta)
        config._update_includes(config.k.meta)
        if not dblu(config.k.meta+".maps", noneAllowed=True):
            config.manifest = dblu(config.k.meta+".manifest", config.p.meta)
        config._choose_mrel()


    def _choose_mrel():
        (murl, mrel, tagkey, knowntag) = dblum("@", ["murl", "mrel", "tagkey", "knowntag"], config.p.meta, noneAllowed=True)
        if mrel == "???":
            choices = []
            disabled_descr = "please `git checkout {}` to sync this release"
            tags = get_tags(config.p.meta)
            for tag in tags:
                choices.append(choice(
                    name=tag,
                    meta="refs/tags/"+tag,
                    descr=(None if tag==knowntag else disabled_descr.format(tag)),
                    disabled=(not tag==knowntag)
                ))
            show_menu = True
            try:
                knowntag_index = tags.index(knowntag) if not knowntag is None else len(tags)-1
            except ValueError:
                if script.force_unknown_tag:
                    config.mrel = "refs/tags/"+knowntag
                    show_menu = False
                else:
                    log.error("platform {} specifies knowntag {} but this could not be found".format(config.p.meta, knowntag))
                    log.error("has arm-reference-platforms been tagged with {} yet?".format(knowntag))
                    log.error("you can temporarily override this error using '--force_unknown_tag'")
                    script.abort()
            if show_menu:
                master_disabled_descr = "master is only available for the latest release, please `git checkout {}`".format(tags[-1])
                choices.append(choice(
                    name="master",
                    meta="master",
                    descr=(None if knowntag_index==len(tags)-1 else master_disabled_descr),
                    disabled=(not knowntag_index==len(tags)-1)
                ))
                mrel = prompt("Please select a manifest release tag to checkout", choices)
                config.mrel = mrel.meta
        else:
            config.mrel = "refs/tags/"+mrel
        config._add_cfg("Release", config.mrel)


    def _choose_fs():
        plat_fss = dblu(config.p.meta+".fs", config.p.meta)
        maps = dblu(config.k.meta+".maps", noneAllowed=True)
        kernel_fss = maps.keys() if maps else \
            dblu(config.k.meta+".fs", config.p.meta)
        fss = [fs for fs in kernel_fss if fs in plat_fss]
        fstree = choice.tree(fss, "fs", config.p.meta)
        config.fs = tree_prompt("Please select your filesystem", fstree)
        config._add_cfg("Configuration", "{} + {}".format(config.k.name, config.fs.name))
        config._add_deps(config.fs.meta)
        config._add_swc(config.fs.meta)
        config._update_includes(config.fs.meta)
        if maps:
            config.manifest = maps[config.fs.meta]


    def _choose_pb():
        choices = []
        for pb in dblu(config.p.meta+".pb", config.p.meta):
            choices.append(choice(dblu(pb+".name", config.p.meta), pb))
        if len(choices)==1:
            config.pb = choices[0]
            log.warn("only avail. option is "+config.pb.name)
        else:
            choices.append(choice("<< all >>", meta="all"))
            config.pb = prompt("Please select a configuration", choices)
        config._add_cfg("Configuration", config.pb.name)
        if config.pb.meta=="all":
            all_pb_deps = []
            for pb in dblu(config.p.meta+".pb", config.p.meta):
                pb_deps = dblu(pb+".deps", config.p.meta, noneAllowed=True)
                if pb_deps:
                    for d in pb_deps:
                        all_pb_deps.append(d)
            config.deps += list(set(all_pb_deps))
            config.swcs = []
        else:
            config._add_deps(config.pb.meta)
            config._update_includes(config.pb.meta)


def run():
    config.query()
    config.sync()
    return 0


def run_qa():
    check_empty_ws()
    script.start_qa()
    manifests = []
    for p in dblu("p.all"):
        log.info(">>> Running QA for platform "+p)
        (ks,fws,fss,pbs) = dblum(p,["k","fw","fs","pb"], p, noneAllowed=True)
        if ks:
            [manifests.append(dblu(k+".manifest", plat=p)) for k in ks]
        if fws:
            [manifests.append(dblu(fw+".manifest", plat=p)) for fw in fws]
        keys = (fss if fss else []) + (pbs if pbs else [])
        if keys:
            for k in keys:
                deps = dblu(k+".deps", plat=p, noneAllowed=True)
                if deps:
                    [sh.fetch(d, plat=p, force_fresh=True) for d in deps]
    """
     " TODO: re-add support for QA run manifest reposync incl. tags
    for m in list(set(manifests)):
        log.info(">>> Attempting to sync manifest "+m)
        sh.reposync(m, "p", force_fresh=True)
    """
    return script.end_qa()


if __name__ == "__main__":
    script.init()
    exit(run() if not script.qa_mode else run_qa())
