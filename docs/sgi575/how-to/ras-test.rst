How to build SGI-575 platform software to validate platform RAS error handling
==============================================================================


.. section-numbering::
    :suffix: .

.. contents::

What is RAS
-----------

Reliability Availability and Serviceability are three aspects that are
considered to be vital to ensure correct functioning of a server system. These
require extensive support in the platform hardware and software to ensure that
the system is producing correct results and that in a scenario where the system
encounters a malfunctioning component, the system is able to:

   -  identify and correct the error condition
   -  record and flag errors to an external component like a Board Management
      Controller (BMC)
   -  provide for mechanisms to avoid or keep to a minimum, the system downtime
      by supporting features like hot-swapping of failing components, or by
      providing for redundancy in the system hardware.

What does RAS test on SGI-575 demonstrate
-----------------------------------------

The SGI-575 platform supports multiple RAS error sources. Out of these, the
RAS error handling test validates the DMC-620 single-bit RAS error injection and
error handling of features in the platform software. The RAS error injection and
error handling requires multiple software components (kernel and firmware
components) to work in tandem in order for the RAS errors to be detected and
propogated to the kernel. This RAS test demonstrates the error injection and
error handling of the DMC-620 single-bit RAS error.

Procedure to build RAS test for SGI-575 platform
------------------------------------------------

The SGI-575 platform demonstrates the RAS feature by injecting a memory error
using RAS simulation capabilities in the DMC-620 controller. The RAS support
consists of the following components:

-  The DMC RAS driver. The driver executes as part of the S-EL0 Management Mode
   and provides DMC RAS error handling and reporting.
-  The TF-A SPM and SDEI modules which are responsible for handling system
   interrupts and sending notifications to the DMC RAS driver and the Linux
   kernel.
-  APEI driver used to retrieve the system RAS errors from S-EL0 Management mode
   code. This information is then used to populate the HEST ACPI table, for
   future consumption by the Linux kernel.
-  CPER Library which is used by individual RAS error handling drivers to
   populate the CPER record with relevant data, to be passed on to the Linux
   kernel on the non-secure side.
-  The Linux kernel SDEI client which is part of the kernel ACPI APEI
   notification mechanism.

Execution of the RAS test requires booting a Fedora distribution system with the
kernel containing changes needed for the RAS test. The first step would be to
get a installed Fedora distribution satadisk image. After the Fedora SATA disk
image has been prepared, the Fedora.satadisk image file is created under the
prebuilts/refinfra directory. Now, build the firmware components and the kernel
image needed for running the RAS test. For generation of these image, the build
command to be used is listed below.

To build the SGI-575 software stack, the command to be used is

   ::

        ./build-scripts/sgi/build-test-ras.sh -p sgi575 <command>

Supported command line options are listed below

   -  <command>

      -  Supported commands are

         -  clean
         -  build
         -  package
         -  all (all the three above)


Examples of the build command are

   -   ::

        ./build-scripts/sgi/build-test-ras.sh -p sgi575 all

      - This command cleans, builds and packages the SGI-575 software stack
        needed for the RAS test for SGI-575 platform.

   -   ::

        ./build-scripts/sgi/build-test-ras.sh -p sgi575 build

      - This command performs an incremental build of the software components
        included in the software stack for the SGI-575 platform. Note: this
        command should be followed by the 'package' command to complete the
        preparation of the fip and the disk image.

   -   ::

        ./build-scripts/sgi/build-test-ras.sh -p sgi575 package

      - This command packages the previously build software stack and prepares
        the fip and the disk image.

Procedure for validating RAS test for SGI-575 platform
------------------------------------------------------

After the build for the RAS test is complete, to boot upto the Fedora login
prompt using the SGI-575 software stack, the command to be used is

   ::

        cd model-scripts/sgi
        ./ras.sh -p sgi575 -n [true|false] -a <additional_params>


Supported command line options are listed below

   -  -n [true|false] (optional)

      -  Controls the use of network ports by the model. If network ports have
         to be enabled, use 'true' as the option. Default value is set to
         'false'.

   -  -a <additional_params> (optional)

      -  Specify any additional model parameters to be passed. The model
         parameters and the data to be passed to those parameters can be found
         in the FVP documentation.


Example commands to validate the RAS functionality are as listed below.

   -   ::

        ./ras.sh -p sgi575

      - This command starts the execution of the SGI-575 model and the software
        boots upto the Fedora login prompt.

   -   ::

        ./ras.sh -p sgi575 -n true

      - This command starts the execution of the SGI-575 model and the software
        boots upto the Fedora login prompt. The model supports networking
        allowing the software running within the model to access the network.

   -   ::

        ./ras.sh -p sgi575 -n true -a "-C board.flash0.diagnostics=1"

      - This command starts the execution of the SGI-575 model with networking
        enabled and the software boots upto the Fedora login prompt. Additional
        parameters to the model are supplied using the -a command line
        parameter.


During the system boot, select the 'Fedora (refinfra) 27 (Server Edition)'
kernel on the grub menu. On a successful login into Fedora, execute the
following command on the Fedora shell prompt to inject the DMC-620 single-bit
RAS error.

   ::

        'echo 0x123 > /sys/kernel/debug/sdei_ras_poison'

On execution of this command, the error record dump, known as CPER dump would be
seen on the Fedora terminal's console, similar to the sample dump shown below.

   ::

        [115792.848999] ghes_edac: Internal error: Can't find EDAC structure
        [115792.849003] [Firmware Warn]: GHES: Invalid address in generic error data: 0x1f03fedcd
        [115792.849008] {1}[Hardware Error]: Hardware error from APEI Generic Hardware Error Source: 1
        [115792.849013] {1}[Hardware Error]: event severity: recoverable
        [115792.849017] {1}[Hardware Error]: Error 0, type: corrected
        [115792.849021] {1}[Hardware Error]: fru_id: 00000000-0000-0000-0000-000000000000
        [115792.849025] {1}[Hardware Error]: fru_text:
        [115792.849029] {1}[Hardware Error]: section_type: memory error
        [115792.849033] {1}[Hardware Error]: physical_address: 0x00000001f03fedcd
        [115792.849038] {1}[Hardware Error]: physical_address_mask: 0xfffffffffffff000
        [115792.849042] {1}[Hardware Error]: error_type: 8, parity error

This completes the validation of the RAS functionality.

--------------

*Copyright (c) 2019, Arm Limited. All rights reserved.*
