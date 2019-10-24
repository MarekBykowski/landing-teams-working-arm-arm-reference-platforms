How to build RD-Daniel and RD-Daniel-Dual platform software to validate busybox boot
====================================================================================

.. section-numbering::
    :suffix: .

.. contents::

Busybox boot on RD-Daniel and RD-Daniel-Dual platforms
------------------------------------------------------

Busybox is a lightweight executable which packages lots of POSIX compliant UNIX
utilities in a single file system. The busybox boot test on RD-Daniel and
RD-Daniel-Dual platforms ensures that the software stack which runs on the model
is able to boot a Linux operating system with a busybox filesystem.

Boot test is especially helpful when porting the software stack for new
platforms which are derivative of the RD-Daniel or RD-Daniel-Dual platform as
this test can be quickly executed to ensure that the various software components
are properly integrated and verify the basic functionality of various software
components. As part of this test, the following components of the software stack
are built - *TF-A*, *UEFI*, *Linux*, *GRUB*, *SCP*.

This document describes how to build and execute the boot test on the
*RD-Daniel* and *RD-Daniel-Dual* fastmodel.

Procedure to build Busybox boot test for RD-Daniel and RD-Daniel platform
-------------------------------------------------------------------------

This section describes how to build the disk image for busybox boot test. The
disk image consists of an EFI partition which has grub and an ext3 partition
which has the linux kernel image. Examples on how to use the build command for
busybox boot test are listed below.

To build the software stack, the command to be used is

   ::

        ./build-scripts/rdinfra/build-test-busybox.sh -p <platform> <command>

Supported command line options are listed below

   -  <platform>

      -  Supported platforms are

         -  ``rddaniel`` for RD-Daniel
         -  ``rddanielx2`` for RD-Daniel-Dual

   -  <command>

      -  Supported commands are

         -  ``clean``
         -  ``build``
         -  ``package``
         -  ``all`` (all the three above)


Examples of the build command are

   -   ::

        ./build-scripts/rdinfra/build-test-busybox.sh -p rddaniel all

      - This command cleans, builds and packages the software stack needed
        for the busybox boot test on RD-Daniel platform.

   -   ::

        ./build-scripts/rdinfra/build-test-busybox.sh -p rddanielx2 build

      - This command performs an incremental build of the software components
        included in the software stack for the RD-Daniel-Dual platform. Note:
        this command should be followed by the 'package' command to complete the
        preparation of the FIP and the disk image.

   -   ::

        ./build-scripts/rdinfra/build-test-busybox.sh -p rddaniel package

      - This command packages the previously built software stack and prepares
        the FIP and the disk image.

Procedure for validating Busybox boot test for RD-Daniel and RD-Daniel-Dual platforms
-------------------------------------------------------------------------------------

After the build for busybox boot test is complete, the following command starts
the execution of the *RD-Daniel* or *RD-Daniel* fastmodel and the software boots
up to the busybox prompt. Examples on how to use the command are listed below.

To boot up to the busybox prompt, the command to be used is

   ::

        cd model-scripts/rdinfra
        ./boot.sh -p <platform> -a <additional_params> -n [true|false]


Supported command line options are listed below

   -  -p <platform>

      - Specifies the platform to build. Supported platforms are

         -  ``rddaniel`` for RD-Daniel
         -  ``rddanielx2`` for RD-Daniel-Dual

   -  -n [true|false] (optional)

      -  Controls the use of network ports by the model. If network ports have
         to be enabled, use 'true' as the option. Default value is set to
         'false'.

   -  -a <additional_params>

      -  Specify any additional model parameters to be passed. The model
         parameters and the data to be passed to those parameters can be found
         in the FVP documentation.


Example commands to validate the Boot test are as listed below.

   -   ::

        ./boot.sh -p rddanielx2

      - This command starts the execution of the RD-Daniel-Dual model and the
        software boots up to the Busybox prompt.

   -   ::

        ./boot.sh -p rddaniel -n true

      - This command starts the execution of the RD-Daniel model and the
        software boots up to the Busybox prompt. The model supports
        networking allowing the software running within the model to access
        the network.

   -   ::

        ./boot.sh -p rddaniel -n true -a "-C board.flash0.diagnostics=1"

      - This command starts the execution of the RD-Daniel model with
        networking enabled and the software boots up to the Busybox prompt.
        Additional parameters to the model are supplied using the -a command
        line parameter.

--------------

*Copyright (c) 2019, Arm Limited. All rights reserved.*
