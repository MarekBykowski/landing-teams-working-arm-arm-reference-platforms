How to install and boot a linux distribution
============================================

.. section-numbering::
    :suffix: .

.. contents::


Linux distribution boot support
--------------------------------
RD-Daniel software stack supports the installation and boot of various linux
distributions such as Debian, Fedora or Ubuntu. The distribution is installed
on a SATA disk and the installed image can be used for multiple boots.


Procedure to build RD-Daniel software stack for distro boot
-----------------------------------------------------------

The RD-Daniel platform software stack has to be first built to prepare for the
distribution installation step. The procedure to build the RD-Daniel platform
software stack is listed below.

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
        stack needed for the distro installation/boot test for the RD-Daniel
        Config-M platform.

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


Procedure for installing a distro on RD-Daniel platform
-------------------------------------------------------

After the build for the distro is complete, a distribution can be installed into
a SATA disk image. Before beginning the installation process, download the CD
iso image of the required distribution version.

The command used to begin the distro installation is:

   ::

    cd model-scripts/rdinfra
    ./distro.sh -p <platform> -i <iso_image_path> -s <disk size> -a <additional_params> -n [true|false]

Supported command line options are listed below

   -  -p <platform>

      - Specifies the platform to build. Supported platforms are

         -  ``rddaniel`` for RD-Daniel
         -  ``rddanielxlr`` for RD-Daniel-XLR

   -  -i </path/to/iso_image_path>

      -  Absolute path to the downloaded distribution installer iso image.

   -  -s <disk_size>

      -  Size of the SATA disk image (in GB) to be created. 16GB and above is
         good enough for most use cases.

   -  -n [true|false] (optional)

      -  Controls the use of network ports by the model. If network ports have
         to be enabled, use 'true' as the option. Default value is set to
         'false'.

   -  -a <additional_params>

      -  Specify any additional model parameters to be passed. The model
         parameters and the data to be passed to those parameters can be found
         in the FVP documentation.


An example of the command to begin the boot of the debian distribution is
listed below.

   -   ::

        ./distro.sh -p rddaniel -i /path/to/debian-10.6.0-arm64-xfce-CD-1.iso -s 16

      - This command creates a 16GB SATA disk image, boot the RD-Daniel Config-M
        software stack and start the installation of debian distro.

      - From here on, follow the instructions of the choosen distribution installer.
        For more information about the installation procedure, refer online
        installation manuals of the choose distribution.
       
      - After the installation is completed, the disk image with a random name
        "<number>.satadisk" will be created in model-scripts/rdinfra/ folder.
        User should use this disk image when booting the Debian distribution.

Additional distribution specific instructions (if any)

   -  Debian Distribution installation

      - During installation, the installer will prompt the user with the message
        'Load CD-ROM drivers from removable media' and display two options -
        Yes/No.

             - Select the option 'No' which would again display two options
               - Yes/No.
             - Select the option 'Yes' which will display 'Automatic detection
               did not find CD-ROM'.
             - Module needed for accessing CD-ROM and display two options -
                   - none
                   - cdrom

             - Select the option 'none' and enter ``/dev/vda``. The installation
               media on the virtio disk will be detected and installation
               continues.


Procedure for booting distro on RD-Daniel platform
--------------------------------------------------

To boot the installed distro, use the following command:

   ::

    cd model-scripts/rdinfra
    ./distro.sh -p <platform> -d <satadisk_path> -a <additional_params> -n [true|false]

Supported command line options are listed below

   -  -p <platform>

      - Specifies the platform to build. Supported platforms are

         -  ``rddaniel`` for RD-Daniel
         -  ``rddanielxlr`` for RD-Daniel-XLR

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

        ./distro.sh -p rddaniel

      - This command looks for the available .satadisk image in the
        ``model-scripts/rdinfra`` folder and boots with that image. If multiple
        .satadisk images are found, it will list them all but won't boot.

   -   ::

        ./distro.sh -p rddaniel -d ./fedora.satadisk

      -  This command begins the distro boot from the ``fedora.satadisk`` image.


This completes the validation of the linux distribution installation and boot
functionalities.

--------------

*Copyright (c) 2020, Arm Limited. All rights reserved.*
