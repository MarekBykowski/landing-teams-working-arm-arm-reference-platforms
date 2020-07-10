User Guide
==========

.. section-numbering::
    :suffix: .

.. contents::


Notice
------

The Total Compute 2020 (TC0) software stack uses the `Yocto project <https://www.yoctoproject.org/>`__
to build a Board Support Package (BSP) and a choice of Poky Linux distribution or Android userspace.
The Yocto project uses `Bitbake <https://www.yoctoproject.org/docs/1.6/bitbake-user-manual/bitbake-user-manual.html>`__
to build the software stack.


Prerequisites
-------------

These instructions assume that:
 * Your host PC is running Ubuntu Linux 18.04 LTS.
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

To resolve these dependencies, run:

::

    sudo apt-get update
    sudo apt-get install chrpath gawk texinfo libssl-dev diffstat wget git-core unzip gcc-multilib \
     build-essential socat cpio python python3 python3-pip python3-pexpect xz-utils debianutils \
     iputils-ping python3-git python3-jinja2 libegl1-mesa libsdl1.2-dev pylint3 xterm git-lfs openssl \
     curl libncurses-dev libz-dev python-pip repo


Syncing and building the source code
------------------------------------

Create a new folder that will be your workspace, which will henceforth be referred to as ``<tc0_workspace>``
in these instructions.

::

    mkdir <tc0_workspace>
    cd <tc0_workspace>


All users will need to sync the Board Support Package sources. Create a ``bsp/`` directory in your
``<tc0_workspace>``:

::

    mkdir bsp

Users wishing to run Android will additionally need to sync the Android userspace sources. Create an
``android10/`` directory in your ``<tc0_workspace>``:

::

    mkdir android10


Board Support Package
#####################

::

    cd <tc0_workspace>/bsp/
    export TC0_RELEASE=refs/tag/TC0-2020.07.20
    repo init -u https://git.linaro.org/landing-teams/working/arm/arm-reference-platforms-manifest.git -m tc0-yocto.xml -b ${TC0_RELEASE}
    repo sync -j${NUM_CPUS}
    export DISTRO="poky"
    export MACHINE="tc0"
    source setup-environment
    bitbake core-image-minimal

The initial clean build will be lengthy, given that all host utilities are to be built as well as
the target images. This includes host executables (python, cmake, etc.) and the required toolchain(s).

Once the build is successful, all images will be placed in the ``<tc0_workspace>/bsp/build-poky/tmp-poky/deploy/images/tc0``
directory.

Note that the BSP includes the Poky Linux distribution, which offers BusyBox-like utilities.


Android userspace
#################

Two profiles are supported:

#. tc0_swr-eng  : This supports Android display with swiftshader (software rendering).
#. tc0_nano-eng : This supports headless Android and provides a good runtime environment for testing shell-based applications.

::

    cd <tc0_workspace>/android10/
    export TC0_RELEASE=refs/tag/TC0-2020.07.20
    repo init -u https://git.linaro.org/landing-teams/working/arm/arm-reference-platforms-manifest.git -m tc0-android.xml -b ${TC0_RELEASE}
    repo sync -j${NUM_CPUS}
    . build/envsetup.sh
    lunch tc0_swr-eng      # or lunch tc0_nano-eng
    make -j${NUM_CPUS}


Provided components
-------------------

Within the Yocto project, each component included in the TC0 software stack is specified as
a `Bitbake recipe <https://www.yoctoproject.org/docs/1.6/bitbake-user-manual/bitbake-user-manual.html#recipes>`__.
The TC0 recipes are located at ``<tc0_workspace>/bsp/layers/meta-arm/``.


Software Components
###################

Trusted Firmware-A
******************

Based on `Trusted Firmware-A <https://trustedfirmware-a.readthedocs.io/en/latest/>`__

+--------+------------------------------------------------------------------------------------------------------------+
| Recipe | <tc0_workspace>/bsp/layers/meta-arm/meta-arm-bsp/recipes-bsp/trusted-firmware-a/trusted-firmware-a-tc0.inc |
+--------+------------------------------------------------------------------------------------------------------------+
| Files  | * bl1-tc0.bin                                                                                              |
|        | * fip-tc0.bin                                                                                              |
+--------+------------------------------------------------------------------------------------------------------------+


System Control Processor (SCP)
******************************

Based on `SCP Firmware <https://github.com/ARM-software/SCP-firmware>`__

+--------+------------------------------------------------------------------------------------------------+
| Recipe | <tc0_workspace>/bsp/layers/meta-arm/meta-arm-bsp/recipes-bsp/scp-firmware/scp-firmware-tc0.inc |
+--------+------------------------------------------------------------------------------------------------+
| Files  | * scp_ramfw.bin                                                                                |
|        | * scp_romfw.bin                                                                                |
+--------+------------------------------------------------------------------------------------------------+


U-Boot
******

Based on `U-Boot gitlab <https://gitlab.denx.de/u-boot/u-boot>`__

+--------+------------------------------------------------------------------------------------+
| Recipe | <tc0_workspace>/bsp/layers/meta-arm/meta-arm-bsp/recipes-bsp/u-boot/u-boot-tc0.inc |
+--------+------------------------------------------------------------------------------------+
| Files  | * u-boot.bin                                                                       |
+--------+------------------------------------------------------------------------------------+


Linux
*****

The recipe responsible for building a 4.19 version of the Android Common kernel (`ACK <https://android.googlesource.com/kernel/common/>`__).

+--------+-----------------------------------------------------------------------------------------------+
| Recipe | <tc0_workspace>/bsp/layers/meta-arm/meta-arm-bsp/recipes-kernel/linux/linux-arm64-ack-tc0.inc |
+--------+-----------------------------------------------------------------------------------------------+
| Files  | * Image                                                                                       |
+--------+-----------------------------------------------------------------------------------------------+


Poky Linux distro
*****************

The layer is based on the `poky <https://www.yoctoproject.org/software-item/poky/>`__ Linux distribution.
The provided distribution is based on BusyBox and built using glibc.

+--------+---------------------------------------------------------------------------------------------+
| Recipe | <tc0_workspace>/bsp/layers/openembedded-core/meta/recipes-core/images/core-image-minimal.bb |
+--------+---------------------------------------------------------------------------------------------+
| Files  | * core-image-minimal-tc0.cpio.gz.u-boot                                                     |
+--------+---------------------------------------------------------------------------------------------+


Android
*******

Android 10 is supported in this release with device profiles suitable for TC0 machine configuration.
Android is built as a separate project and then booted with the BSP built by Yocto. The images are
packaged using scripts in the ``<tc0_workspace>/bsp/run-scripts`` directory.


Run scripts
###########

Within the ``<tc0_workspace>/bsp/run-scripts/`` are several convenience functions for testing the software
stack. Usage descriptions for the various scripts are provided in the following sections.


Running the software on FVP
---------------------------

A Fixed Virtual Platform (FVP) of the TC0 platform must be available to execute the included run scripts.

The run-scripts structure is as follows:

::

    run-scripts
    |--tc0
       |--run_model.sh
       |-- ...

Ensure that all dependencies are met by executing the FVP: ``./path/to/FVP_TC0``. You should see
the FVP launch, presenting a graphical interface showing information about the current state of the FVP.

The ``run_model.sh`` script in ``<tc0_workspace>/bsp/run-scripts/tc0`` will launch the FVP, providing
the previously built images as arguments. Execute the ``run_model.sh`` script:

::

       ./run_model.sh
       Incorrect script use, call script as:
       <path_to_run_model.sh> [OPTIONS]
       OPTIONS:
       -m, --model                      path to model
       -d, --distro                     distro version, values supported [poky, android-nano, android-swr]
       -g, --generate-android-image     [OPTIONAL] generate android image and ramdisk, values supported [true, false], DEFAULT: true
       -t, --tap-interface              [OPTIONAL] enable TAP interface
       -e, --extra-model-params	        [OPTIONAL] extra model parameters
       If using an android distro, export ANDROID_PRODUCT_OUT variable to point to android out directory

       For Running Poky/Android :
        ./run-scripts/run_model.sh -m <model binary path> -d poky/android-swr/android-nano


When the script is executed, three terminal instances will be launched, one for the SCP and two for
the  AP. Once the FVP is running, the SCP will be the first to boot, bringing the AP out of reset.
The AP will start booting from its ROM and then proceed to boot Trusted Firmware-A, then U-Boot, then
Linux and Poky/Android.

When booting Poky the model will boot Linux and present a login prompt. Login using the username ``root``.
You may need to hit Enter for the prompt to appear.

--------------

*Copyright (c) 2020, Arm Limited. All rights reserved.*
