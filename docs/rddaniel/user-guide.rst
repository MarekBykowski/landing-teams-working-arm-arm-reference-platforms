RD-Daniel platform user guide
=============================


.. section-numbering::
    :suffix: .

.. contents::


Introduction
------------

RD (Reference Design) is a collection of resources to provide a representative
view of typical compute subsystems that can be designed and implemented using
specific generations of Arm IP.

RD-Daniel supports the following configurations and those include the following
ARM IP's:

        - ARM CPU:

                - RD-Daniel Config M:
                        - 16xMP1 Zeus CPUs

                - RD-Daniel Config L:
                        - 32xMP1 Zeus CPUs

                - RD-Daniel Config XL:
                        - 64xMP1 Zeus CPUs

        - CMN-Rhodes (with CAL): 16MB System Level Cache and 32MB Snoop Filter
        - Multiple AXI expansion ports for I/O Coherent PCIe, Ethernet, offload
        - Arm Cortex-M7 for System Control Processor (SCP) and
          Manageability Control Processor (MCP)

RD-Daniel Config XL is a dual-chip configuration of Config L in which two
RD-Daniel Config L platforms are connected through high speed CCIX link. The
CCIX link is enabled through CMN-Rhodes's Coherent Multichip Link (CML) feature.

The Fixed Virtual Platform of RD-Daniel Config XL supports 4xMP1 Zeus CPUs on
each chips totalling to 8xMP1 Zeus CPUs. The FVP version of RD-Daniel Config XL
is referred as RD-Daniel-Dual in this document.

This document is a user guide on how to setup, build and run the software stack
of RD-Daniel and RD-Daniel-Dual on Fixed Virtual Platform.


Host machine requirements
-------------------------

The minimum recommended host PC specification for building the software stack
and running the RD-Daniel and RD-Daniel-Dual FVP model is a dual-core processor
running at 2GHz with 8GB of RAM. For best performance, use a machine with a
quad-core processor running at 2.6GHz with 16GB of RAM with free hard disk space
of at least 64GB.

The software package has been tested on **Ubuntu 16.04 LTS (64-bit)** and
**Ubuntu 18.04 LTS (64-bit)**. This guide assumes that the user is on either of
this operating system.


Repo tool setup
---------------

The software stack for RD-Daniel and RD-Daniel-Dual is available in multiple git
repositories. In order to simplify downloading the software stack, `repo tool <https://source.android.com/setup/develop/repo>`_
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

- Download the repo tool

        ::

                sudo apt-get install repo

This completes the setup of the repo tool.


Syncing the software stack
--------------------------

The manifest file, which contains the location of all the git repositories of
RD-Daniel and RD-Daniel-Dual software stack, is available `here <https://git.linaro.org/landing-teams/working/arm/arm-reference-platforms-manifest.git/>`_.
This section explains how to sync the software stack.

- Switch to a new folder

        ::

                mkdir rd-daniel
                cd rd-daniel

- For obtaining the latest *stable* software stack, use the following commands
  to sync:

        - For RD-Daniel:

        ::

                repo init -u https://git.linaro.org/landing-teams/working/arm/arm-reference-platforms-manifest.git -m pinned-rddaniel.xml -b refs/tags/<RELEASE_TAG>
                repo sync -j $(nproc) --fetch-submodules --force-sync

        - For RD-Daniel-Dual:

        ::

                repo init -u https://git.linaro.org/landing-teams/working/arm/arm-reference-platforms-manifest.git -m pinned-rddanielx2.xml -b refs/tags/<RELEASE_TAG>
                repo sync -j $(nproc) --fetch-submodules --force-sync

  Note: The RELEASE_TAG can be found in the release notes, if obtained. If
  a release note is not available, or if a RELEASE_TAG is not known, use
  "master" as the branch to checkout and pass it as the value to the "-b"
  parameter as shown in the commands below.

        - For RD-Daniel:

        ::

                repo init -u https://git.linaro.org/landing-teams/working/arm/arm-reference-platforms-manifest.git -m rddaniel.xml -b master
                repo sync -j $(nproc) --fetch-submodules --force-sync

        - For RD-Daniel-Dual:

        ::

                repo init -u https://git.linaro.org/landing-teams/working/arm/arm-reference-platforms-manifest.git -m rddanielx2.xml -b master
                repo sync -j $(nproc) --fetch-submodules --force-sync

This will download the RD-Daniel or RD-Daniel-Dual software stack into the
``rd-daniel`` folder.


Installing prerequisites
------------------------

Run the following command to install all the required prerequisites to build the
software stack:

        ::

                sudo ./build-scripts/rdinfra/install_prerequisites.sh

It is mandatory to execute this script at least once before build and executing
the software stack.


Downloading the GCC toolchain binaries
--------------------------------------

In addition to the prerequisites installed, gcc toolchain binaries have to be
downloaded and placed at the ``tools/gcc`` folder. Use the following commands
to download and untar the binaries:

        ::

                # Move to the rd-daniel software stack directory
                cd rd-daniel

                # Create a folder for gcc under tools folder
                mkdir -p tools/gcc
                cd tools/gcc

                # Download and extract the binaries
                wget https://releases.linaro.org/components/toolchain/binaries/6.2-2016.11/aarch64-linux-gnu/gcc-linaro-6.2.1-2016.11-x86_64_aarch64-linux-gnu.tar.xz
                tar -xJf gcc-linaro-6.2.1-2016.11-x86_64_aarch64-linux-gnu.tar.xz
                wget https://releases.linaro.org/components/toolchain/binaries/6.2-2016.11/arm-linux-gnueabihf/gcc-linaro-6.2.1-2016.11-x86_64_arm-linux-gnueabihf.tar.xz
                tar -xJf gcc-linaro-6.2.1-2016.11-x86_64_arm-linux-gnueabihf.tar.xz
                wget https://armkeil.blob.core.windows.net/developer//sitecore/shell/-/media/Files/downloads/gnu-rm/5_4-2016q3/gcc-arm-none-eabi-5_4-2016q3-20160926-linux,-d-,tar.bz2
                tar -xjf gcc-arm-none-eabi-5_4-2016q3-20160926-linux,-d-,tar.bz2

This completes the setup of the GCC toolchain binaries.


Obtaining the RD-Daniel and RD-Daniel Fast Model
------------------------------------------------

User can request for the latest version of RD-Daniel and RD-Daniel-Dual Fast
Model by sending a email to Arm at this email address: `support-connect@arm.com <mailto:support-connect@arm.com>`_.

Follow the instruction in the installer and setup the FVP. Typically, the
installer will ask to create a new folder in the home directory. You can either
install the FVP in the home folder, or in the ``fastmodel/refinfra`` folder
inside the ``rd-daniel`` folder. If you would like to install in the
``fastmodel/refinfra`` folder, when asked for the install location,
provide the absolute path of the ``fastmodel/refinfra``.

Before launching any scripts from ``model-scripts`` folder, export the absolute
path of the model as an environment variable.

        ::

                export MODEL=<absolute-path-of-the-model-executable>

This completes the steps to obtain the RD-Daniel and RD-Daniel-Dual Fast Model.


Supported Features
------------------

RD-Daniel and RD-Daniel-Dual software stack supports busybox boot (`Busybox`_).

--------------

*Copyright (c) 2019, Arm Limited. All rights reserved.*


.. _Busybox: how-to/busybox-boot.rst

