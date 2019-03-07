How to build SGI-575 platform software to install and boot Ubuntu distribution
==============================================================================

.. section-numbering::
    :suffix: .

.. contents::


Ubuntu distribution boot support
--------------------------------
SGI-575 software stack supports the installation and boot of Ubuntu 18.04 Bionic
distribution. The Ubuntu distribution is installed on a SATA disk and the
installed image can be used for multiple boots.


Procedure to build SGI-575 software stack for Ubuntu boot
---------------------------------------------------------

The SGI-575 platform software stack has to be first built to prepare for the
Ubuntu distribution installation step. The procedure to execute the SGI-575
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


An example of the command to begin the installation of the Ubuntu distribution
is listed below.

   -   ::

        ./build-scripts/build-test-uefi.sh -p sgi575 all

      - This command cleans, builds and packages the SGI-575 software stack
        needed for the Ubuntu installation/boot test for SGI-575 platform.

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


Procedure for installing Ubuntu distro on SGI-575 platform
----------------------------------------------------------

Ubuntu installer supports installation only through a CDROM disk. Hence, the
Ubuntu installation disk (ISO image) cannot be used with the SGI-575 model. As
an alternate, Ubuntu can be installed through the PXE boot with the help of
the network installer which can be downloaded from `here <http://ports.ubuntu.com/ubuntu-ports/dists/bionic-updates/main/installer-arm64/current/images/netboot/netboot.tar.gz>`_.
Refer the `steps to setup PXE server`_ before beginning the installation.

The following steps can be followed to begin the installation process.

Create an empty disk image on which the Ubuntu installation will be done.

        ::

          cd model-scripts/sgi
          dd if=/dev/zero of=<disk_image_name>.satadisk bs=1G count=<size in GB>

        - For example, use the following command to create a disk size of 4GB

                ::

                  dd if=/dev/zero of=ubuntu_pxe.satadisk bs=1G count=4

The command to begin the installation is:

        ::

          ./distro.sh -p sgi575 -d <disk_image_name> -n [true|false] -a <additional_params>


Supported command line options are listed below

   -  -d <disk_image_path>

      -  Path to the created disk image on which Ubuntu will be installed.

   -  -n [true|false]

      -  Controls the use of network ports by the model. Since this installation
         has to be done through the network, this must be set to 'true'.

   -  -a <additional_params>

      -  Specify any additional model parameters to be passed. The model
         parameters and the data to be passed to those parameters can be found
         in the FVP documentation.


An example of the command to begin the boot of the Ubuntu distribution is
listed below.

   -   ::

        ./distro.sh -p sgi575 -d ./ubuntu_pxe.satadisk -n true

      - This command will start the SGI-575 model and loads the edk2 firmware.

      - After the console reaches loading of Tianocore edk2 firmware, press
        escape to enter the UEFI menu and select the Boot Manager option. If
        PXE setup is done correctly, you will see an option
        ``UEFI PXEv4 (Mac:<random-mac-address>)``. Select the UEFI PXEv4 option
        to continue the PXE boot. After few seconds, the model will acquire IP
        address and find the tftp sever.

      - The SGI-575 platform supports a total of 8GB of DDR memory out of which
        6GB of memory is located above the 32-bit memory space. The Ubuntu
        installation fails if the upper 6GB is enabled. To disable the use of
        the upper 6GB, at the grub menu displayed during the installation,
        edit the kernel boot parameters as below limiting the DDR memory to
        2032MB (2GB - 16MB) for SATA disk detection.

                ::

                 setparams 'Install'
                 set background_color=black
                 linux /ubuntu-installer/arm64/linux ---quiet ip=dhcp mem=2032m
                 initrd /ubuntu-installer/arm64/initrd.gz



      - From here on, follow the instructions of the Ubuntu installer. For more
        information about the installation procedure, please refer this
        `link <https://help.ubuntu.com/lts/installation-guide/arm64/ch06s03.html>`_.


Procedure for booting Ubuntu distro on SGI-575 platform
-------------------------------------------------------

To boot the Ubuntu distro, use the following command:

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

        ./distro.sh -p sgi575 -d ./ubuntu_pxe.satadisk

      -  This command begins the distro boot from the ``ubuntu_pxe.satadisk``
         image.

   - During boot, at the grub menu, edit the kernel boot parameters as below for
     enabling earlycon output and limiting the DDR memory to 2032MB for
     SATA disk detection

        ::

         setparams 'Install'
         set background_color=black
         linux /ubuntu-installer/arm64/linux mem=2032m earlycon=pl011,0x7ff80000 console=ttyAMA0,115200
         initrd /ubuntu-installer/arm64/initrd.gz

     Save and exit the grub menu. This boot will then continue up to the login
     prompt.


This completes the validation of the Ubuntu distribution installation and boot
functionalities.

--------------

*Copyright (c) 2019, Arm Limited. All rights reserved.*

.. _steps to setup PXE server: setup-pxe-server.rst
