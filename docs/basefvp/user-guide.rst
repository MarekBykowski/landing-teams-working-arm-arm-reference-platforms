Armv8 Architecture FVP platform user guide
==========================================


.. section-numbering::
    :suffix: .

.. contents::


Introduction
------------

The platform includes the Architecture Envelope Model (AEM) for Armv8 and a comprehensive set of SystemIP.

This document is a user guide on how to setup, build and run Linux based software stack on Armv8-A Base Platform FVP.


Host machine requirements
-------------------------

The software package has been tested on **Ubuntu 16.04 LTS (64-bit)** and
**Ubuntu 18.04 LTS (64-bit)**. 


Repo tool setup
---------------

Platform software stack comprises of various software components, spread across multiple git repositories. In
order to simplify fetching software stack components, `repo tool <https://source.android.com/setup/develop/repo>`_
can be used. This section explains how to setup git and repo tool.

- Install Git by using the following command

        ::

                sudo apt-get install git

- Git installation can be confirmed by checking the version

        ::

                git --version

  This should return the git version in a format such as ``git version 2.7.4``

- Set name and email address in git

        ::

                git config --global user.name "<your-name>"
                git config --global user.email "<your-email@example.com>"

- Install repo tool

        ::

                sudo apt-get install repo

This completes the setup of repo tool.



Obtaining Armv8-A Base Platform FVP
-----------------------------------

Armv8-A Base Platform FVP can be downloaded from 
`here <https://developer.arm.com/tools-and-software/simulation-models/fixed-virtual-platforms>`_.


Follow the instruction in the installer and setup the FVP.

Before launching any scripts from ``model-scripts`` folder, export the absolute
path of the model as an environment variable.

        ::

                export MODEL=<absolute-path-of-the-model-executable>

This completes the steps to obtain Armv8-A Base Platform FVP.


Sync, Build and Run Busybox on Armv8-A Base Platform FVP
---------------------------------------------------------
This description outlines steps to boot latest stable kernel version 5.1 on Armv8-A Base Platform FVP with Busybox filesystem.

        ::

                # Move to the platform directory
                mkdir platform
                cd platform

                # Fetch software stack
                repo init -u https://git.linaro.org/landing-teams/working/arm/manifest.git -m pinned-latest.xml -b 19.06
                repo sync

                # Get GCC tools
                mkdir -p tools/gcc
                cd tools/gcc
                wget https://releases.linaro.org/components/toolchain/binaries/6.2-2016.11/aarch64-linux-gnu/gcc-linaro-6.2.1-2016.11-x86_64_aarch64-linux-gnu.tar.xz
                tar -xJf gcc-linaro-6.2.1-2016.11-x86_64_aarch64-linux-gnu.tar.xz
                wget https://releases.linaro.org/components/toolchain/binaries/6.2-2016.11/arm-linux-gnueabihf/gcc-linaro-6.2.1-2016.11-x86_64_arm-linux-gnueabihf.tar.xz
                tar -xJf gcc-linaro-6.2.1-2016.11-x86_64_arm-linux-gnueabihf.tar.xz

                # Build
                ./build-scripts/build-all.sh -p fvp -f busybox all

                # Run
                export INITRD=output/fvp/fvp-busybox/uboot/ramdisk.img
                export IMAGE=output/fvp/fvp-busybox/uboot/Image
                export BL1=output/fvp/fvp-busybox/uboot/bl1.bin
                export FIP=output/fvp/fvp-busybox/uboot/fip.bin
                export DTB=output/fvp/fvp-busybox/uboot/fvp-base-aemv8a-aemv8a-t1.dtb

                cd model-scripts/fvp
                ./run_model.sh

Sync, Build and Run OE on Armv8-A Base Platform FVP
---------------------------------------------------
This description outlines steps to boot latest stable kernel version 5.1 on Armv8-A Base Platform FVP with OE (LAMP) filesystem.
       

        ::

                # Move to the platform directory
                mkdir platform
                cd platform

                # Fetch software stack
                repo init -u https://git.linaro.org/landing-teams/working/arm/manifest.git -m pinned-latest.xml -b 19.06
                repo sync

                # Get GCC tools
                mkdir -p tools/gcc
                cd tools/gcc
                wget https://releases.linaro.org/components/toolchain/binaries/6.2-2016.11/aarch64-linux-gnu/gcc-linaro-6.2.1-2016.11-x86_64_aarch64-linux-gnu.tar.xz
                tar -xJf gcc-linaro-6.2.1-2016.11-x86_64_aarch64-linux-gnu.tar.xz
                wget https://releases.linaro.org/components/toolchain/binaries/6.2-2016.11/arm-linux-gnueabihf/gcc-linaro-6.2.1-2016.11-x86_64_arm-linux-gnueabihf.tar.xz
                tar -xJf gcc-linaro-6.2.1-2016.11-x86_64_arm-linux-gnueabihf.tar.xz

                # Build
                ./build-scripts/build-all.sh -p fvp -f oe all

                # Fetch prebuilt OE filesystem
                mkdir oedisk
                cd oedisk
                wget http://releases.linaro.org/openembedded/juno-lsk/15.09/lt-vexpress64-openembedded_lamp-armv8-gcc-4.9_20150912-729.img.gz
                gunzip lt-vexpress64-openembedded_lamp-armv8-gcc-4.9_20150912-729.img.gz
                export DISK=lt-vexpress64-openembedded_lamp-armv8-gcc-4.9_20150912-729.img

                # Run
                export INITRD=output/fvp/fvp-oe/uboot/ramdisk.img
                export IMAGE=output/fvp/fvp-oe/uboot/Image
                export BL1=output/fvp/fvp-oe/uboot/bl1.bin
                export FIP=output/fvp/fvp-oe/uboot/fip.bin
                export DTB=output/fvp/fvp-oe/uboot/fvp-base-aemv8a-aemv8a-t1.dtb

                cd model-scripts/fvp
                ./run_model.sh

Sync, Build and Run Android-N on Armv8-A Base Platform FVP
----------------------------------------------------------
This description outlines steps to boot Android N (7.0-16.10) filesystem on Armv8-A Base Platform FVP.
       
        ::

                # Move to the platform directory
                mkdir platform
                cd platform

                # Fetch software stack
                repo init -u https://git.linaro.org/landing-teams/working/arm/manifest.git -m pinned-ack.xml -b 19.06
                repo sync

                # Get GCC tools
                mkdir -p tools/gcc
                cd tools/gcc
                wget https://releases.linaro.org/components/toolchain/binaries/6.2-2016.11/aarch64-linux-gnu/gcc-linaro-6.2.1-2016.11-x86_64_aarch64-linux-gnu.tar.xz
                tar -xJf gcc-linaro-6.2.1-2016.11-x86_64_aarch64-linux-gnu.tar.xz
                wget https://releases.linaro.org/components/toolchain/binaries/6.2-2016.11/arm-linux-gnueabihf/gcc-linaro-6.2.1-2016.11-x86_64_arm-linux-gnueabihf.tar.xz
                tar -xJf gcc-linaro-6.2.1-2016.11-x86_64_arm-linux-gnueabihf.tar.xz

                # Fetch prebuilt Android N filesystem
                mkdir -p prebuilts/android/fvp
                cd prebuilts/android/fvp
                wget http://releases.linaro.org/android/reference-lcr/fvp/7.0-16.10/fvp.img.bz2
                bunzip2 fvp.img.bz2
                export DISK=fvp.img
                wget http://releases.linaro.org/android/reference-lcr/fvp/7.0-16.10/ramdisk.img

                # Build
                ./build-scripts/build-all.sh -p fvp -f android all

                # Run
                export INITRD=prebuilts/android/fvp/ramdisk.img
                export IMAGE=output/fvp/fvp-android/uboot/Image
                export BL1=output/fvp/fvp-android/uboot/bl1.bin
                export FIP=output/fvp/fvp-android/uboot/fip.bin
                export DTB=output/fvp/fvp-android/uboot/fvp-base-aemv8a-aemv8a-t1.dtb
                
                cd model-scripts/fvp
                ./run_model.sh

Build and Run AArch32 builds on Armv8-A Base Platform FVP
---------------------------------------------------------

Build: Use platform selection as fvp32 in build steps explained above.
       Note: Output files become available at output/fvp32 folder. Set environment variables like IMAGE accordingly.

Run: Pass aarch32 argument to run_mode.sh
     ./run_model.sh --aarch32
Note: Android boot is not supported on AArch32 builds

--------------

*Copyright (c) 2019, Arm Limited. All rights reserved.*



