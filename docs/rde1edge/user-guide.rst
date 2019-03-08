RD-E1-Edge platform user guide
==============================


.. section-numbering::
    :suffix: .

.. contents::


Introduction
------------

RD (Reference Design) is a collection of resources to provide a representative
view of typical compute subsystems that can be designed and implemented using
specific generations of Arm IP. RD-E1-Edge in particular is based on:

        - 16x `Neoverse E1 Cores <https://developer.arm.com/products/processors/neoverse/neoverse-e1>`_
          with DynamIQ Shared Unit (DSU).
        - Dedicated L2 cache: 256KB per core
        - Shared L3 cache: 2MB per cluster
        - CMN-600 with CML option: 8MB System Level Cache and 16MB Snoop Filter
        - DMC-620 with 2xRDIMM DDR4-3200
        - Multiple AXI expansion ports for I/O Coherent PCIe, Ethernet, offload
        - Arm Cortex-M7 for System Control Processor (SCP) and
          Manageability Control Processor (MCP)

This document is a user guide on how to setup, build and run the software stack
of RD-E1-Edge on Fixed Virtual Platform.


Host machine requirements
-------------------------

The minimum recommended host PC specification for building the software stack
and running the RD-E1-Edge FVP model is a dual-core processor running at 2GHz with
8GB of RAM. For best performance, use a machine with a quad-core processor
running at 2.6GHz with 16GB of RAM with free hard disk space of at least 64GB.

The software package has been tested on **Ubuntu 16.04 LTS (64-bit)** and
**Ubuntu 18.04 LTS (64-bit)**. This guide assumes that the user is on either of
this operating system.


Repo tool setup
---------------

The software stack for RD-E1-Edge is available in multiple git repositories. In
order to simplify downloading the software stack for RD-E1-Edge platform, `repo tool <https://source.android.com/setup/develop/repo>`_
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
RD-E1-Edge software stack, is available `here <https://git.linaro.org/landing-teams/working/arm/arm-reference-platforms-manifest.git/>`_.
This section explains how to sync the software stack.

- Switch to a new folder

        ::

                mkdir rde1edge
                cd rde1edge

- For obtaining the latest *stable* software stack, use the following commands
  to sync:

        ::

                repo init -u https://git.linaro.org/landing-teams/working/arm/arm-reference-platforms-manifest.git -m pinned-rde1edge.xml -b refs/tags/<RELEASE_TAG>
                repo sync -j $(nproc) --fetch-submodules --force-sync

  Note: The RELEASE_TAG can be found in the release notes, if obtained. If
  a release note is not available, or if a RELEASE_TAG is not known, use
  "master" as the branch to checkout and pass it as the value to the "-b"
  parameter as shown in the commands below.

        ::

                repo init -u https://git.linaro.org/landing-teams/working/arm/arm-reference-platforms-manifest.git -m pinned-rde1edge.xml -b master
                repo sync -j $(nproc) --fetch-submodules --force-sync


  Note: If a release tag is not available, use "master" as the branch to
  checkout and pass it as the value to the "-b" parameter.

- For obtaining the software stack with latest *upstream updates* but which
  might not have been fully validated, use the following commands to sync:

        ::

                repo init -u https://git.linaro.org/landing-teams/working/arm/arm-reference-platforms-manifest.git -m rde1edge.xml -b master
                repo sync -j $(nproc) --fetch-submodules --force-sync

This will download the RD-E1-Edge software stack into the ``rde1edge`` folder.


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

                # Move to the rde1edge software stack directory
                cd rde1edge

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


Obtaining the RD-E1-Edge Fast Model
-----------------------------------

User can request for the latest version of RD-E1-Edge Fast Model through
`this page <https://developer.arm.com/products/system-design/fixed-virtual-platforms>`_
or contact arm directly at this email address: `support-connect@arm.com <mailto:support-connect@arm.com>`_.

Follow the instruction in the installer and setup the FVP. Typically, the
installer will ask to create a new folder in the home directory. You can either
install the FVP in the home folder, or in the ``fastmodel/refinfra`` folder
inside the ``rde1edge`` folder. If you would like to install in the
``fastmodel/refinfra`` folder, when asked for the install location,
enter as ``fastmodel/refinfra``.

Before launching any scripts from ``model-scripts`` folder, export the absolute
path of the model as an environment variable.

        ::

                export MODEL=<absolute-path-of-the-model-executable>

This completes the steps to obtain the RD-E1-Edge Fast Model.


Supported Features
------------------

RD-E1-Edge software stack supports number of tests to explore its features. To
begin with, one can start with the busybox boot, and then try installing and
booting various linux distribution. RD-E1-Edge is target for infrastructure
platforms and it supports variety of infrastructure specific features. All the
supported tests are listed below:

        1. Supported Filesystems:
                   a. `Busybox`_
                   b. `Fedora 27 Enterprise Linux Distribution`_
                   c. `Debian 9.8.0 Enterprise Linux Distribution`_
                   d. `Ubuntu 18.4 Enterprise Linux Distribution`_
        2. Supported Tests:
                   a. `KVM`_
                   b. `RAS`_
                   c. `Secure Boot`_


--------------

*Copyright (c) 2019, Arm Limited. All rights reserved.*


.. _Busybox: how-to/busybox-boot.rst
.. _Fedora 27 Enterprise Linux Distribution: how-to/fedora-test.rst
.. _Debian 9.8.0 Enterprise Linux Distribution: how-to/debian-test.rst
.. _Ubuntu 18.4 Enterprise Linux Distribution: how-to/ubuntu-test.rst
.. _KVM: how-to/kvm-test.rst
.. _RAS: how-to/ras-test.rst
.. _Secure Boot: how-to/secureboot-test.rst
