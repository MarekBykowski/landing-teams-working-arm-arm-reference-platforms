Juno platform software user guide
=================================


.. section-numbering::
    :suffix: .

.. contents::


Introduction
------------

This document is a user guide on how to setup and build Linux based software stack on Juno development board.
More details on Juno development board can be found
`here <https://developer.arm.com/tools-and-software/development-boards/juno-development-board>`_.


Host machine requirements
-------------------------

The software package has been tested on **Ubuntu 16.04 LTS (64-bit)**
Install python3-pyelftools


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


Sync and Build Busybox software stack on Juno development board
---------------------------------------------------------------
This description outlines steps to sync and build Linux (latest stable kernel version 5.3) based stack for Juno development board with Busybox filesystem.


        ::

        Software sync can be done in two methods:

        Method 1
                git clone https://git.linaro.org/landing-teams/working/arm/arm-reference-platforms.git
                cd arm-reference-platforms/
                python3 sync_workspace.py  --no_check_apt_deps 
                Follow the menu options to sync Busybox for Juno development board
        NOTE: Choose 'Prebuilts' in menu option to download prebuilt binaries

        OR

        Method 2

                # Move to the platform directory
                mkdir platform
                cd platform

                # Fetch software stack
                repo init -u https://git.linaro.org/landing-teams/working/arm/manifest.git -m pinned-latest.xml -b 19.10
                repo sync

                # Get GCC tools
                mkdir -p tools/gcc
                cd tools/gcc
                wget https://releases.linaro.org/components/toolchain/binaries/6.2-2016.11/aarch64-linux-gnu/gcc-linaro-6.2.1-2016.11-x86_64_aarch64-linux-gnu.tar.xz
                tar -xJf gcc-linaro-6.2.1-2016.11-x86_64_aarch64-linux-gnu.tar.xz
                wget https://releases.linaro.org/components/toolchain/binaries/6.2-2016.11/arm-linux-gnueabihf/gcc-linaro-6.2.1-2016.11-x86_64_arm-linux-gnueabihf.tar.xz
                tar -xJf gcc-linaro-6.2.1-2016.11-x86_64_arm-linux-gnueabihf.tar.xz

        # Build
                ./build-scripts/build-all.sh -p juno -f busybox all

        # Run
                Refer Juno Getting Started documentation
                https://developer.arm.com/tools-and-software/development-boards/juno-development-board


Sync and Build OE software stack on Juno development board
----------------------------------------------------------
This description outlines steps to sync and build Linux (latest stable kernel version 5.3) based stack for Juno development board with OE filesystem.

        ::

        Software sync can be done in two methods:

        Method 1
                git clone https://git.linaro.org/landing-teams/working/arm/arm-reference-platforms.git
                cd arm-reference-platforms/
                python3 sync_workspace.py  --no_check_apt_deps 
                Follow the menu options to sync OE for Juno development board
        NOTE: Choose 'Prebuilts' in menu option to download prebuilt binaries

        OR

        Method 2
                # Move to the platform directory
                mkdir platform
                cd platform

                # Fetch software stack
                repo init -u https://git.linaro.org/landing-teams/working/arm/manifest.git -m pinned-latest.xml -b 19.10
                repo sync

                # Get GCC tools
                mkdir -p tools/gcc
                cd tools/gcc
                wget https://releases.linaro.org/components/toolchain/binaries/6.2-2016.11/aarch64-linux-gnu/gcc-linaro-6.2.1-2016.11-x86_64_aarch64-linux-gnu.tar.xz
                tar -xJf gcc-linaro-6.2.1-2016.11-x86_64_aarch64-linux-gnu.tar.xz
                wget https://releases.linaro.org/components/toolchain/binaries/6.2-2016.11/arm-linux-gnueabihf/gcc-linaro-6.2.1-2016.11-x86_64_arm-linux-gnueabihf.tar.xz
                tar -xJf gcc-linaro-6.2.1-2016.11-x86_64_arm-linux-gnueabihf.tar.xz

        # Build
                ./build-scripts/build-all.sh -p juno -f oe all
                
                # Fetch prebuilt OE Minimal or OE LAMP filesystem
                OE Minimal:
                wget http://releases.linaro.org/openembedded/juno-lsk/17.01/lt-vexpress64-openembedded_minimal-armv8-gcc-5.2_20170127-761.img.gz
                OE LAMP:
                http://releases.linaro.org/openembedded/juno-lsk/17.01/lt-vexpress64-openembedded_lamp-armv8-gcc-5.2_20170127-761.img.gz

        # Run
                Refer Juno Getting Started documentation
                https://developer.arm.com/tools-and-software/development-boards/juno-development-board


Sync and Build Android P software stack on Juno development board
-----------------------------------------------------------------
This description outlines steps to sync and build Android P (with Android common kernel version 4.14) software stack Juno development board.

        ::

        Software sync can be done in two methods:

        Method 1
                git clone https://git.linaro.org/landing-teams/working/arm/arm-reference-platforms.git
                cd arm-reference-platforms/
                python3 sync_workspace.py  --no_check_apt_deps 
                Follow the menu options to sync Android for Juno development board
        NOTE: Choose 'Prebuilts' in menu option to download prebuilt binaries

        OR

        Method 2
                # Move to the platform directory
                mkdir platform
                cd platform

                # Fetch software stack
                repo init -u https://git.linaro.org/landing-teams/working/arm/manifest.git -m pinned-latest.xml -b 19.10
                repo sync

                # Get GCC tools
                mkdir -p tools/gcc
                cd tools/gcc
                wget https://releases.linaro.org/components/toolchain/binaries/6.2-2016.11/aarch64-linux-gnu/gcc-linaro-6.2.1-2016.11-x86_64_aarch64-linux-gnu.tar.xz
                tar -xJf gcc-linaro-6.2.1-2016.11-x86_64_aarch64-linux-gnu.tar.xz
                wget https://releases.linaro.org/components/toolchain/binaries/6.2-2016.11/arm-linux-gnueabihf/gcc-linaro-6.2.1-2016.11-x86_64_arm-linux-gnueabihf.tar.xz
                tar -xJf gcc-linaro-6.2.1-2016.11-x86_64_arm-linux-gnueabihf.tar.xz

                # Fetch prebuilt Android P filesystem
                mkdir -p prebuilts/android/juno
                cd prebuilts/android/juno
                wget http://releases.linaro.org/members/arm/android/juno/19.01/juno.img.bz2
                bunzip2 juno.img.bz2
                wget http://releases.linaro.org/members/arm/android/juno/19.01/ramdisk.img

        # Build
                ./build-scripts/build-all.sh -p juno -f android all

        # Run
                Refer Juno Getting Started documentation
                https://developer.arm.com/tools-and-software/development-boards/juno-development-board



AArch32 builds for Juno development board
-----------------------------------------

Build: Use platform selection as juno32 in build steps explained above.
       Note: Output files become available at output/juno32 folder. 

Note: Android boot is not supported on AArch32 builds

--------------

*Copyright (c) 2019, Arm Limited. All rights reserved.*



