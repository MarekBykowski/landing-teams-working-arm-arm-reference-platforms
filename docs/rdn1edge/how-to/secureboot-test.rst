How to build RD-N1-Edge platform software to validate Secure Boot
=================================================================


.. section-numbering::
    :suffix: .

.. contents::

What is Secure Boot
-------------------

Secure boot is a mechanism to build and maintain a complete chain of trust on
all the software layers executed in a system and preventing malicious code to be
stored and loaded in place of the authenticated one. When the device starts, the
firmware checks the signature of each piece of boot software, including UEFI
firmware drivers, EFI applications, and the operating system. If the signatures
are valid, the device boots, and the firmware gives control to the operating
system. Fundamental to the success of the secure boot is the ability to securely
store (also referred to as secure storage) and access the keys used for
authentication during the various stages of boot.

Secure boot and Secure storage mechanisms are defined by the UEFI
specifications. In short, the UEFI specifications define the use of two
asymmetric key pairs, platform key (PK) and Key Exchange Key (KEK), and
databases for valid and black listed signatures. These keys and databases are
used during the secure boot phase which implies that the platform should provide
a tamper proof mechanism to store these keys.

Secure boot support for RD-N1-Edge platform
-------------------------------------------

The RD-N1-Edge platform software allows validation of the secure boot process.
Though secure boot process have to be validated using a linux distribution as
the target OS, the RD-N1-Edge platform software stack currently limits this feature
validation to boot of a signed busybox OS. There are pre-requisite packages to
be installed on the host PC to build the disk image to validate the secure boot
process. It is important that the following packages are installed prior to
building of the software stack for secure boot validation. The prerequisite
package installer script, if used, does install these packages as well.

- efitools git repo is cloned and available at tools/efitools
- sbsign package is installed on to the local host system

The next step is to create key pairs required for secure boot. The one-time
generation of the following key pairs are mandatory - PK, KEK, DB and DBX. The
following commands can be used to generate these key pairs.

- Key Pair Creation : PK, KEK, DB and DBX

  ::

        cd tools/efitools
        openssl req -new -x509 -newkey rsa:2048 -subj "/CN=PK/" -keyout PK.key -out PK.crt -days 3650 -nodes -sha256
        openssl req -new -x509 -newkey rsa:2048 -subj "/CN=KEK/" -keyout KEK.key -out KEK.crt -days 3650 -nodes -sha256
        openssl req -new -x509 -newkey rsa:2048 -subj "/CN=DB_Key/" -keyout DB.key -out DB.crt -days 3650 -nodes -sha256
        openssl req -new -x509 -newkey rsa:2048 -subj "/CN=DBX_Key/" -keyout DBX.key -out DBX.crt -days 3650 -nodes -sha256

- Convert crt certificate to der format

  ::

        openssl x509 -in PK.crt -outform der -out PK.der
        openssl x509 -in KEK.crt -outform der -out KEK.der
        openssl x509 -in DB.crt -outform der -out DB.der
        openssl x509 -in DBX.crt -outform der -out DBX.der

The signing of the grub and linux images are performed as a part of build script
“build-secureboot.sh”. There is no explicit user action required to sign these
images.

Procedure to build secure boot test for RD-N1-Edge platforms
------------------------------------------------------------

The procedure to build the secure boot test along with the RD-N1-Edge platform software
stack is listed below.

To build the RD-N1-Edge software stack, the command to be used is

   ::

        ./build-scripts/rdinfra/build-test-secureboot.sh -p rdn1edge <command>

Supported command line options are listed below

   -  <command>

      -  Supported commands are

         -  clean
         -  build
         -  package
         -  all (all the three above)


Examples of the build command are

   -   ::

        ./build-scripts/rdinfra/build-test-secureboot.sh -p rdn1edge all

      - This command cleans, builds and packages the RD-N1-Edge software stack needed
        for the secure boot test for RD-N1-Edge platform.

   -   ::

        ./build-scripts/rdinfra/build-test-secureboot.sh -p rdn1edge build

      - This command performs an incremental build of the software components
        included in the software stack for the RD-N1-Edge platform. Note: this
        command should be followed by the 'package' command to complete the
        preparation of the fip and the disk image.

   -   ::

        ./build-scripts/rdinfra/build-test-secureboot.shh -p rdn1edge package

      - This command packages the previously built software stack and prepares
        the fip and the disk image.


Procedure to execute secure boot test on RD-N1-Edge platforms
-------------------------------------------------------------
The procedure to execute the secure boot test on the RD-N1-Edge platform is listed
below.

   ::

        cd model-scripts/rdinfra
        ./secure_boot.sh -p rdn1edge -a <additional_params> -n [true|false]


Supported command line options are listed below

   -  -n [true|false] (optional)

      -  Controls the use of network ports by the model. If network ports have
         to be enabled, use 'true' as the option. Default value is set to
         'false'.

   -  -a <additional_params>

      -  Specify any additional model parameters to be passed. The model
         parameters and the data to be passed to those parameters can be found
         in the FVP documentation.


Example commands to validate the secure boot functionality are as listed below.

   -   ::

        ./secure_boot.sh -p rdn1edge

      - This command starts the execution of the RD-N1-Edge model and the software
        boots upto the busybox login prompt.

   -   ::

        ./secure_boot.sh -p rdn1edge -n true

      - This command starts the execution of the RD-N1-Edge model and the
        software boots upto the busybox login prompt. The model supports
        networking allowing the software running within the model to access
        the network.

   -   ::

        ./secure_boot.sh -p rdn1edge -n true -a "-C board.flash0.diagnostics=1"

    -   This command starts the execution of the RD-N1-Edge model with networking
        enabled and the software boots upto the busybox login prompt. Additional
        parameters to the model are supplied using the -a command line
        parameter.

There are additional steps to be performed on the first boot to setup the secure
boot process. These steps are listed below. Ensure that these steps are executed
on the very first boot for validating the secure boot.

- Interrupt the boot at EDK2 by pressing escape key and dropping into the EDK2
  boot menu.
- Select Device Manger -> Secure Boot Configuration -> Secure Boot Mode →
  choose Custom mode and then press enter.
- Select "Custom Secure Boot Options” and then press enter.
- Select “DBX Options” -> "Enroll Signature" then press enter →
  "Enroll Signature Using File" and the press enter → Select “NO VOLUME LEBEL”
  and then press enter.
- Select EFI and press enter -> select BOOT and press enter → now Select
  “DBX.der” and press enter -> “Commit Changes and Exit”.
- Repeat steps “d” and “e” for “DB options” for “DB.der”.
- Repeat steps “d” and “e” for “KEK options” for “KEK.der”.
- Repeat steps “d” and “e” for “PK options” for “PK.der”.
- Press Escape and press F10 to save. Ensure that the “Current Secure Boot
  State” is set as “Enabled”.
- Press Escape and select the “continue” option.
- Prompts the user to press the “Enter”. Press Enter key which then reboots the
  system
- Make sure to close the model using “Cross Mark” of “Fast Models -Clark”
  windows after this, if model does not close then press “ctrl-c” to close it.

Relaunch the model again, the platform boots up to busybox login prompt with
secure boot enabled. If the authentication of the grub or the linux kernel
fails, the boot fails and the user is notified about the authentication failure.

To confirm that the boot is indeed a secure boot, the linux kernel messages
can be looked up. The following messages would appear in the linux boot log in
case of a secure linux kernel boot.

   ::

      Loading driver at 0x000F5D26000 EntryPoint=0x000F6D0AF80
      Loading driver at 0x000F5D26000 EntryPoint=0x000F6D0AF80
      EFI stub: Booting Linux Kernel...
      EFI stub: UEFI Secure Boot is enabled.
      EFI stub: Using DTB from configuration table
      EFI stub: Exiting boot services and installing virtual address map...
      [    0.000000] Booting Linux on physical CPU 0x0000000000 [0x410fd060]

This completes the validation of the Secure boot functionality.

--------------

*Copyright (c) 2019, Arm Limited and Contributors. All rights reserved.*
