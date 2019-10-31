SGM775 platform user guide
==========================================


.. section-numbering::
    :suffix: .

.. contents::


Introduction
------------

SGM-775 is System Guidance for Mobile with collection of resources to provide
a representative view of typical compute subsystems that can be designed and
implemented using specific generations of Arm IP for mobile systems.

This document is a user guide on how to setup, build and run Linux based software stack on SGM-775 Platform FVP.


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



Obtaining SGM-775 Fast Model
----------------------------

A free version of SGM-775 FVP can be downloaded from website:
    https://developer.arm.com/products/system-design/fixed-virtual-platforms


Follow the instruction in the installer and setup the FVP.

Before launching any scripts from ``model-scripts`` folder, export the absolute
path of the model as an environment variable.

        ::

                export MODEL=<absolute-path-of-the-model-executable>

This completes the steps to obtain SGM-775 fast model.


Sync, Build and Run Busybox on SGM-775 FVP
------------------------------------------
This description outlines steps to boot Android common kernel version 4.9 on SGM-775 FVP with Busybox filesystem.

        ::

                # Move to the platform directory
                mkdir platform
                cd platform

                # Fetch software stack
                repo init -u https://git.linaro.org/landing-teams/working/arm/manifest.git -m sgm775.xml -b 19.10
                repo sync

                # Get GCC tools
                mkdir -p tools/gcc
                cd tools/gcc
                wget https://releases.linaro.org/components/toolchain/binaries/6.2-2016.11/aarch64-linux-gnu/gcc-linaro-6.2.1-2016.11-x86_64_aarch64-linux-gnu.tar.xz
                tar -xJf gcc-linaro-6.2.1-2016.11-x86_64_aarch64-linux-gnu.tar.xz
                wget https://releases.linaro.org/components/toolchain/binaries/6.2-2016.11/arm-linux-gnueabihf/gcc-linaro-6.2.1-2016.11-x86_64_arm-linux-gnueabihf.tar.xz
                tar -xJf gcc-linaro-6.2.1-2016.11-x86_64_arm-linux-gnueabihf.tar.xz

        # Build
                ./build-scripts/build-all.sh -p sgm775 -f busybox all

        # Run
                cd model-scripts/sgm775
                ./run_model.sh -f busybox


Sync, Build and Run Android-O on SGM-775 FVP
----------------------------------------------------------
This description outlines steps to boot Android O on SGM-775 FVP.
       
        ::
                # Move to the platform directory
                mkdir platform
                cd platform

                # Fetch software stack
                repo init -u https://git.linaro.org/landing-teams/working/arm/manifest.git -m sgm775-android.xml -b 19.10
                repo sync

                # Get GCC tools
                mkdir -p tools/gcc
                cd tools/gcc
                wget https://releases.linaro.org/components/toolchain/binaries/6.2-2016.11/aarch64-linux-gnu/gcc-linaro-6.2.1-2016.11-x86_64_aarch64-linux-gnu.tar.xz
                tar -xJf gcc-linaro-6.2.1-2016.11-x86_64_aarch64-linux-gnu.tar.xz
                wget https://releases.linaro.org/components/toolchain/binaries/6.2-2016.11/arm-linux-gnueabihf/gcc-linaro-6.2.1-2016.11-x86_64_arm-linux-gnueabihf.tar.xz
                tar -xJf gcc-linaro-6.2.1-2016.11-x86_64_arm-linux-gnueabihf.tar.xz

        # Build
                ./build-scripts/build-all.sh -p sgm775 -f android all

        # Run
                cd model-scripts/sgm775
                ./run_model.sh -f android


--------------

*Copyright (c) 2019, Arm Limited. All rights reserved.*

