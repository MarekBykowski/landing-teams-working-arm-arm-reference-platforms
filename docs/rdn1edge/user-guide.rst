RD-N1-Edge and RD-N1-Edge-Dual platform user guide
==================================================


.. section-numbering::
    :suffix: .

.. contents::


Introduction
------------

RD (Reference Design) is a collection of resources to provide a representative
view of typical compute subsystems that can be designed and implemented using
specific generations of Arm IP. RD-N1-Edge in particular is based on:

        - 8x `Neoverse N1 Cores <https://developer.arm.com/products/processors/neoverse/neoverse-n1>`_
          with DynamIQ Shared Unit (DSU)
        - Dedicated L2 cache: 512KB per core
        - Shared L3 cache: 2MB per cluster
        - CMN-600 with CML option: 8MB System Level Cache and 16MB Snoop Filter
        - DMC-620 with 2xRDIMM DDR4-3200
        - Multiple AXI expansion ports for I/O Coherent PCIe, Ethernet, offload
        - Arm Cortex-M7 for System Control Processor (SCP) and
          Manageability Control Processor (MCP)

RD-N1-Edge also supports a dual-chip configuration in which two RD-N1-Edge
platforms are connected through high speed CCIX link. The CCIX link is enabled
by CMN600's Coherent Multichip Link. Such platforms are called RD-N1-Edge-Dual
hereafter.

This document is a user guide on how to setup, build and run the software stack
of RD-N1-Edge and RD-N1-Edge-Dual on Fixed Virtual Platform.


Host machine requirements
-------------------------

The minimum recommended host PC specification for building the software stack
and running the RD-N1-Edge and RD-N1-Edge-Dual FVP model is a dual-core
processor running at 2GHz with 8GB of RAM. For best performance, use a machine
with a quad-core processor running at 2.6GHz with 16GB of RAM with free hard
disk space of at least 64GB.

The software package has been tested on **Ubuntu 16.04 LTS (64-bit)** and
**Ubuntu 18.04 LTS (64-bit)**. This guide assumes that the user is on either of
this operating system.


Repo tool setup
---------------

The software stack for RD-N1-Edge and RD-N1-Edge-Dual is available in multiple
git repositories. In order to simplify downloading the software stack, `repo tool <https://source.android.com/setup/develop/repo>`_
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
RD-N1-Edge and RD-N1-Edge-Dual software stack, is available `here <https://git.linaro.org/landing-teams/working/arm/arm-reference-platforms-manifest.git/>`_.
This section explains how to sync the software stack.

- Switch to a new folder

        ::

                mkdir rdn1edge
                cd rdn1edge

- For obtaining the latest *stable* software stack, use the following commands
  to sync:

        - For RD-N1-Edge:

        ::

                repo init -u https://git.linaro.org/landing-teams/working/arm/arm-reference-platforms-manifest.git -m pinned-rdn1edge.xml -b refs/tags/<RELEASE_TAG>
                repo sync -j $(nproc) --fetch-submodules --force-sync

        - For RD-N1-Edge-Dual:

        ::

                repo init -u https://git.linaro.org/landing-teams/working/arm/arm-reference-platforms-manifest.git -m pinned-rdn1edgex2.xml -b refs/tags/<RELEASE_TAG>
                repo sync -j $(nproc) --fetch-submodules --force-sync

  Note: The RELEASE_TAG can be found in the release notes, if obtained. If
  a release note is not available, or if a RELEASE_TAG is not known, use
  "master" as the branch to checkout and pass it as the value to the "-b"
  parameter as shown in the commands below.

        - For RD-N1-Edge:

        ::

                repo init -u https://git.linaro.org/landing-teams/working/arm/arm-reference-platforms-manifest.git -m pinned-rdn1edge.xml -b master
                repo sync -j $(nproc) --fetch-submodules --force-sync

        - For RD-N1-Edge-Dual:

        ::

                repo init -u https://git.linaro.org/landing-teams/working/arm/arm-reference-platforms-manifest.git -m pinned-rdn1edgex2.xml -b master
                repo sync -j $(nproc) --fetch-submodules --force-sync

- For obtaining the software stack with latest *upstream updates* but which
  might not have been fully validated, use the following commands to sync:

        - For RD-N1-Edge:

        ::

                repo init -u https://git.linaro.org/landing-teams/working/arm/arm-reference-platforms-manifest.git -m rdn1edge.xml -b master
                repo sync -j $(nproc) --fetch-submodules --force-sync

        - For RD-N1-Edge-Dual:

        ::

                repo init -u https://git.linaro.org/landing-teams/working/arm/arm-reference-platforms-manifest.git -m rdn1edgex2.xml -b master
                repo sync -j $(nproc) --fetch-submodules --force-sync

This will download the RD-N1-Edge or RD-N1-Edge-Dual software stack into the
``rdn1edge`` folder.


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

                # Move to the rdn1edge software stack directory
                cd rdn1edge

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


Obtaining the RD-N1-Edge and RD-N1-Edge-Dual Fast Model
-------------------------------------------------------

RD-N1-Edge Fast Model version 11.8 can be downloaded from `arm developer page <https://developer.arm.com/tools-and-software/simulation-models/fixed-virtual-platforms>`_
(under section *Arm Neoverse FVPs*).

User can request for the latest version of RD-N1-Edge and RD-N1-Edge-Dual Fast
Models through `this page <https://developer.arm.com/products/system-design/fixed-virtual-platforms>`_
or contact arm directly at this email address: `support-connect@arm.com <mailto:support-connect@arm.com>`_.

Follow the instruction in the installer and setup the FVP. Typically, the
installer will ask to create a new folder in the home directory. You can either
install the FVP in the home folder, or in the ``fastmodel/refinfra`` folder
inside the ``rdn1edge`` folder. If you would like to install in the
``fastmodel/refinfra`` folder, when asked for the install location,
enter as ``fastmodel/refinfra``.

Before launching any scripts from ``model-scripts`` folder, export the absolute
path of the model as an environment variable.

        ::

                export MODEL=<absolute-path-of-the-model-executable>

This completes the steps to obtain the RD-N1-Edge and RD-N1-Edge-Dual Fast
Models.


Supported Features
------------------

RD-N1-Edge and RD-N1-Edge-Dual software stack supports number of tests to
explore its features. To begin with, one can start with the busybox boot, and
then try installing and booting various linux distribution. RD-N1-Edge is target
for infrastructure platforms and it supports variety of infrastructure specific
features.

All the supported tests for RD-N1-Edge and RD-N1-Edge-Dual are listed below:

+----------------------------------------------+-------------+-----------------+
| Filesystems                                  | RD-N1-Edge  | RD-N1-Edge-Dual |
+==============================================+=============+=================+
| `Busybox`_                                   | Supported   | Supported       |
+----------------------------------------------+-------------+-----------------+
| `Fedora 27 Enterprise Linux Distribution`_   | Supported   |                 |
+----------------------------------------------+-------------+-----------------+
| `Debian 9.8.0 Enterprise Linux Distribution`_| Supported   |                 |
+----------------------------------------------+-------------+-----------------+
| `Ubuntu 18.4 Enterprise Linux Distribution`_ | Supported   |                 |
+----------------------------------------------+-------------+-----------------+

+----------------------------------------------+-------------+-----------------+
| Tests                                        | RD-N1-Edge  | RD-N1-Edge-Dual |
+==============================================+=============+=================+
| `ACS`_                                       | Supported   |                 |
+----------------------------------------------+-------------+-----------------+
| `KVM`_                                       | Supported   |                 |
+----------------------------------------------+-------------+-----------------+
| `RAS`_                                       | Supported   |                 |
+----------------------------------------------+-------------+-----------------+
| `Secure Boot`_                               | Supported   |                 |
+----------------------------------------------+-------------+-----------------+
| `TFTF`_                                      | Supported   |                 |
+----------------------------------------------+-------------+-----------------+

--------------

*Copyright (c) 2019, Arm Limited. All rights reserved.*


.. _Busybox: how-to/busybox-boot.rst
.. _Fedora 27 Enterprise Linux Distribution: how-to/fedora-test.rst
.. _Debian 9.8.0 Enterprise Linux Distribution: how-to/debian-test.rst
.. _Ubuntu 18.4 Enterprise Linux Distribution: how-to/ubuntu-test.rst
.. _ACS: how-to/acs-test.rst
.. _KVM: how-to/kvm-test.rst
.. _RAS: how-to/ras-test.rst
.. _Secure Boot: how-to/secureboot-test.rst
.. _TFTF: how-to/tftf-test.rst

