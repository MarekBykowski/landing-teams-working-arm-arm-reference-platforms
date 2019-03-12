Running the software on N1SDP
=============================


.. section-numbering::
    :suffix: .

.. contents::


Introduction
------------

The Neoverse N1 System Development Platform (N1SDP) is an enterprise class reference board based on the Neoverse N1 core.
This document is a guide on how to run an Arm Reference Platforms software stack on N1SDP .

These instructions assumes you have already followed the `user-guide`_ to sync and build an Arm Platforms
software stack for N1SDP.

The synced workspace includes several board files and prebuilt binaries under *<workspace/board_firmware/>* directory.

Setup Preparation
-----------------

**Preparing a bootable disk**

A bootable disk (USB stick or SATA drive) can be prepared by formatting it with the prebuilt image located at
*<workspace/grub-oe-lamp.img>* or the source build image at the location *<workspace/output/n1sdp/build_artifact/grub-oe-lamp.img>*
after the source build.

This is a bootable GRUB image comprising LINUX and an OpenEmbedded LAMP file system. The partitioning and packaging is performed
during the build.

Use the following commands to burn the GRUB image to a USB stick or SATA drive:

        ::

             $ lsblk
             $ sudo dd if=grub-oe-lamp.img of=/dev/sdX
             $ sync

        Note:

        Replace ``/dev/sdX`` with the handle corresponding to your USB stick or SATA drive, as identified by the ``lsblk`` command.

        Connect the bootable media to the N1SDP platform; USB sticks should be inserted into to one of the four USB3.0 ports, while
        SATA drives should be connected to one of the two SATA ports.


**Configure COM Ports**

Connect a USB-B cable between your host PC and N1SDP's DBG USB port, then power ON the board. The DBG USB connection will enumerate
as four virtual COM ports assigned to the following processing entities, in order

       ::

               COM<n>   - Motherboard Configuration Controller (MCC)
               COM<n+1> - Application Processor (AP)
               COM<n+2> - System Control Processor (SCP)
               COM<n+3> - Manageability Control Processor (MCP)

Please check Device Manager in Windows or ls /dev/ttyUSB* in Linux to identify <n..>

Use a serial port application such as *PuTTy* or *minicom* to connect to all virtual COM ports with the following settings:

      ::

               115200 baud
               8-bit word length
               No parity
               1 stop bit
               No flow control

*Note: Some serial port applications refer to this as "115200 8N1" or similar.*

**Preparing a microSD card**

Ensure both BOOT CONF switches are in the OFF position, then issue the following commands in the MCC console:

      ::

              Cmd> USB_ON

This will mount the on-board microSD card as a USB Mass Storage Device on the host PC with name N1SDP.  The new contents to re-flash in
the SD card is taken from prebuilt image at *<workspace/board_firmware/*>.

SOC Firmware could be overriden after source build from the *<workspace/output/n1sdp/build_artifact/*> to *<sd card mount point/SOFTWARE/>* except the grub-oe-lamp.img
Issue a sync command on your host PC to ensure copy has completed.

Running the deliverables on N1SDP
---------------------------------
For Running the software stack on N1SDP, binaries to prepare bootable disk and micro sd card could be
fetched in the following two ways as mentioned in `user-guide`_

**Prebuilt configuration**

The precompiled SOC firmware as well as the board firmware are synced in *<workspace/n1sdp-latest-oe-uefi/>* and a
grub-oe-lamp.img in *<workspace/>* Prepare bootable disk and micro sd card as mentioned in section above :


**Built from source**

After fetching and building the source, new updated SOC software binaries are copied at *<workspace/output/n1sdp/build_artifact/>*.
Prepare a bootable disk and micro sd card as mentioned in section above :


**Booting the board**

Ensure all COM ports configuration done . Bootable media prepared and connected and micro sd card formatted with the
board and SOC firmware. Ensure to connect the ethernet cable to the *onchip PCIe GbE port* to avoid dhcp time out during booting.
Shutdown and reboot the N1SDP platform from MCC command prompt .

     ::

       Cmd> SHUTDOWN
       Cmd> REBOOT


Once the programming is done, the board will boot up and run the new software images.
The REBOOT command initializes all the board components and flashes the binaries from the micro SD card into on-board QSPI flash
memory or DDR3 memory connected to the IOFPGA. Destination for programming the binaries and programming settings can be checked
in *<MB/images.txt>* on the micro SD card.

Enter to the UEFI menu by pressing *Esc* on the AP Console as the *edk2* logs start appearing. User can select from the UEFI
boot manager, which media to boot from.


--------------

*Copyright (c) 2019, Arm Limited. All rights reserved.*

.. _user-guide: ../user-guide.rst
