How to build SGI-575 platform software to validate busybox boot
===============================================================

.. section-numbering::
    :suffix: .

.. contents::

Busybox boot on SGI-575 platform
--------------------------------

Busybox is a lightweight executable which packages lots of POSIX compliant UNIX
utilities in a single file system. The busybox boot test on SGI-575 platform
ensures that the SGI-575 software stack which runs on the model is able to boot
a Linux operating system with a busybox filesystem.

Boot test is especially helpful when porting the software stack for new
platforms which are derivative of the SGI-575 platform as this test can be
quickly executed to ensure that the various software components are properly
integrated and verify the basic functionality of various software components.
As part of this test, the following components of the software stack are built -
*TF-A*, *UEFI*, *Linux*, *GRUB*, *SCP*.

This document describes how to build and execute the Boot test on the *SGI-575*
fastmodel.

Procedure to build Busybox boot test for SGI-575 platform
---------------------------------------------------------

This section describes how to build the disk image for busybox boot test. The
disk image consists of an EFI partition which has grub and an ext3 partition
which has the linux kernel image. Examples on how to use the build command for
busybox boot test are listed below.

To build the SGI software stack, the command to be used is

   ::

        ./build-scripts/sgi/build-test-busybox.sh -p sgi575 <command>

Supported command line options are listed below

   -  <command>

      -  Supported commands are

         -  clean
         -  build
         -  package
         -  all (all the three above)


Examples of the build command are

   -   ::

        ./build-scripts/sgi/build-test-busybox.sh -p sgi575 all

      - This command cleans, builds and packages the SGI software stack needed
        for the busybox boot test on SGI-575 platform.

   -   ::

        ./build-scripts/sgi/build-test-busybox.sh -p sgi575 build

      - This command performs an incremental build of the software components
        included in the software stack for the SGI-575 platform. Note: this
        command should be followed by the 'package' command to complete the
        preparation of the FIP and the disk image.

   -   ::

        ./build-scripts/sgi/build-test-busybox.sh -p sgi575 package

      - This command packages the previously built software stack and prepares
        the FIP and the disk image.

Procedure for validating Busybox boot test for SGI-575 platform
---------------------------------------------------------------

After the build for busybox boot test is complete, the following command starts
the execution of the *SGI-575* fastmodel and the software boots up to the
Busybox prompt. Examples on how to use the command are listed below.

To boot up to the Busybox prompt, the command to be used is

   ::

        cd model-scripts/sgi
        ./boot.sh -p sgi575 -a <additional_params> -n [true|false]


Supported command line options are listed below

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

        ./boot.sh -p sgi575

      - This command starts the execution of the SGI-575 model and the software
        boots up to the Busybox prompt.

   -   ::

        ./boot.sh -p sgi575 -n true

      - This command starts the execution of the SGI-575 model and the
        software boots up to the Busybox prompt. The model supports
        networking allowing the software running within the model to access
        the network.

   -   ::

        ./boot.sh -p sgi575 -n true -a "-C board.flash0.diagnostics=1"

      - This command starts the execution of the SGI-575 model with networking
        enabled and the software boots up to the Busybox prompt. Additional
        parameters to the model are supplied using the -a command line
        parameter.

--------------

*Copyright (c) 2019, Arm Limited. All rights reserved.*
