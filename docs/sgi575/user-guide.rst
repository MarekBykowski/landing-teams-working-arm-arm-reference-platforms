SGI-575 platform user guide
===========================


.. section-numbering::
    :suffix: .

.. contents::


Introduction
------------

SGI (System Guidance for Infrastructure) is a collection of resources to provide
a representative view of typical compute subsystems that can be designed and
implemented using specific generations of Arm IP. SGI-575 in particular is based
on:

    - Server Based System Architecture (SBSAv3)
    - 8x Cortex-A75 with private L2 Cache
    - DynamIQ with L3 Cache options
    - System Level Cache options
    - Up to 2x DDR4-3200 (DMC-620)
    - Arm Cortex-M7 for System Control Processor (SCP) and
      Manageability Control Processor (MCP)

This document is a user guide on how to setup, build and run the software stack
of SGI-575 on Fixed Virtual Platform.


Host machine requirements
-------------------------

The minimum recommended host PC specification for building the software stack
and running the SGI-575 FVP model is a dual-core processor running at 2GHz with
8GB of RAM. For best performance, use a machine with a quad-core processor
running at 2.6GHz with 16GB of RAM with free hard disk space of at least 64GB.

The software package has been tested on **Ubuntu 16.04 LTS (64-bit)** and
**Ubuntu 18.04 LTS (64-bit)**. This guide assumes that the user is on either of
this operating system.


Repo tool setup
---------------

The software stack for SGI-575 is available in multiple git repositories. In
order to simplify downloading the software stack for SGI-575 platform, `repo tool <https://source.android.com/setup/develop/repo>`_
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
SGI-575 software stack, is available `here <https://git.linaro.org/landing-teams/working/arm/arm-reference-platforms-manifest.git/>`_.
This section explains how to sync the software stack.

- Switch to a new folder

        ::

                mkdir sgi575
                cd sgi575

- For obtaining the latest *stable* software stack, use the following commands
  to sync:

        ::

                repo init -u https://git.linaro.org/landing-teams/working/arm/arm-reference-platforms-manifest.git -m pinned-sgi575.xml -b refs/tags/<RELEASE_TAG>
                repo sync -j $(nproc) --fetch-submodules --force-sync

  Note: The RELEASE_TAG can be found in the release notes, if obtained. If
  a release note is not available, or if a RELEASE_TAG is not known, use
  "master" as the branch to checkout and pass it as the value to the "-b"
  parameter as shown in the commands below.

        ::

                repo init -u https://git.linaro.org/landing-teams/working/arm/arm-reference-platforms-manifest.git -m pinned-sgi575.xml -b master
                repo sync -j $(nproc) --fetch-submodules --force-sync

- For obtaining the software stack with latest *upstream updates* but which
  might not have been fully validated, use the following commands to sync:

        ::

                repo init -u https://git.linaro.org/landing-teams/working/arm/arm-reference-platforms-manifest.git -m sgi575.xml -b master
                repo sync -j $(nproc) --fetch-submodules --force-sync

This will download the SGI-575 software stack into the ``sgi575`` folder.


Installing prerequisites
------------------------

Run the following command to install all the required prerequisites to build the
software stack:

        ::

                sudo ./build-scripts/sgi/install_prerequisites.sh

It is mandatory to execute this script at least once before build and executing
the software stack.


Downloading the GCC toolchain binaries
--------------------------------------

In addition to the prerequisites installed, gcc toolchain binaries have to be
downloaded and placed at the ``tools/gcc`` folder. Use the following commands
to download and untar the binaries:

        ::

                # Move to the sgi575 software stack directory
                cd sgi575

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


Obtaining the SGI-575 Fast Model
--------------------------------

A free version of SGI-575 FVP can be downloaded from the `FVP download page <https://developer.arm.com/products/system-design/fixed-virtual-platforms>`_.
Or, use this `direct link <https://silver.arm.com/download/download.tm?pv=4155978&p=2984141>`_
to download the compressed file. User can request for the latest version through
the same page or contact arm directly at this email address: `support-connect@arm.com <mailto:support-connect@arm.com>`_.

To setup the free version of SGI-575 FVP, after obtaining the file from the
above download link, use the following commands to extract and setup the model:

        ::

                # Move to the directory containing the downloaded file
                cd <required-path>

                # Create a directory where the downloaded file will be extracted
                mkdir fastmodel

                # Extract the tar file to fastmodel foler
                tar xvf FM000-KT-00155-r11p1-31rel0.tgz -C fastmodel

                # Setup the SGI-575 FVP
                cd fastmodel
                ./FVP_CSS_SGI-575.sh

Follow the instruction in the installer and setup the FVP. Typically, the
installer will ask to create a new folder in the home directory. You can either
install the FVP in the home folder, or in the ``fastmodel/refinfra`` folder
inside the ``sgi575`` folder. If you would like to install in the
``fastmodel/refinfra`` folder, when asked for the install location (see below),
provided the install path as shown below.

        ::

                Where would you like to install to? [default: /home/<user-id>/FVP_CSS_SGI-575]: /home/<some-path>/sgi575/fastmodel/refinfra

                Please answer with one of: 'yes/y' or 'no/n'
                '/home/<some-path>/sgi575/fastmodel/refinfra' does not exist, create? [default: yes]

This should install the SGI-575 FVP in ``sgi575/fastmodel/refinfra/``
folder. Before launching any scripts from ``model-scripts`` folder, export the
absolute path of the model as an environment variable.

        ::

                export MODEL=<some-path>/sgi575/fastmodel/refinfra/models/Linux64_GCC-4.8/FVP_CSS_SGI-575

This completes the steps to obtain the SGI-575 Fast Model.


Supported Features
------------------

SGI-575 software stack supports number of tests to explore its features. To
begin with, one can start with the busybox boot, and then try installing and
booting various linux distribution. SGI-575 is target for infrastructure
platforms and it supports variety of infrastructure specific features. All the
supported tests are listed below:

        1. Supported Filesystems:
                   a. `Busybox`_
                   b. `Fedora 27 Enterprise Linux Distribution`_
                   c. `Debian 9.8.0 Enterprise Linux Distribution`_
                   d. `Ubuntu 18.4 Enterprise Linux Distribution`_
        2. Supported Tests:
                   a. `ACS`_
                   b. `KVM`_
                   c. `RAS`_
                   d. `Secure Boot`_
                   e. `TFTF`_


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
