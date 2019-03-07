How to build SGI-575 platform software to install and boot Fedora distribution
==============================================================================

.. section-numbering::
    :suffix: .

.. contents::


Fedora distribution boot support
--------------------------------
SGI-575 software stack supports the installation and boot of Fedora Enterprise
Server Distribution (Fedora 27 Distribution). The Fedora distribution is
installed on a SATA disk and the installed image can be used for multiple boots.


Procedure to build SGI-575 software stack for Fedora boot
---------------------------------------------------------

The SGI-575 platform software stack has to be first built to prepare for the
Fedora distribution installation step. The procedure to execute the SGI-575
platform stack is listed below.

To build the SGI-575 software stack, the command to be used is

   - ::

      ./build-scripts/build-test-uefi.sh -p sgi575 <command>

   - Supported command line options are listed below

      -  <command>

         -  ``clean``
         -  ``build``
         -  ``package``
         -  ``all`` (all the three above)


An example of the command to begin the installation of the Fedora distribution
is listed below.

   -   ::

        ./build-scripts/build-test-uefi.sh -p sgi575 all

      - This command cleans, builds and packages the SGI-575 software stack
        needed for the Fedora installation/boot test for SGI-575 platform.

   -   ::

        ./build-scripts/build-test-uefi.sh -p sgi575 build

      - This command performs an incremental build of the software components
        included in the software stack for the SGI-575 platform. Note: this
        command should be followed by the ``package`` command to complete the
        preparation of the fip image.

   -   ::

        ./build-scripts/build-test-uefi.sh -p sgi575 package

      - This command packages the previously build software stack and prepares
        the fip image.


Procedure for installing Fedora distro on SGI-575 platform
----------------------------------------------------------

After the build for the distro is complete, Fedora can be installed into a
SATA disk image. Before beginning the installation process download the iso
image of the required Fedora version. For example, the Fedora distribution iso image
has to be downloaded from `here <https://dl.fedoraproject.org/pub/fedora-secondary/releases/27/Server/aarch64/iso/>`_
or with this `direct link <https://dl.fedoraproject.org/pub/fedora-secondary/releases/27/Server/aarch64/iso/Fedora-Server-dvd-aarch64-27-1.6.iso>`_.

The command used to begin the distro installation is:

   ::

    cd model-scripts/sgi
    ./distro.sh -p sgi575 -i <iso_image_path> -s <disk size> -a <additional_params> -n [true|false]

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


An example of the command to begin the boot of the Fedora distribution is
listed below.

   -   ::

        ./distro.sh -p sgi575 -i ./Fedora-Server-dvd-aarch64-27-1.6.iso -s 4

      - This command creates a 4GB SATA disk image, boot the SGI-575 software
        stack and start the installation of Fedora distro.

      - From here on, follow the instructions of the Fedora installer. For more
        information about the installation procedure, please refer this
        `link <https://docs.fedoraproject.org/en-US/index.html>`_.

      - After the installation is completed, the disk image with a random name
        "<number>.satadisk" will be created in model-scripts/sgi/ folder. User
        should use this disk image when booting the Fedora distribution.


Procedure for booting Fedora distro on SGI-575 platform
-------------------------------------------------------

To boot the Fedora distro, use the following command:

   ::

    cd model-scripts/sgi
    ./distro.sh -p sgi575 -d <satadisk_path> -a <additional_params> -n [true|false]

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

        ./distro.sh -p sgi575

      - This command looks for the available .satadisk image in the
        ``model-scripts/sgi`` folder and boots with that image. If multiple
        .satadisk images are found, it will list them all but won't boot.

   -   ::

        ./distro.sh -p sgi575 -d ./fedora.satadisk

      -  This command begins the distro boot from the ``fedora.satadisk`` image.

This completes the validation of the Fedora distribution installation and boot
functionalities.

--------------

*Copyright (c) 2019, Arm Limited. All rights reserved.*
