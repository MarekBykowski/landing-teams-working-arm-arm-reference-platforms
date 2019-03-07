How to build RD-N1-Edge platform software to install and boot Red Hat distribution
==================================================================================

.. section-numbering::
    :suffix: .

.. contents::


Red Hat distribution boot support
---------------------------------
RD-N1-Edge software stack supports the installation and boot of Red Hat Enterprise
Server Distribution (RHEL 7.4 Distribution). The Red Hat distribution is
installed on a SATA disk and the installed image can be used for multiple boots.


Procedure to build RD-N1-Edge software stack for Red Hat boot
-------------------------------------------------------------

The RD-N1-Edge platform software stack has to be first built to prepare for the
Red Hat distribution installation step. The procedure to execute the RD-N1-Edge
platform stack is listed below.

To build the RD-N1-Edge software stack, the command to be used is

   - ::

      ./build-scripts/build-test-uefi.sh -p rdn1edge <command>

   - Supported command line options are listed below

      -  <command>

         -  ``clean``
         -  ``build``
         -  ``package``
         -  ``all`` (all the three above)


An example of the command to begin the installation of the Red Hat distribution
is listed below.

   -   ::

        ./build-scripts/build-test-uefi.sh -p rdn1edge all

      - This command cleans, builds and packages the RD-N1-Edge software stack
        needed for the Red Hat installation/boot test for RD-N1-Edge platform.

   -   ::

        ./build-scripts/build-test-uefi.sh -p rdn1edge build

      - This command performs an incremental build of the software components
        included in the software stack for the RD-N1-Edge platform. Note: this
        command should be followed by the ``package`` command to complete the
        preparation of the fip image.

   -   ::

        ./build-scripts/build-test-uefi.sh -p rdn1edge package

      - This command packages the previously build software stack and prepares
        the fip image.


Procedure for installing Red Hat distro on RD-N1-Edge platform
--------------------------------------------------------------

After the build for the distro is complete, Red Hat can be installed into a
SATA disk image. Before beginning the installation process, contact Red Hat to
obtain the RHEL 7.4 DVD installer image for AArch64 platform.

The command used to begin the distro installation is:

   ::

    cd model-scripts/rdinfra
    ./distro.sh -p rdn1edge -i <iso_image_path> -s <disk size> -a <additional_params> -n [true|false]

Supported command line options are listed below

   -  -i <iso_image_path>

      -  Path to the downloaded installer iso image.

   -  -s <disk_size>

      -  Size of the SATA disk image (in GB) to be created. 4GB and above is
         good enough for most use cases.

   -  -n [true|false] (optional)

      -  Controls the use of network ports by the model. If network ports have
         to be enabled, use 'true' as the option. Default value is set to
         'false'.

   -  -a <additional_params>

      -  Specify any additional model parameters to be passed. The model
         parameters and the data to be passed to those parameters can be found
         in the FVP documentation.


An example of the command to begin the boot of the Red Hat distribution is
listed below.

   -   ::

        ./distro.sh -p rdn1edge -i ./RHEL-ALT-7.4-20171030.0-Server-aarch64-dvd1.iso -s 4

      - This command creates a 4GB SATA disk image, boot the RD-N1-Edge software
        stack and start the installation of Red Hat distro.

      - From here on, follow the instructions of the Red Hat installer. For more
        information about the installation procedure, please refer this
        `link <https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/>`_.

      - After the installation is completed, the disk image with a random name
        "<number>.satadisk" will be created in model-scripts/rdinfra/ folder. User
        should use this disk image when booting the Red Hat distribution.


Procedure for booting Red Hat distro on RD-N1-Edge platform
-----------------------------------------------------------

To boot the Red Hat distro, use the following command:

   ::

    cd model-scripts/rdinfra
    ./distro.sh -p rdn1edge -d <satadisk_path> -a <additional_params> -n [true|false]

Supported command line options are listed below

   -  -d <satadisk_path>

      -  Path to the installed SATA disk image created using the previous
         section.

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

        ./distro.sh -p rdn1edge

      - This command looks for the available .satadisk image in the
        ``model-scripts/rdinfra`` folder and boots with that image. If multiple
        .satadisk images are found, it will list them all but won't boot.

   -   ::

        ./distro.sh -p rdn1edge -d ./redhat.satadisk

      -  This command begins the distro boot from the ``redhat.satadisk`` image.

This completes the validation of the Red Hat distribution installation and boot
functionalities.

--------------

*Copyright (c) 2019, Arm Limited. All rights reserved.*
