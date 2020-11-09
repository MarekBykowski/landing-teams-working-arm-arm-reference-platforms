How to boot WinPE
=================

.. section-numbering::
    :suffix: .

.. contents::


WinPE boot support
------------------
RD-Daniel software stack supports the boot of Windows Preinstallation
Environment (WinPE). A pre-built WinPE disk image is provided as a SATA disk to
RD-Daniel FVP which then is used to boot WinPE.


Procedure to build RD-Daniel software stack for WinPE boot
----------------------------------------------------------

The RD-Daniel platform software stack has to be first built to prepare for the
WinPE boot. The procedure to build the RD-Daniel platform stack is listed below.

To build the RD-Daniel software stack, the command to be used is

   - ::

      ./build-scripts/build-test-uefi.sh -p <platform> <command>

Supported command line options are listed below

   -  <platform>

      -  Supported platforms are

         -  ``rddaniel`` for RD-Daniel
         -  ``rddanielxlr`` for RD-Daniel-XLR

      -  <command>

         -  ``clean``
         -  ``build``
         -  ``package``
         -  ``all`` (all the three above)


Examples of the build command are

   -   ::

        ./build-scripts/build-test-uefi.sh -p rddaniel all

      - This command cleans, builds and packages the RD-Daniel Config-M software
        stack needed for the WinPE boot for the RD-Daniel Config-M platform.

   -   ::

        ./build-scripts/build-test-uefi.sh -p rddanielxlr build

      - This command performs an incremental build of the software components
        included in the software stack for the RD-Daniel Config-XLR platform.
        Note: this command should be followed by the ``package`` command to
        complete the preparation of the fip image.

   -   ::

        ./build-scripts/build-test-uefi.sh -p rddanielxlr package

      - This command packages the previously built software stack and prepares
        the fip image.


Procedure for preparing a WinPE disk image
------------------------------------------

To prepare a WinPE disk image, follow the instructions listed on this page -
`Boot to WinPE <https://docs.microsoft.com/en-us/windows-hardware/manufacture/desktop/download-winpe--windows-pe/>`_

Procedure for booting WinPE on RD-Daniel platform
-------------------------------------------------

To boot from the WinPE disk image, use the following command:

   ::

    cd model-scripts/rdinfra
    ./distro.sh -p <platform> -d <satadisk_path> -a <additional_params> -n [true|false]

Supported command line options are listed below

   -  -p <platform>

      - Specifies the platform to build. Supported platforms are

         -  ``rddaniel`` for RD-Daniel
         -  ``rddanielxlr`` for RD-Daniel-XLR

   -  -d <satadisk_path>

      -  Absolute path to the WinPE disk image created using the previous section.

   -  -n [true|false] (optional)

      -  Controls the use of network ports by the model. If network ports have
         to be enabled, use 'true' as the option. Default value is set to
         'false'.

   -  -a <additional_params>

      -  Specify any additional model parameters to be passed. The model
         parameters and the data to be passed to those parameters can be found
         in the FVP documentation.


Example command  functionality are as listed below.

   -   ::

        ./distro.sh -p rddaniel -d /path/to/WinPE_arm64.iso

      -  This command begins the WinPE boot from the ``WinPE_arm64.iso`` image.
         Follow the instructions on console to complete the WinPE boot.


This completes the validation of WinPE boot on RD-Daniel platform.

--------------

*Copyright (c) 2020, Arm Limited. All rights reserved.*
