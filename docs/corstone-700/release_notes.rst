Release notes - 2019.09.23
==========================

.. section-numbering::
    :suffix: .

.. contents::


Components
----------
The following is a summary of the key software features of the release:

 - Tiny Linux stack built using Yocto for the Host Cortex-A processor.
 - Boot firmware with driver support for interrupt router & collator,
   MHUv2 (Mailbox Handling Unit version 2) and Boot processor and Host system
   Firewall.
 - Automated unit test suite.
 - RTX RTOS software running on external system.

Hardware Features
-----------------

 - Interrupt Router
 - Interrupt Collator
 - MHUv2 Driver
 - Boot processor Firewall
 - Host system Firewall
 - External system
 - REFCLK

Software Features
-----------------

 - OpenAMP in boot firmware
 - RPMSG driver in Linux
 - Interrupt Router driver in boot firmware
 - Interrupt Collator driver in boot firmware
 - MHUv2.1 driver in boot firmware and Linux
 - Firewall driver in boot firmware with translation and protection extension
 - Firewall driver in host system with protection and lock extension
 - RTX RTOS software running on external system
 - REFCLK Timer driver in boot firmware
 - Flash Parser driver

Platform Support
----------------
This Software release is tested on Corstone700 Fast Model platform (FVP) and
not on FPGA. Supported Fast model version for this release is 11.8.38

Known Issues or Limitations
---------------------------

 - The provided software stack has only been tested on an Arm Fixed Virtual
   Platform (FVP).
 - No support for multiple transport protocols in MHUv2 driver.
   It supports single word in-channel message.

Support
-------
For support email: support-subsystem-iot@arm.com

--------------

*Copyright (c) 2019, Arm Limited. All rights reserved.*
