Running the software on N1SDP
=============================


.. section-numbering::
    :suffix: .

.. contents::


Introduction
------------

The Neoverse N1 System Development Platform (N1SDP) is an enterprise class reference board based on the Neoverse N1 core.
This document is a guide on how to run an Arm Reference Platforms software stack on N1SDP .

These instructions assumes you have already followed the `user-guide`_ to sync and build an Arm Reference Platforms
software stack for N1SDP.

The synced workspace includes several board files and prebuilt binaries under the *<workspace/board_firmware/>* directory.

Setup Preparation
-----------------

**Preparing a bootable disk**

A bootable disk (USB stick or SATA drive) can be prepared by formatting it with the prebuilt image located at
*<workspace/grub-ubuntu.img>* or the source build image at the location *<workspace/output/n1sdp/build_artifact/grub-ubuntu.img>*
after the source build.

This is a bootable GRUB image comprising LINUX and an Ubuntu 18.04 file system. The partitioning and packaging is performed
during the build.

Use the following commands to burn the GRUB image to a USB stick or SATA drive:

        ::

             $ lsblk
             $ sudo dd if=grub-ubuntu.img of=/dev/sdX bs=1M
             $ sync

Note: Replace ``/dev/sdX`` with the handle corresponding to your USB stick or SATA drive, as identified by the ``lsblk`` command.

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

Please check Device Manager in Windows or ls /dev/ttyUSB* in Linux to identify <n>.

Use a serial port application such as *PuTTy* or *minicom* to connect to all virtual COM ports with the following settings:

      ::

               115200 baud
               8-bit word length
               No parity
               1 stop bit
               No flow control

Note: Some serial port applications refer to this as "115200 8N1" or similar.

Running the deliverables on N1SDP
---------------------------------

Ensure both BOOT CONF switches are in the OFF position, then issue the following
command in the MCC console:

    Cmd> USB_ON

This will mount the on-board microSD card as a USB Mass Storage Device on the
host PC with the name N1SDP; how you then proceed will depend on whether you
built from source or chose a prebuilt configuration.

Ensure that time is correctly set on N1SDP board through following command in
the MCC console if not set then change it accordingly:

      ::

             Cmd> debug
             Debug> time
             Debug> date
             Debug> exit




**Prebuilt configuration**

Copy the contents of <workspace/n1sdp-board-firmware-N1SDP-ALPHA2-19.07/n1sdp-board-firmware-N1SDP-ALPHA2-19.07/>
onto the mounted microSD card, then skip to the ** Booting the board ** section.

**Built from source**

Copy the contents of <workspace/board_firmware/> onto the mounted microSD card,
then copy the .bin files mcp_fw.bin, mcp_rom.bin, scp_fw.bin, and scp_rom.bin from <workspace/output/n1sdp/build_artifact/> to the
<SOFTWARE/> directory on the mounted microSD card, overwriting the existing files.

**Booting the board**

Insert the bootable disk created earlier, and connect an ethernet cable to the
Gigabit Ethernet port to avoid DHCP timeouts during boot.

Shutdown and reboot the board by issuing the following commands to the MCC
console:

    ::

             Cmd> SHUTDOWN
             Cmd> REBOOT

On rebooting, the board will copy the new binaries and firmware images from
the microSD card into either on-board QSPI flash or DDR3 memory via the IOFPGA;
see <MB/images.txt> on the microSD card.

Enter the UEFI menu by pressing Esc on the AP console as the edk2 logs start
appearing; from here, enter the UEFI Boot Manager menu and then select media
having Ubuntu 18.04 bootable image.
Ubuntu 18.04 will boot in two stages, onces first boot is finished reboot the board
from MCC console.

    ::

             Cmd> REBOOT

After this boot onwards full fledged Ubuntu 18.04 distribution will be up and running.
Login as root and install any required packages from the console
# apt-get install <package-name>

--------------

*Copyright (c) 2019, Arm Limited. All rights reserved.*

.. _user-guide: ../user-guide.rst

