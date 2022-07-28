User Guide
==========

.. section-numbering::
    :suffix: .

.. contents::


Notice
------

The FVP-BASE software stack uses the `Yocto project <https://www.yoctoproject.org/>`__
to build a Board Support Package (BSP) and the Poky Linux distribution.
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

Syncing and building the source code
------------------------------------

Create a new folder that will be your workspace, which will henceforth be referred to as ``<workspace>``
in these instructions.

::

    mkdir <workspace>
    cd <workspace>
    repo init -u git@github.com:MarekBykowski/landing-teams-working-arm-arm-reference-platforms-manifest.git -m fvp-yocto.xml -b refs/tags/BASEFVP-2020.08.06
    repo sync -j${NUM_CPUS}
    export DISTRO="poky"
    export MACHINE="fvp-base"
    source setup-environment
    bitbake core-image-minimal

The initial clean build will be lengthy, given that all host utilities are to be built as well as
the target images. This includes host executables (python, cmake, etc.) and the required toolchain(s).

Once the build is successful, all images will be placed in the ``<workspace>/build-poky/tmp-poky/deploy/images/fvp-base``
directory.

Note that the BSP includes the Poky Linux distribution, which offers BusyBox-like utilities.

Provided components
-------------------

Within the Yocto project, each component included in the FVP-BASE software stack is specified as
a `Bitbake recipe <https://www.yoctoproject.org/docs/1.6/bitbake-user-manual/bitbake-user-manual.html#recipes>`__.
The FVP-BASE recipes are located at ``<workspace>/layers/meta-arm/``.


Software Components
###################

Trusted Firmware-A
******************

Based on `Trusted Firmware-A <https://trustedfirmware-a.readthedocs.io/en/latest/>`__

+--------+----------------------------------------------------------------------------------------------------+
| Recipe | <workspace>/layers/meta-arm/meta-arm-bsp/recipes-bsp/trusted-firmware-a/trusted-firmware-a-fvp.inc |
+--------+----------------------------------------------------------------------------------------------------+
| Files  | * <workspace>/build-poky/tmp-poky/deploy/images/fvp-base/bl1-fvp.bin                               |
|        | * <workspace>/build-poky/tmp-poky/deploy/images/fvp-base/fip-fvp.bin                               |
+--------+----------------------------------------------------------------------------------------------------+

U-Boot
******

Based on `U-Boot gitlab <https://gitlab.denx.de/u-boot/u-boot>`__

+--------+-------------------------------------------------------------------------------+
| Recipe | <workspace>/layers/meta-arm/meta-arm-bsp/recipes-bsp/u-boot/u-boot_%.bbappend |
+--------+-------------------------------------------------------------------------------+
| Files  | * <workspace>/build-poky/tmp-poky/deploy/images/fvp-base/u-boot.bin           |
+--------+-------------------------------------------------------------------------------+


Linux
*****

The recipe responsible for building a 5.4 version of the Yocto Linux kernel

+--------+-----------------------------------------------------------------------------------+
| Recipe | <workspace>/layers/openembedded-core/meta/recipes-kernel/linux/linux-yocto_5.4.bb |
+--------+-----------------------------------------------------------------------------------+
| Files  | * <workspace>/build-poky/tmp-poky/deploy/images/fvp-base/Image                    |
+--------+-----------------------------------------------------------------------------------+


Poky Linux distro
*****************

The layer is based on the `poky <https://www.yoctoproject.org/software-item/poky/>`__ Linux distribution.
The provided distribution is based on BusyBox and built using glibc.

+--------+-----------------------------------------------------------------------------------------------+
| Recipe | <workspace>/layers/openembedded-core/meta/recipes-core/images/core-image-minimal.bb           |
+--------+-----------------------------------------------------------------------------------------------+
| Files  | * <workspace>/build-poky/tmp-poky/deploy/images/fvp-base/core-image-minimal-fvp-base.disk.img |
+--------+-----------------------------------------------------------------------------------------------+


Running the software on FVP
---------------------------

The run-scripts structure is as follows:

::

    run-scripts
    |--fvp
       |--run_model.sh
       |-- ...

Ensure that all dependencies are met by executing the FVP: $MODEL`. You should see
the FVP launch, presenting a graphical interface showing information about the current state of the FVP.

The ``run_model.sh`` script in ``<workspace>/run-scripts/fvp`` will launch the FVP.
Set environment variables and execute the ``run_model.sh`` as follows:

::

    export IMAGE=<workspace>/build-poky/tmp-poky/deploy/images/fvp-base/Image
    export BL1=<workspace>/build-poky/tmp-poky/deploy/images/fvp-base/bl1-fvp.bin
    export FIP=<workspace>/build-poky/tmp-poky/deploy/images/fvp-base/fip-fvp.bin
    export DISK=<workspace>/build-poky/tmp-poky/deploy/images/fvp-base/core-image-minimal-fvp-base.disk.img
    export DTB=<workspace>/build-poky/tmp-poky/deploy/images/fvp-base/fvp-base-gicv3-psci-custom.dtb

    cd <workspace>/run-scripts/fvp
    ./run_model.sh

Enable network on FVP
---------------------

To enable network on FVP, follow below steps

1. Create network bridge and add the host PC network as its interface:
::

    sudo apt-get install bridge-utils
    sudo brctl addbr br0
    sudo brctl addif br0 <host network interface name>
    sudo ifconfig <host network interface name> 0.0.0.0
    sudo ifconfig br0 up
    sudo dhclient br0

2. Add the tap interface:
::

    sudo ip tuntap add dev <bridge_interface_name> mode tap user $(whoami)
    sudo ifconfig <bridge_interface_name> 0.0.0.0 promisc up
    sudo brctl addif br0 <bridge_interface_name>

eg. 
    sudo ip link add dummy type dummy
    sudo brctl addbr br0
    sudo brctl addif br0 dummy
    sudo brctl show
    sudo ifconfig dummy 0.0.0.0
    sudo ifconfig br0 up
    sudo ifconfig br0 192.168.0.10
    sudo ip tuntap add dev arm mode tap user $(whoami)
    sudo ifconfig arm 0.0.0.0 promisc up
    sudo brctl addif br0 arm
    brctl show


3. Add below parameters in run_model.sh:
::

    -C bp.hostbridge.interfaceName=<bridge_interface_name>
    -C bp.smsc_91c111.enabled=1

4. ./run_model.sh

Build and Run AArch32 builds on Armv8-A Base Platform FVP
---------------------------------------------------------

Build: Follow the steps explained above, however set the MACHINE variable as follows:

::

    export MACHINE="fvp-base-arm32"

Note: Output files become available in the <workspace>/build-poky/tmp-poky/deploy/images/fvp-base-arm32 folder.
Set environment variables accordingly:

::

    export IMAGE=<workspace>/build-poky/tmp-poky/deploy/images/fvp-base-arm32/zImage
    export BL1=<workspace>/build-poky/tmp-poky/deploy/images/fvp-base-arm32/bl1-fvp.bin
    export FIP=<workspace>/build-poky/tmp-poky/deploy/images/fvp-base-arm32/fip-fvp.bin
    export DISK=<workspace>/build-poky/tmp-poky/deploy/images/fvp-base-arm32/core-image-minimal-fvp-base-arm32.disk.img
    export DTB=<workspace>/build-poky/tmp-poky/deploy/images/fvp-base-arm32/fvp-base-gicv3-psci-custom.dtb


Run: Pass aarch32 argument to run_model.sh

::

    ./run_model.sh --aarch32

Release Tags
------------

Here's the list of release tags and corresponding Fast Model version supported:

+-----------------------+-------------------------+
|     Release Tag       |     Base FVP Version    |
+=======================+=========================+
| BASEFVP-2020.08.06    |        11.11.34         |
+-----------------------+-------------------------+
|                       |                         |
+-----------------------+-------------------------+


--------------

*Copyright (c) 2020, Arm Limited. All rights reserved.*

