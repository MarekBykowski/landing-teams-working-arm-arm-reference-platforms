How to build SGI-575 platform software and execute Arm ACS test suite
=====================================================================


.. section-numbering::
    :suffix: .

.. contents::

What is Arm ACS
---------------

Architecture Compliance Suite (ACS) is used to ensure architectural compliance
across different implementations of the architecture. Arm Enterprise ACS
includes a set of examples of the invariant behaviours that are provided by a
set of specifications for enterprise systems (e.g. SBSA, SBBR, etc.), so that
implementers can verify if these behaviours have been interpreted correctly.
ACS is delivered with tests in source form along with a build script, the output
of the build being a bootable Linux UEFI Validation (LUV) OS image that can run
all tests required by these specifications.

What does ACS test on SGI-575 demonstrate
-----------------------------------------

SGI-575 platform is targetted for enterprise and network infrastructure
use cases. This requires the SGI-575 platform to be compliant to the various
architectural specifications such as SBSA and SBBR. The ACS test on SGI-575
platform helps with building the platform firmware stack and ACS test suite
and then validating the same on the SGI-575 platform. The test results are
stored on the luv-live disk image which can be retrived from this disk. The
results can then be looked into to determine the conformance to the SBSA and
SBBR standards.

Procedure to build ACS test for SGI-575 platform
------------------------------------------------

The procedure to build the ACS test suite along the SGI-575 platform software
stack is listed below. The components of the SGI-575 platform software stack
that are built is limited to those that provide the EFI implementation and the
EFI shell on the SGI-575 platforms (i.e, SCP, TF-A and EDK2).

To build the SGI-575 software stack, ACS tests and to prepares the disk image,
the command to be used is

   ::

        ./build-scripts/build-test-acs.sh -p sgi575 <command>

Supported command line options are listed below

   -  <command>

      -  Supported commands are

         -  clean
         -  build
         -  package
         -  all (all the three above)


Examples of the build command are

   -   ::

        ./build-scripts/build-test-acs.sh -p sgi575 all

      - This command cleans, builds and packages the SGI-575 software stack
        required for the ACS test on SGI-575 platform. The ACS test suite is
        also built from source.

   -   ::

        ./build-scripts/build-test-acs.sh -p sgi575 build

      - This command performs an incremental build of the software components
        included in the software stack for ACS test on the SGI-575 platform.
        Note: this command should be followed by the 'package' command to
        complete the preparation of the fip and the luv-live disk image.

   -   ::

        ./build-scripts/build-test-acs.sh -p sgi575 package

      - This command packages the previously build software stack and prepares
        the fip and the luv-live disk image.

The above build command includes steps to build the ACS test suite from the
source. In case it is desired to use a pre-built image of the ACS test
luv-live disk image, the build can be restricted to the platform software
firmware components such as SCP, TF-A and EDK2. The command to be used to
build the firmware components but not ACS test suite from the source is

   ::

        ./build-scripts/build-test-uefi.sh -p sgi575 <command>

Supported command line options are listed below

   -  <command>

      -  Supported commands are

         -  clean
         -  build
         -  package
         -  all (all the three above)


Examples of the build command are

   -   ::

        ./build-scripts/build-test-uefi.sh -p sgi575 all

      - This command cleans, builds and packages the SGI-575 software stack
        required for the ACS test on SGI-575 platform.

   -   ::

        ./build-scripts/build-test-uefi.sh -p sgi575 build

      - This command performs an incremental build of the software components
        included in the software stack for ACS test on the SGI-575 platform.
        Note: this command should be followed by the 'package' command to
        complete the preparation of the fip image.

   -   ::

        ./build-scripts/build-test-uefi.sh -p sgi575 package

      - This command packages the previously build software stack and prepares
        the fip image.


Procedure for executing ACS test for SGI-575 platform
-----------------------------------------------------

The procedure to execute the ACS test cases on the SGI-575 platform is listed
below.

   ::

        cd model-scripts/sgi
        ./acs.sh -p sgi575 -v <path to luv-live image> -n [true|false] -a <additional_params>


Supported command line options are listed below

   -  -v <absolute path to the luv-live prebuilt image> (optional)

      -  Allows use of a pre-built luv-live image for the test. The absolute
         path to the luv-live image has be supplied as the parameter. This
         parameter is optional, and if not specified, the luv-live image is
         picked up from the location into which the images are packaged by the
         build command.

   -  -n [true|false] (optional)

      -  Controls the use of network ports by the model. If network ports have
         to be enabled, use 'true' as the option. Default value is set to
         'false'.

   -  -a <additional_params> (optional)

      -  Specify any additional model parameters to be passed. The model
         parameters and the data to be passed to those parameters can be found
         in the FVP documentation.


Example commands to execute the ACS tests are as listed below.

   -   ::

        ./acs.sh -p sgi575

      - This command starts the execution of the SGI-575 model and the ACS tests
        are executed. The luv-live image is picked up from the location
        ./output/sgi575/luv-live-image-gpt.img.

   -   ::

        ./acs.sh -p sgi575 -v /tmp/luv-live-image-gpt.img

      - This command starts the execution of the SGI-575 model and the ACS tests
        are executed. The luv-live image is picked up from the location
        ./tmp/luv-live-image-gpt.img.

   -   ::

        ./acs.sh -p sgi575 -n true -a "-C board.flash0.diagnostics=1"

      - This command starts the execution of the SGI-575 model with networking
        enable and the ACS tests are executed. The luv-live image is picked up
        from the location ./output/sgi575/luv-live-image-gpt.img. Additional
        parameters to the model are supplied using the -a command line
        parameter.

--------------

*Copyright (c) 2019, Arm Limited. All rights reserved.*
