Release notes - 19.02
=====================

.. section-numbering::
    :suffix: .

.. contents::


Components
----------
The following is a summary of the key software features of the release:

 - Tiny linux stack built using Yocto for the Host Cortex-A processor.
 - Boot firmware with driver support for interrupt router & collator,
   MHUv2 (Mailbox Handling Unit version 2) and Firewall.
 - Automated unit test suite.
 - No software support for external system in this release.

Hardware Features
-----------------

 - Interrupt Router
 - Interrupt Collator
 - MHUv2 Driver
 - Boot processor Firewall
 - REFCLK

Software Features
-----------------

 - OpenAMP in boot firmware
 - RPMSG driver in Linux
 - Interrupt Router driver in boot firmware
 - Interrupt Collator driver in boot firmware
 - MHUv2.1 Driver driver in boot firmware and Linux
 - Firewall driver in boot firmware
 - REFCLK Timer driver in boot firmware
 - Flash Parser driver

Platform Support
----------------
This Software release is tested on Corstone700 Fast Model platform (FVP) and
not on FPGA.Supported Fast model version for this release is 11.7.


Known Issues or Limitations
---------------------------

 - The provided software stack has only been tested on
   an Arm Fixed Virtual Platform (FVP).
 - No support for multiple transport protocols in MHUv2 driver.
   It supports single word in-channel message.

Support
-------
For support email: support-subsystem-iot@arm.com

--------------

*Copyright (c) 2019, Arm Limited. All rights reserved.*
