.. section-numbering::
    :suffix: .

.. contents::


Release notes - 2020.12.10
==========================

Software Features
------------------
The following is a summary of the key software features of this release:

- Linux kernel version upgraded to 5.6
- Enabled Ethernet support in linux.
  (note: SMSC 91c111 in FVP and SMSC 9115 in FPGA)
- Enabled USB host, gadget and mass support in linux (Only for FPGA)
- Added U-boot support v2020.04
- Trusted Firmware A upgraded to v2.3
- Added support to configure the firewall monitor extension feature
- Using Yocto meta-arm layers aligned with Yocto Gatesgarth.
- Using Yocto poky-tiny-distro
- Detailed change log can be found in change-log.rst

Platform Support
----------------
 - This Software release is tested on Corstone700 Fast Model platform (FVP) and FPGA
 - Supported Fast model version for this release is 11.10.47
 - Supported FPGA version is AN543 V3.0 on MPS3 board

Known Issues or Limitations
---------------------------

 - No support for multiple transport protocols in MHUv2 driver.
   It supports single word in-channel message.

Release notes - 2020.02.10
==========================


Components
----------
The following is a summary of the key software features of the release:

 - Tiny Linux stack built using Yocto for the Host Cortex-A processor.
 - Boot firmware with device drivers for following Arm IPs:

   - Interrupt Router
   - Interrupt Collator
   - Mailbox Handling Unit MHUv2
   - Boot processor Firewall
   - Host system Firewall
   - Secure Debug Channel SDC-600
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
 - Secure Debug Channel SDC-600

Software Features
-----------------

 - OpenAMP in boot firmware
 - RPMSG driver in Linux
 - Interrupt Router driver in boot firmware
 - Interrupt Collator driver in boot firmware
 - MHUv2.1 driver in boot firmware and Linux
 - Firewall driver in boot firmware with translation and protection extension
 - Firewall driver in host system with protection and lockdown extension
 - RTX RTOS software running on external system
 - REFCLK Timer driver in boot firmware
 - Flash content parser driver
 - SDC-600 Secure debug driver in boot firmware

Platform Support
----------------
 - This Software release is tested on Corstone700 Fast Model platform (FVP) and FPGA

   - Supported Fast model version for this release is 11.9.51
   - Supported FPGA version is AN543 V1.0 on MPS3 board

Known Issues or Limitations
---------------------------

 - No support for multiple transport protocols in MHUv2 driver.
   It supports single word in-channel message.

Support
-------
For support email: support-subsystem-iot@arm.com

--------------

*Copyright (c) 2019-2020, Arm Limited. All rights reserved.*
