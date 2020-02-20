User Guide
==========

.. section-numbering::
    :suffix: .

.. contents::

Notice
------
The Cortex-A5 DesignStart software stack uses the `Yocto project <https://www.yoctoproject.org/>`__ to build
a Linux distribution suitable for the DesignStart platform. The yocto project relies on the
`Bitbake <https://www.yoctoproject.org/docs/1.6/bitbake-user-manual/bitbake-user-manual.html>`__
tool as its build tool.

Prerequisites
-------------
These instructions assume your host PC is running Ubuntu Linux 18.04 LTS.
The instructions in this document expects that you are using a bash shell.

The following prerequisites must be available on the host system:
 * chrpath
 * gawk
 * makeinfo
 * openssl headers
 * diffstat
 * yocto

To resolve these dependencies, run:

::

    sudo apt-get update
    sudo apt-get install chrpath gawk texinfo libssl-dev diffstat wget git-core unzip gcc-multilib \
     build-essential socat cpio python python3 python3-pip python3-pexpect xz-utils debianutils \
     iputils-ping python3-git python3-jinja2 libegl1-mesa libsdl1.2-dev pylint3 xterm git-lfs openssl \
     curl libncurses-dev libz-dev python-pip


Provided components
-------------------
Within the Yocto project, each component included in the CA5DS software stack is specified as
a `bitbake recipe <https://www.yoctoproject.org/docs/1.6/bitbake-user-manual/bitbake-user-manual.html#recipes>`__.
The recipes specific to the CA5DS project may be located at:
``<ca5ds_workspace>/layers/meta-arm/meta-designstart``.

Software
########

Trusted Firmware-A
******************
Based on `ARM Trusted Firmware-A <https://github.com/ARM-software/arm-trusted-firmware>`__.

+--------+--------------------------------------------------------------------------+
| Recipe | <ca5ds_workspace>/layers/meta-arm/arm/recipes-bsp/trusted-firmware-a     |
+--------+--------------------------------------------------------------------------+
| Files  | * a5ds.fip                                                               |
+--------+--------------------------------------------------------------------------+

U-Boot
******
The recipe responsible for building u-boot.
The layer is based on linaro `U-Boot <https://git.linaro.org/landing-teams/working/arm/u-boot.git/>`__.

+--------+--------------------------------------------------------------------------+
| Recipe | <ca5ds_workspace>/layers/meta-arm/arm/recipes-bsp/u-boot                 |
+--------+--------------------------------------------------------------------------+
| Files  | * u-boot.bin                                                             |
+--------+--------------------------------------------------------------------------+

Linux
*****
The recipe responsible for building a version of Linux.
The layer is based on the `poky-tiny <https://wiki.yoctoproject.org/wiki/Poky-Tiny>`__
distribution which is a Linux distribution stripped down to a minimal configuration.

The provided distribution is based on busybox and built using muslibc.

+--------+--------------------------------------------------------------------------+
| Recipe | <ca5ds_workspace>/layers/meta-arm/arm/recipes-kernel/linux               |
+--------+--------------------------------------------------------------------------+
| Files  | * zImage                                                                 |
|        | * iota-tiny-image-a5ds.cpio.gz (rootfs)                                  |
+--------+--------------------------------------------------------------------------+

Run scripts
###########

Within ``<ca5ds_workspace>/run-scripts/`` a number of convenience functions for testing the software
stack may be found.
Usage descriptions for the various scripts are provided in the following sections.


Building the Software stack
---------------------------
CA5DS is a Bitbake based Yocto distro which uses bitbake commands to build the stack.
In the top directory of the synced workspace (~/ca5ds), run:

::

    export DISTRO="iota-tiny"
    export MACHINE="a5ds"
    source setup-environment

By sourcing setup-environment, your current directory should now have switched to
``<ca5ds_workspace>/build-iota-tiny/``. If not, change the current directory to this path.
Next, to build the stack, execute:

::

    bitbake iota-tiny-image

The initial clean build will be lengthy, given that all host utilities are to be built as well as
the target images.
This includes host executables (python, cmake, etc.) and the required toolchain(s).

Once the build is successful, all images will be placed in the
``<ca5ds_workspace>/build-iota-tiny/tmp-iota_tiny/deploy/images/a5ds`` folder.

Everything apart from the BL1(ROM) binary is bundled into a single binary, the
``iota-tiny-image-a5ds.wic`` file.

Running the software on FVP
---------------------------
An FVP (Fixed Virtual Platform) of the Cortex-A5 DesignStart platform must be available to execute the
included run scripts.
Also, ensure that the FVP has its dependencies met by executing the FVP:

::

./<CA5DS Model Binary>

All dependencies are met if the FVP launches without any errors, presenting a graphical interface
showing information about the current state of the FVP.

The ``run_model.sh`` script in "<ca5ds_workspace>/run-scripts" folder will provide the previously built images as
arguments to the FVP and launch the FVP.

The run-scripts structure is as below:
::

    run-scripts
    |── run_model.sh
    └── scripts
        └── ...

Execute the ``run_model.sh`` script:

::

       ./run_model.sh
       usage: run_model.sh ${FVP executable path}

When the script is executed, one terminal instance will be launched for the CA5 processing element.
Once the FVP is executing, relevant memory contents of the .wic file are copied to their respective
memory locations within the model, and the CPU is brought out of reset.

The CPU will boot Linux and present a login prompt; login using the username ``root``.

Running the software on FPGA
----------------------------

Download the FPGA bundle and extract it. The directory structure of the FPGA bundle is shown below.
::

    ca5ds_fpga.impl
    └─ logical
       └─ sd_card
          ├── config.txt
          ├── MB
          │   ├── HBI0309B
          │   └── HBI0309C
          │       ├── CA5DS
          │       │   ├── ca5ds.txt
          │       │   ├── ca5ds0.bit
          │       │   └── images.txt
          │       ├── board.txt
          │       └── mbb_v139.ebf
          ├── readme
          └── SOFTWARE
              └── selftest.axf

Depending upon the MPS3 board version (printed on the MPS3 board) you should update the images.txt file
(in corresponding HBI0309x folder) so that the file points to the images under SOFTWARE directory.
Here is an example
::

    [IMAGES]
    TOTALIMAGES: 2                     ;Number of Images (Max: 32)

    IMAGE0ADDRESS: 0x00000000          ;Please select the required executable program
    IMAGE0UPDATE: FORCE                ;Image Update:NONE/AUTO/FORCE/RAM/AUTOQSPI/FORCEQSPI
    IMAGE0FILE: \SOFTWARE\bl1.bin

    IMAGE1ADDRESS: 0x08000000          ;Please select the required executable program
    IMAGE1UPDATE: RAM                  ;Image Update:NONE/AUTO/FORCE/RAM/AUTOQSPI/FORCEQSPI
    IMAGE1FILE: \SOFTWARE\ca5ds.wic

OUTPUT_DIR=``<a5ds_workspace>/build-iota-tiny/tmp-iota_tiny/deploy/images/a5ds``

1. Copy bl1.bin from OUTPUT_DIR directory to SOFTWARE directory of the FPGA bundle
2. Copy iota-tiny-image-a5ds.wic from OUTPUT_DIR directory
   to SOFTWARE directory of the FPGA bundle and rename the wic image to ca5ds.wic

**NOTE:** Renaming of the images are required because MCC firmware has limitation of 8 characters before .(dot)
and 3 characters after .(dot).

Now, copy the entire folder to board's SDCard and reboot the board.

On the host machine open 2 minicom sessions. In case of Linux machine, it will be ttyUSB0 and ttyUSB1. It might
be different on Window machine.
::

    ttyUSB0 for Motherboard Configuration Controller (MCC)
    ttyUSB1 for Cortex-A5

Once the system is booted completely, you should see console logs on the minicom session(ttyUSB1).
Login to the shell using **"root"** login.

--------------

*Copyright (c) 2019-2020, Arm Limited. All rights reserved.*
