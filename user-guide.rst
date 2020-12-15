User Guide
==========

.. section-numbering::
    :suffix: .

.. contents::

Introduction
------------

The Neoverse N1 System Development Platform (N1SDP) is an enterprise class reference board based on
the Neoverse N1 core.

This document is a guide on how to fetch, build from source, and run an Arm Reference Platforms
software stack on N1SDP, including a Linux distribution based on either the `Yocto project`_'s Poky
Linux, or on Ubuntu Server.

The synced workspace includes:

 * Scripts to build the board firmware, Linux kernel, and Ubuntu Server distro image
 * Yocto `Bitbake`_ layers for building the Board Support Package (BSP) and Poky Linux distro
 * Other supporting board files and prebuilt binaries.

Prerequisites
-------------

These instructions assume that:
 * Your host PC is running Ubuntu Linux 18.04 LTS and should have at least 50GB free storage space
 * You are running the provided scripts in a ``bash`` shell environment.

The following utilities must be available on your host PC:
 * chrpath
 * compression library
 * diffstat
 * gawk
 * makeinfo
 * openssl headers
 * pip
 * repo
 * yocto

To ensure that all the required packages are installed, run:

::

    sudo apt-get update
    sudo apt-get install chrpath gawk texinfo libssl-dev diffstat wget git-core unzip gcc-multilib \
     build-essential socat cpio python python3 python3-pip python3-pexpect xz-utils debianutils \
     iputils-ping python3-git python3-jinja2 libgl1-mesa-dev libsdl1.2-dev pylint3 xterm git-lfs \
     openssl curl libncurses-dev libz-dev python-pip

**Install repo tool**

Follow the instructions provided in the `repo README file`_ to install the ``repo tool``.

NOTE: The repo tool which gets installed using apt-get command sometimes return errors, in such a case its recommended to install repo using the ``curl`` method.

Syncing and building the source code
------------------------------------

The N1SDP software stack supports two software distributions:
 * Poky Linux, a minimal BusyBox-like environment
 * Ubuntu Server.

The instructions below provide the necessary steps to sync and build these distributions.

First, create a new folder that will be your workspace and will henceforth be referred to as
``<n1sdp_workspace>`` in these instructions:

::

    mkdir <n1sdp_workspace>
    cd <n1sdp_workspace>
    export N1SDP_RELEASE=refs/tags/N1SDP-2020.12.15

NOTE: Sometimes new features and additional bug fixes will be made available in the git repositories
and will not yet have been tagged as part of a release. To pickup these latest changes you can drop
the ``-b <release tag>`` option from the ``repo init`` commands below, however please be aware that
such untagged changes have not yet been formally verified and should be considered unstable until
they are tagged in an official release.

To sync BSP without Ubuntu
##########################

Choose this option if you intend to run the provided Poky Linux distro, or your own alternative
software solution.

To sync a specific tagged release::

    repo init -u https://git.linaro.org/landing-teams/working/arm/arm-reference-platforms-manifest.git -m n1sdp-v2.xml -g bsp -b ${N1SDP_RELEASE}
    repo sync -j$(nproc)

Or to sync the latest untagged features and bug fixes::

    repo init -u https://git.linaro.org/landing-teams/working/arm/arm-reference-platforms-manifest.git -m n1sdp-v2.xml -g bsp
    repo sync -j$(nproc)

To sync both the BSP and Ubuntu
###############################

Choose this option if you intend to run the provided Ubuntu Server distro.

To sync a specific tagged release::

    repo init -u https://git.linaro.org/landing-teams/working/arm/arm-reference-platforms-manifest.git -m n1sdp-v2.xml -g ubuntu -b ${N1SDP_RELEASE}
    repo sync -j$(nproc)

Or to sync the latest untagged features and bug fixes::

    repo init -u https://git.linaro.org/landing-teams/working/arm/arm-reference-platforms-manifest.git -m n1sdp-v2.xml -g ubuntu
    repo sync -j$(nproc)

To build the BSP and Poky Linux distro
######################################

Mandatory for *all* users.

::

    cd <n1sdp_workspace>/bsp
    export DISTRO="poky"
    export MACHINE="n1sdp"
    source setup-environment
    bitbake core-image-base

The initial clean build is expected to take a long time, as all host tools and utilities are built
from source before the target images. This includes host executables (python, cmake, etc.) and the
required toolchain(s).

Once the build is successful, all images will be placed in the
``<n1sdp_workspace>/bsp/build-poky/tmp-poky/deploy/images/n1sdp`` directory.

To build the Ubuntu Server distro
#################################

Only required if intending to run the provided Ubuntu Server distro.

The Ubuntu Server distro image is built using the script provided in
``<n1sdp_workspace>/ubuntu/build-scripts``.

::

    cd <n1sdp_workspace>/ubuntu
    ./build-scripts/build-ubuntu.sh

    Options that can be passed to script are:
    <path to build-ubuntu.sh> [OPTIONS]
    OPTIONS:
    cleanall           remove all the sources fetched during previous build, removing all binaries from sub folders.
    clean              remove all binaries from sub folders generated in previous build.
    build              build linux, linux-firmware, busybox, grub binaries and Ubuntu distribution image
    package            package all the above listed components into one single Ubuntu grub image

    NOTE: If no option specified then script will execute cleanall, build and package.
          The final image grub-ubuntu.image can be located in ubuntu/output/n1sdp


Provided components
-------------------

Within the Yocto project, each component included in the N1SDP software stack is specified as
a `Bitbake`_ recipe. The N1SDP recipes are located at ``<n1sdp_workspace>/bsp/layers/meta-arm/``.

**Steps for baking Images from unstaged source code**

Yocto allows modifying the fetched source code of each recipe component in the
workspace, by applying patches. This is however not a convenient approach for
developers, since creating patches and updating recipes is time-consuming.
To make that easier, Yocto provides the devtool utility. devtool creates a
new workspace, in which you can edit the fetched source code and bake images
with the modifications

::

    cd <n1sdp_workspace>/bsp
    MACHINE=n1sdp DISTRO=poky . ./conf/setup-environment
    # create a workspace for a given recipe component
    # recipe-component-name can be of:
    # trusted-firmware-a / scp-firmware / grub-efi / linux-linaro-arm
    devtool modify <recipe-component-name>
    # This creates a new workspace for recipe-component-name and fetches source code
    # into "build-poky/workspace/sources/{trusted-firmware-a,scp-firmware,edk2-firmware,grub-efi,linux-linaro-arm}"
    # edit the source code in the newly created workspace
    # build images with changes on workspace
    # recipe-component-name can be of: scp-firmware / edk2-firmware / grub-efi / linux-linaro-arm
    bitbake <recipe-component-name>

NOTE : edk2-firmware cannot be built using devtool, kindly refer to the bug report on `bugzilla`_ for more details.

Software Components
###################

Trusted Firmware-A
******************

Based on `Trusted Firmware-A`_.

+--------+----------------------------------------------------------------------------------------------------------------+
| Recipe | <n1sdp_workspace>/bsp/layers/meta-arm/meta-arm-bsp/recipes-bsp/trusted-firmware-a/trusted-firmware-a-n1sdp.inc |
+--------+----------------------------------------------------------------------------------------------------------------+
| Files  | * <n1sdp_workspace>/bsp/build-poky/tmp-poky/deploy/images/n1sdp/bl31-n1sdp.bin                                 |
+--------+----------------------------------------------------------------------------------------------------------------+


System Control Processor (SCP)
******************************

Based on `SCP Firmware`_.

+--------+----------------------------------------------------------------------------------------------------+
| Recipe | <n1sdp_workspace>/bsp/layers/meta-arm/meta-arm-bsp/recipes-bsp/scp-firmware/scp-firmware-n1sdp.inc |
+--------+----------------------------------------------------------------------------------------------------+
| Files  | * <n1sdp_workspace>/bsp/build-poky/tmp-poky/deploy/images/n1sdp/scp_ramfw.bin                      |
|        | * <n1sdp_workspace>/bsp/build-poky/tmp-poky/deploy/images/n1sdp/scp_romfw.bin                      |
|        | * <n1sdp_workspace>/bsp/build-poky/tmp-poky/deploy/images/n1sdp/mcp_ramfw.bin                      |
|        | * <n1sdp_workspace>/bsp/build-poky/tmp-poky/deploy/images/n1sdp/mcp_romfw.bin                      |
+--------+----------------------------------------------------------------------------------------------------+


uefi edk2
*********

Based on `UEFI edk2`_.

+--------+---------------------------------------------------------------------------------------------+
| Recipe | <n1sdp_workspace>/bsp/layers/meta-arm/meta-arm-bsp/recipes-bsp/uefi/edk2-firmware-n1sdp.inc |
+--------+---------------------------------------------------------------------------------------------+
| Files  | * <n1sdp_workspace>/bsp/build-poky/tmp-poky/deploy/images/n1sdp/uefi.bin                    |
+--------+---------------------------------------------------------------------------------------------+


Linux
*****

Based on `Linux 5.4 for N1SDP`_.

+--------+-------------------------------------------------------------------------------------------------+
| Recipe | <n1sdp_workspace>/bsp/layers/meta-arm/meta-arm-bsp/recipes-kernel/linux/linux-linaro-arm_5.4.bb |
+--------+-------------------------------------------------------------------------------------------------+
| Files  | * <n1sdp_workspace>/bsp/build-poky/tmp-poky/deploy/images/n1sdp/Image                           |
+--------+-------------------------------------------------------------------------------------------------+


Poky Linux distribution
***********************

The layer is based on the `Poky`_ Linux distro, which is itself based on BusyBox and built using
glibc.

+--------+---------------------------------------------------------------------------------------------------+
| Recipe | <tc0_workspace>/bsp/layers/openembedded-core/meta/recipes-core/images/core-image-base.bb          |
+--------+---------------------------------------------------------------------------------------------------+
| Files  | * <tc0_workspace>/bsp/build-poky/tmp-poky/deploy/images/n1sdp/core-image-base-n1sdp.wic           |
+--------+---------------------------------------------------------------------------------------------------+


Ubuntu Linux distribution
*************************

Ubuntu is built as a separate project using the ``build-scripts/``, then booted using the BSP built
by Yocto. The generated distro image is placed at ``output/n1sdp/grub-ubuntu.img``.


Running the software distribution on N1SDP
------------------------------------------

This section provides steps for:
 * Setting up the N1SDP with the required board firmware
 * Preparing a bootable disk
 * Boot the supported software distributions (Poky Linux or Ubuntu Server).

Setting up the N1SDP
####################

After powering up or rebooting the board, any firmware images placed on the board's microSD will be
flashed into either on-board QSPI flash copied into DDR3 memory via the IOFPGA.

**Configure COM Ports**

Connect a USB-B cable between your host PC and N1SDP's DBG USB port, then power ON the board. The
DBG USB connection will enumerate as four virtual COM ports assigned to the following processing
entities, in order

       ::

               COM<n>   - Motherboard Configuration Controller (MCC)
               COM<n+1> - Application Processor (AP)
               COM<n+2> - System Control Processor (SCP)
               COM<n+3> - Manageability Control Processor (MCP)

Please check Device Manager in Windows or ``ls /dev/ttyUSB*`` in Linux to identify <n>.

Use a serial port application such as *PuTTy* or *minicom* to connect to all virtual COM ports with
the following settings:

      ::

               115200 baud
               8-bit word length
               No parity
               1 stop bit
               No flow control

Note: Some serial port applications refer to this as "115200 8N1" or similar.

Before running the deliverables on N1SDP, ensure both BOOT CONF switches are in the OFF position,
then issue the following command in the MCC console:

    Cmd> USB_ON

This will mount the on-board microSD card as a USB Mass Storage Device on the host PC with the name
"N1SDP".

Enter the following command on the MCC console window to ensure time is correctly set. This is
required in order for the first distro boot to succeed:

      ::

             Cmd> debug
             Debug> time
             Debug> date
             Debug> exit

Update firmware on microSD card
###############################

The board firmware files are located in ``<n1sdp_workspace/bsp/build-poky/tmp-poky/deploy/images/n1sdp/>``
after the BSP source build.

Single chip mode::

    n1sdp-board-firmware_primary.tar.gz    : firmware to be copied to microSD of N1SDP board in single chip mode.

Multi chip mode::

    n1sdp-board-firmware_primary.tar.gz    : firmware to be copied to microSD of primary board.
    n1sdp-board-firmware_secondary.tar.gz  : firmware to be copied to microSD of secondary board.

There are two methods for populating the microSD card:
   1. The microSD card from the N1SDP can be removed from N1SDP and can be mounted on a host machine
      using a card reader,
   2. The USB debug cable when connected to host machine will show the microSD partition on host
      machine which can be mounted.

      ::

             $> sudo mount /dev/sdx1 /mnt
             $> sudo rm -rf /mnt/*
             $> sudo tar --no-same-owner -xzf n1sdp-board-firmware_primary.tar.gz -C /mnt/
             $> sudo umount /mnt```

NOTE: replace ``sdx1`` with the device and partition of the SD card.

Option (2) above is typically preferred, as removing the microSD card requires physical access to
the motherboard inside the N1SDP's tower case.

Firmware tarball contains iofpga configuration files, SCP, TF-A, and UEFI binaries.

**NOTE**:
Please ensure to use the recommended PMIC binary. Refer to page `potential-damage`_ for more info.

If a PMIC binary mismatch is detected, a warning message is printed in the MCC console recommending
the user to switch to appropriate PMIC image. On MCC recommendation *ONLY*, please update the
``MB/HBI0316A/io_v123f.txt`` file on the microSD using the below commands.

Example command to switch to 300k_8c2.bin from the host PC::

      ::

             $> sudo mount /dev/sdx1 /mnt
             $> sudo sed -i '/^MBPMIC: pms_0V85.bin/s/^/;/g' /mnt/MB/HBI0316A/io_v123f.txt
             $> sudo sed -i '/^;MBPMIC: 300k_8c2.bin/s/^;//g' /mnt/MB/HBI0316A/io_v123f.txt
             $> sudo umount /mnt


Boot Poky on N1SDP
##################

**Preparing a bootable Poky disk**

A bootable disk (USB stick or SATA drive) can be prepared by flashing the image generated from the
source build. The image will be available at the location
``<n1sdp_workspace/bsp/build-poky/tmp-poky/deploy/images/n1sdp/core-image-base-n1sdp.wic>``.

This is a bootable GRUB wic image comprising Linux kernel and Poky distro. The partitioning and
packaging is performed during the build based on the wks file located at
``<n1sdp_workspace/bsp/layers/meta-arm/meta-arm-bsp/wic/n1sdp-efidisk.wks>``.

Use the following commands to burn the GRUB image to a USB stick or SATA drive:

        ::

             $ lsblk
             $ sudo dd if=core-image-base-n1sdp.wic of=/dev/sdx conv=fsync bs=1M
             $ sync

Note: Replace ``/dev/sdx`` with the handle corresponding to your USB stick or SATA drive, as
identified by the ``lsblk`` command.

**Booting the board with Poky image**

Insert the bootable disk created earlier. Shutdown and reboot the board by issuing the following
commands to the MCC console:

    ::

             Cmd> SHUTDOWN
             Cmd> REBOOT

Enter the UEFI menu by pressing Esc on the AP console as the edk2 logs start appearing; from here,
enter the UEFI Boot Manager menu and then select the burned disk.

By default the Linux kernel will boot with ACPI, though Device Tree can also be specified::

            *ARM reference image boot on N1SDP (ACPI)
             ARM reference image boot on Single-Chip N1SDP (Device Tree)
             ARM reference image boot on Multi-Chip N1SDP (Device Tree)

The system will boot into a base image environment of Poky Linux.

The N1SDP login password is *root*

Boot Ubuntu on N1SDP
####################

**Preparing a bootable Ubuntu disk**

A bootable disk (USB stick or SATA drive) can be prepared by formatting it with the distro image
created during source build. The image will be available at the location location
``<n1sdp_workspace/ubuntu/output/n1sdp/grub-ubuntu.img>``.

This is a bootable GRUB image comprising Linux kernel and an Ubuntu Server 18.04 file system. The
partitioning and packaging is performed during the build.

Use the following commands to burn the GRUB image to a USB stick or SATA drive:

        ::

             $ lsblk
             $ sudo dd if=grub-ubuntu.img of=/dev/sdX bs=1M
             $ sync

Note: Replace ``/dev/sdX`` with the handle corresponding to your USB stick or SATA drive, as
identified by the ``lsblk`` command.

**Booting the board with Ubuntu image**

Insert the bootable disk created earlier and connect the ethernet cable to a working internet
connection. This is *REQUIRED* on first boot in order to successfully download and install necessary
Ubuntu packages. Installation will fail if an internet connection is not available.

Shutdown and reboot the board by issuing the following commands to the MCC console:

    ::

             Cmd> SHUTDOWN
             Cmd> REBOOT


Enter the UEFI menu by pressing Esc on the AP console as the edk2 logs start appearing; from here,
enter the UEFI Boot Manager menu and then select the burned disk.

Ubuntu 18.04 will boot in two stages; the first boot is an installation pass, after which a second
boot is required to actually enter the Ubuntu Server environment.

To reboot the board after the first boot installation pass has completed, from MCC console:

    ::

             Cmd> REBOOT

The system will boot into a minimal Ubuntu 18.04 environment.

Login as user ``root`` with password *root*, and install any desired packages from the console::

            # apt-get install <package-name>

Building Kernel Modules Natively
********************************

Native building of kernel modules typically requires kernel headers to be installed on the platform.
However, a bug in deb-pkg currently causes host executables to be packed rather than the target
executables.

This can be worked around by building and installing the kernel natively on the platform.

Boot the N1SDP board with Ubuntu filesystem and login as root.

    ::

        apt-get install -y git build-essential bc bison flex libssl-dev
        git clone -b n1sdp http://git.linaro.org/landing-teams/working/arm/kernel-release.git
        git clone http://git.linaro.org/landing-teams/working/arm/n1sdp-pcie-quirk.git
        cd kernel-release/
        git am ../n1sdp-pcie-quirk/linux/\*.patch
        mkdir out
        cp -v /boot/config-5.4.0+  out/.config
        make O=out -j4
        make O=out modules_install
        make O=out install
        update-grub
        sync

Reboot the board and when Grub menu appears, select the Advanced Boot Options -> 5.4.0 kernel for
booting.

.. _potential-damage: https://community.arm.com/developer/tools-software/oss-platforms/w/docs/604/notice-potential-damage-to-n1sdp-boards-if-using-latest-firmware-release
.. _Yocto project: https://www.yoctoproject.org
.. _Bitbake: https://www.yoctoproject.org/docs/1.6/bitbake-user-manual/bitbake-user-manual.html
.. _Trusted Firmware-A: https://trustedfirmware-a.readthedocs.io/en/latest/
.. _SCP Firmware: https://github.com/ARM-software/SCP-firmware
.. _UEFI edk2: https://github.com/tianocore/edk2
.. _Linux 5.4 for N1SDP: https://git.linaro.org/landing-teams/working/arm/kernel-release.git
.. _Poky: https://www.yoctoproject.org/software-item/poky
.. _repo README file: https://gerrit.googlesource.com/git-repo/+/refs/heads/master/README.md
.. _bugzilla: https://bugzilla.yoctoproject.org/show_bug.cgi?id=14141

----------

*Copyright (c) 2020, Arm Limited. All rights reserved.*
