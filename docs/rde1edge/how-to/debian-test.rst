How to build RD-E1-Edge platform software to install and boot Debian distribution
=================================================================================

.. section-numbering::
    :suffix: .

.. contents::


Debian distribution boot support
--------------------------------
RD-E1-Edge software stack supports the installation and boot of Debian 9.8
Stretch Distribution (Debian 9.8 Distribution). The Debian distribution is
installed on a SATA disk and the installed image can be used for multiple boots.


Procedure to build RD-E1-Edge software stack for debian boot
------------------------------------------------------------

The RD-E1-Edge platform software stack has to be first built to prepare for the
debian distribution installation step. The procedure to execute the RD-E1-Edge
platform stack is listed below.

To build the RD-E1-Edge software stack, the command to be used is

   - ::

      ./build-scripts/build-test-uefi.sh -p rde1edge <command>

   - Supported command line options are listed below

      -  <command>

         -  ``clean``
         -  ``build``
         -  ``package``
         -  ``all`` (all the three above)


An example of the command to begin the installation of the debian distribution
is listed below.

   -   ::

        ./build-scripts/build-test-uefi.sh -p rde1edge all

      - This command cleans, builds and packages the RD-E1-Edge software stack
        needed for the Debian installation/boot test for RD-E1-Edge platform.

   -   ::

        ./build-scripts/build-test-uefi.sh -p rde1edge build

      - This command performs an incremental build of the software components
        included in the software stack for the RD-E1-Edge platform. Note: this
        command should be followed by the ``package`` command to complete the
        preparation of the FIP image.

   -   ::

        ./build-scripts/build-test-uefi.sh -p rde1edge package

      - This command packages the previously built software stack and prepares
        the FIP image.


Procedure for installing Debian distro on RD-E1-Edge platform
-------------------------------------------------------------

After the build for the distro is complete, Debian can be installed into a
SATA disk image. Before beginning the installation process download the iso
image of the required debian version. For example, Debian 9.8 Strech CD ISO
image can be downloaded from `here <https://cdimage.debian.org/debian-cd/current/arm64/iso-cd/>`_
or with this `direct link <https://cdimage.debian.org/debian-cd/current/arm64/iso-cd/debian-9.8.0-arm64-xfce-CD-1.iso>`_.

The command used to begin the distro installation is:

   ::

    cd model-scripts/rdinfra
    ./distro.sh -p rde1edge -i <iso_image_path> -s <disk size> -a <additional_params> -n [true|false]

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


An example of the command to begin the boot of the debian distribution is
listed below.

   -   ::

        ./distro.sh -p rde1edge -i ./debian-9.8.0-arm64-xfce-CD-1.iso -s 4

      - This command creates a 4GB SATA disk image, boots the RD-E1-Edge
        software stack and start the installation of debian distro.

      - The RD-E1-Edge platform supports a total of 8GB of DDR memory out of
        which 6GB of memory is located above the 32-bit memory space. The debian
        installation fails if the upper 6GB is enabled. To disable the use of
        the upper 6GB, at the grub menu displayed during the installation,
        edit the kernel boot parameters as below for enabling earlycon output
        and limiting the DDR memory to 2032MB (2GB - 16MB) for SATA disk
        detection.

        ::

         setparams 'Install'
         set background_color=black
         linux /install.a64/vmlinuz mem=2032M earlycon=pl011,0x7ff80000 console=ttyAMA0,115200
         initrd /intsall.a64/initrd.gz

      - From here on, follow the instructions of the Debian installer. For more
        information about the installation procedure, please refer this
        `link <https://www.debian.org/releases/stable/arm64/index.html.en>`_.

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

      - After the installation is completed, the disk image with a random name
        "<number>.satadisk" will be created in model-scripts/rdinfra/ folder.
        User should use this disk image when booting the Debian distribution.


Procedure for booting Debian distro on RD-E1-Edge platform
----------------------------------------------------------

To boot the debian distro, use the following command:

   ::

    cd model-scripts/rdinfra
    ./distro.sh -p rde1edge -d <satadisk_path> -a <additional_params> -n [true|false]

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


Example commands are as listed below.

   -   ::

        ./distro.sh -p rde1edge

      - This command looks for the available .satadisk image in the
        ``model-scripts/rdinfra`` folder and boots with that image. If multiple
        .satadisk images are found, it will list them all but won't boot.

   -   ::

        ./distro.sh -p rde1edge -d ./debian.satadisk

      -  This command begins the distro boot from the ``debian.satadisk`` image.

   - During boot, at the grub menu, edit the kernel boot parameters as below for
     enabling earlycon output and limiting the DDR memory to 2032MB for
     SATA disk detection

        ::

         setparams 'Install'
         set background_color=black
         linux /install.a64/vmlinuz mem=2032M earlycon=pl011,0x7ff80000 console=ttyAMA0,115200
         initrd /intsall.a64/initrd.gz

     Save and exit the grub menu. The boot will then continue up to the login
     prompt.


This completes the validation of the Debian distribution installation and boot
functionalities.

--------------

*Copyright (c) 2019, Arm Limited. All rights reserved.*
