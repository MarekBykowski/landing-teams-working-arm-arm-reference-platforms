User Guide
==========

.. section-numbering::
    :suffix: .

.. contents::

Notice
------
The Corstone-500 software stack uses the `Yocto project <https://www.yoctoproject.org/>`__ to build
a tiny Linux distribution. The yocto project relies on the
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
Within the Yocto project, each component included in the Corstone-500 software stack is specified as
a `bitbake recipe <https://www.yoctoproject.org/docs/1.6/bitbake-user-manual/bitbake-user-manual.html#recipes>`__.
The recipes specific to the Corstone-500 project may be located at:
``<Corstone-500_workspace>/layers/meta-arm/``.

Software
########

Trusted Firmware-A
******************
Based on `ARM Trusted Firmware-A <https://github.com/ARM-software/arm-trusted-firmware>`__.

+--------+----------------------------------------------------------------------------------------------------------------+
| Recipe | <Corstone-500_workspace>/layers/meta-arm/meta-arm/recipes-bsp/trusted-firmware-a/trusted-firmware-a_2.3.bb     |
+--------+----------------------------------------------------------------------------------------------------------------+
| Files  | * bl1.bin                                                                                                      |
+--------+----------------------------------------------------------------------------------------------------------------+

U-Boot
******
Based on `U-Boot <git://git.denx.de/u-boot.git>`__.

+--------+----------------------------------------------------------------------------------------------------------------+
| Recipe | <Corstone-500_workspace>/layers/openembedded-core/meta/recipes-bsp/u-boot/u-boot_2020.07.bb                    |
+--------+----------------------------------------------------------------------------------------------------------------+
| Files  | * u-boot.bin                                                                                                   |
+--------+----------------------------------------------------------------------------------------------------------------+

Linux
*****
The recipe responsible for building a version of Linux.
The Linux distribution used is poky-tiny which is provided by the Yocto project.
poky-tiny allows the generation of a small size linux distribution.

`poky-tiny <https://wiki.yoctoproject.org/wiki/Poky-Tiny>`__

The provided distribution is based on busybox and built using musl C library.

+--------+----------------------------------------------------------------------------------------------------------------+
| Recipe | <Corstone-500_workspace>/layers/meta-arm/meta-arm-bsp/recipes-kernel/linux/linux-yocto_5.3.bb                  |
+--------+----------------------------------------------------------------------------------------------------------------+
| Files  | * zImage                                                                                                       |
|        | * arm-reference-image-corstone500.cpio.gz (rootfs)                                                             |
+--------+----------------------------------------------------------------------------------------------------------------+

Run scripts
###########

Within ``<Corstone-500_workspace>/run-scripts/iot`` a number of convenience functions for testing the software
stack may be found.
Usage descriptions for the various scripts are provided in the following sections.


Building the Software stack
---------------------------
Corstone-500 is a Bitbake based Yocto distro which uses bitbake commands to build the stack.
In the top directory of the synced workspace (~/Corstone-500), run:

::

    export DISTRO="poky-tiny"
    export MACHINE="corstone500"
    source setup-environment

By sourcing setup-environment, your current directory should now have switched to
``<Corstone-500_workspace>/build-poky-tiny/``. If not, change the current directory to this path.
Next, to build the stack, execute:

::

    bitbake arm-reference-image

The initial clean build will be lengthy, given that all host utilities are to be built as well as
the target images.
This includes host executables (python, cmake, etc.) and the required toolchain(s).

Once the build is successful, all images will be placed in the deploy directory
``<Corstone-500_workspace>/build-poky-tiny/tmp-poky_tiny/deploy/images/corstone500`` folder.

Everything apart from the BL1(ROM) binary is bundled into a single binary, the
``arm-reference-image-corstone500.wic.nopt`` file.

Running the software on FVP
---------------------------
An FVP (Fixed Virtual Platform) of the Corstone-500 platform must be available to execute the
included run scripts.
Also, ensure that the FVP has its dependencies met by executing the FVP:

::

./<Corstone-500 Model Binary>

All dependencies are met if the FVP launches without any errors, presenting a graphical interface
showing information about the current state of the FVP.

The ``run_model.sh`` script in "<Corstone-500_workspace>/run-scripts/iot" folder will provide the previously built images as
arguments to the FVP and launch the FVP.

The iot folder structure is as follows:
::

    iot
    |── run_model.sh
    └── scripts
        └── ...

Execute the ``run_model.sh`` script:

::

       ./run_model.sh
       usage: run_model.sh ${FVP executable path} [ -u ]
         -u: Run unit test selector using pyIRIS
          No additional argument: load and execute model

When the script is executed, one terminal instance will be launched for the Cortex-A5 processing element.
Once the FVP is executing, relevant memory contents of the .wic.nopt file are copied to their respective
memory locations within the model, and the CPU is brought out of reset.

The CPU will boot Linux and present a login prompt; login using the username ``root``.

--------------

*Copyright (c) 2019-2020, Arm Limited. All rights reserved.*
