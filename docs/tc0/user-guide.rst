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
     curl libncurses-dev libz-dev python-pip repo u-boot-tools

If syncing and building android, the minimum requirements for the host machine can be found at https://source.android.com/setup/build/requirements, These include:
 * At least 250GB of free disk space to check out the code and an extra 150 GB to build it. If you conduct multiple builds, you need additional space.
 * At least 16 GB of available RAM/swap.

Syncing and building the source code
------------------------------------

There are two distros supported in the TC0 software stack: poky (a minimal distro containing busybox) and android.

To sync code for poky, please follow the steps in "Syncing code" section for BSP only. To sync code for android, please follow the steps for syncing both BSP and Android.

To build the required binaries for poky, please follow the steps in "Board Support Package build" section only. To build the binaries for Android, please follow the steps in both "Board Support Package build" and "Android OS build" sections.

Syncing code
#####################

Create a new folder that will be your workspace, which will henceforth be referred to as ``<tc0_workspace>``
in these instructions.

::

    mkdir <tc0_workspace>
    cd <tc0_workspace>
    export TC0_RELEASE=refs/tags/TC0-2020.10.29

To sync BSP only without Android, execute the repo command.

::

    repo init -u https://git.linaro.org/landing-teams/working/arm/arm-reference-platforms-manifest.git -m tc0.xml -b ${TC0_RELEASE} -g bsp
    repo sync -j$(nproc)

To sync both the BSP and Android, execute the repo command.

::

    repo init -u https://git.linaro.org/landing-teams/working/arm/arm-reference-platforms-manifest.git -m tc0.xml -b ${TC0_RELEASE} -g android
    repo sync -j$(nproc)


Board Support Package build
############################

::

    cd <tc0_workspace>/bsp
    export DISTRO="poky"
    export MACHINE="tc0"
    source setup-environment
    bitbake tc0-kernel-image

The initial clean build will be lengthy, given that all host utilities are to be built as well as
the target images. This includes host executables (python, cmake, etc.) and the required toolchain(s).

Once the build is successful, all images will be placed in the ``<tc0_workspace>/bsp/build-poky/tmp-poky/deploy/images/tc0``
directory.

Note that the BSP includes the Poky Linux distribution, which offers BusyBox-like utilities.


Android OS build
#################

Two profiles are supported:

#. tc0_swr  : This supports Android display with swiftshader (software rendering).
#. tc0_nano : This supports headless Android and provides a good runtime environment for testing shell-based applications.

The android images can be built with or without authentication enabled using Android Verified Boot(AVB).
AVB build is done in userdebug mode and takes a longer time to boot as the images are verified.
To enable AVB, copy the kernel Image to the device profile in advance of executing the below commands to build android:

::

    cp <tc0_workspace>/bsp/build-poky/tmp-poky/deploy/images/tc0/Image <tc0_workspace>/android/device/arm/tc0/

The ``build-scripts/tc0/build_android.sh`` script in ``<tc0_workspace>/android`` will patch and build android. This can be passed 2 parameters, ``-d`` for deciding which profile to build and ``-a`` for enabling AVB. The following command shows the help menu for the script:

::

    cd <tc0_workspace>/android
    ./build-scripts/tc0/build_android.sh  -h
    Incorrect script use, call script as:
    <path to build_android.sh> [OPTIONS]
    OPTIONS:
    -d, --distro                            distro version, values supported [android-nano, android-swr]
    -a, --avb                               [OPTIONAL] avb boot, values supported [true, false], DEFAULT: false

As an example, to build android with software rendering and AVB enabled, execute the command:

::

  ./build-scripts/tc0/build_android.sh -d android-swr -a true

To build headless android without AVB, execute the command:

::

  ./build-scripts/tc0/build_android.sh -d android-nano

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
| Files  | * <tc0_workspace>/bsp/build-poky/tmp-poky/deploy/images/tc0/bl1-tc0.bin                                    |
|        | * <tc0_workspace>/bsp/build-poky/tmp-poky/deploy/images/tc0/fip-tc0.bin                                    |
+--------+------------------------------------------------------------------------------------------------------------+


System Control Processor (SCP)
******************************

Based on `SCP Firmware <https://github.com/ARM-software/SCP-firmware>`__

+--------+------------------------------------------------------------------------------------------------+
| Recipe | <tc0_workspace>/bsp/layers/meta-arm/meta-arm-bsp/recipes-bsp/scp-firmware/scp-firmware-tc0.inc |
+--------+------------------------------------------------------------------------------------------------+
| Files  | * <tc0_workspace>/bsp/build-poky/tmp-poky/deploy/images/tc0/scp_ramfw.bin                      |
|        | * <tc0_workspace>/bsp/build-poky/tmp-poky/deploy/images/tc0/scp_romfw.bin                      |
+--------+------------------------------------------------------------------------------------------------+


U-Boot
******

Based on `U-Boot gitlab <https://gitlab.denx.de/u-boot/u-boot>`__

+--------+------------------------------------------------------------------------------------+
| Recipe | <tc0_workspace>/bsp/layers/meta-arm/meta-arm-bsp/recipes-bsp/u-boot/u-boot-tc0.inc |
+--------+------------------------------------------------------------------------------------+
| Files  | * <tc0_workspace>/bsp/build-poky/tmp-poky/deploy/images/tc0/u-boot.bin             |
+--------+------------------------------------------------------------------------------------+


Linux
*****

The recipe responsible for building a 4.19 version of the Android Common kernel (`ACK <https://android.googlesource.com/kernel/common/>`__).

+--------+-----------------------------------------------------------------------------------------------+
| Recipe | <tc0_workspace>/bsp/layers/meta-arm/meta-arm-bsp/recipes-kernel/linux/linux-arm64-ack-tc0.inc |
+--------+-----------------------------------------------------------------------------------------------+
| Files  | * <tc0_workspace>/bsp/build-poky/tmp-poky/deploy/images/tc0/Image                             |
+--------+-----------------------------------------------------------------------------------------------+


Poky Linux distro
*****************

The layer is based on the `poky <https://www.yoctoproject.org/software-item/poky/>`__ Linux distribution.
The provided distribution is based on BusyBox and built using glibc.

+--------+---------------------------------------------------------------------------------------------------+
| Recipe | <tc0_workspace>/bsp/layers/openembedded-core/meta/recipes-core/images/core-image-minimal.bb       |
+--------+---------------------------------------------------------------------------------------------------+
| Files  | * <tc0_workspace>/bsp/build-poky/tmp-poky/deploy/images/tc0/fitImage-core-image-minimal-tc0-tc0   |
+--------+---------------------------------------------------------------------------------------------------+


Android
*******

Android 10 is supported in this release with device profiles suitable for TC0 machine configuration.
Android is built as a separate project and then booted with the BSP built by Yocto.


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
       -a, --avb                        [OPTIONAL] avb boot, values supported [true, false], DEFAULT: false
       -t, --tap-interface              [OPTIONAL] enable TAP interface
       -e, --extra-model-params	        [OPTIONAL] extra model parameters
       If using an android distro, export ANDROID_PRODUCT_OUT variable to point to android out directory
       for eg. ANDROID_PRODUCT_OUT=<tc0_workspace>/android/out/target/product/tc0_swr

       For running Poky:
        ./run-scripts/run_model.sh -m <model binary path> -d poky

       For running android with AVB disabled:
        ./run-scripts/run_model.sh -m <model binary path> -d android-swr
        OR
        ./run-scripts/run_model.sh -m <model binary path> -d android-nano

       For running android with AVB enabled:
        ./run-scripts/run_model.sh -m <model binary path> -d android-swr -a true
        OR
        ./run-scripts/run_model.sh -m <model binary path> -d android-nano -a true

When the script is executed, three terminal instances will be launched, one for the SCP and two for
the  AP. Once the FVP is running, the SCP will be the first to boot, bringing the AP out of reset.
The AP will start booting from its ROM and then proceed to boot Trusted Firmware-A, then U-Boot, then
Linux and Poky/Android.

When booting Poky the model will boot Linux and present a login prompt. Login using the username ``root``.
You may need to hit Enter for the prompt to appear.

--------------

*Copyright (c) 2020, Arm Limited. All rights reserved.*
