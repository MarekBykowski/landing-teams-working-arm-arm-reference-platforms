Release notes - 2020.08.14
==========================

.. section-numbering::
    :suffix: .

.. contents::

Release tag
-----------
The manifest tag for this release is TC0-2020.08.14

Components
----------
The following is a summary of the key software features of the release:
 - Yocto based BSP build supporting Android and Poky distro.
 - Trusted firmware-A for secure boot.
 - System control processor(SCP) for programming the interconnect, doing power control etc.
 - U-Boot bootloader.

Hardware Features
-----------------
 - Booker CI with Memory Tagging Unit(MTU) support driver in SCP.
 - GIC Clayton Initialization in Trusted Firmware-A.
 - HDLCD and virtual encoder support for display in Linux.
 - MHUv2 Driver for SCP and AP communication.
 - UARTs, Timers, Flash, PIK, Clock drivers.

Software Features
-----------------
 - Poky Distribution support.
 - Android Q/10 Support.
 - Android Common Kernel 4.19.
 - Trusted Firmware-A.
 - Support secure boot based on TBBR specification https://developer.arm.com/documentation/den0006/latest
 - System Control Processor firmware.
 - Yocto based build system.
 - U-Boot bootloader.

Platform Support
----------------
 - This Software release is tested on TC0 Fast Model platform (FVP).
   - Supported Fast model version for this release is 11.11.36

Known issues or Limitations
---------------------------
At the U-Boot prompt press enter and type "boot" to continue booting else wait
for ~15 secs for boot to continue automatically.This is because of the time
differrence in CPU frequency and FVP operating frequency.

Support
-------
For support email:  support-arch@arm.com

--------------

*Copyright (c) 2020, Arm Limited. All rights reserved.*
