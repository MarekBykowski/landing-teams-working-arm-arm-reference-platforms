Change Log
==========

This document contains a summary of the new features, changes and
fixes in each release of Corstone-700 software stack.

Version 2020.12.10
------------------

Features added
~~~~~~~~~~~~~~
- Linux kernel version upgraded to 5.6
- Enabled Ethernet support in linux.
  (note: SMSC 91c111 in FVP and SMSC 9115 in FPGA))
- Enabled USB host, gadget and mass support, in linux (Only for FPGA)
- Added U-boot support v2020.04
- Trusted Firmware A upgraded to v2.3
- Added support to configure the firewall monitor extension feature
- Using Yocto meta-arm layers aligned with Yocto Gatesgarth.
- Using Yocto poky-tiny-distro

Changes
~~~~~~~
- Split the FVP and FPGA into two machines. FVP and FPGA needs to be build separately.
  More information can be found in the user guide.

Fixes
~~~~~
- Fix in the SE firewall driver to configure the regions using base and the upper
  address of the regions.
- Fixed the system timer frequency for MPS3 FPGA board as 32Mhz, in TF-A code.

Version 2020.02.10
------------------

Features added
~~~~~~~~~~~~~~
- Support for Tamper interrupts and ISRs added in firewall driver.
- Secure Debug Channel SDC-600 driver in boot firmware.
- Enabled linux rootfs to use CRAMFS XIP.
- Support for FPGA.

Changes
~~~~~~~
- Configured linux kernel and rootfs to run it as XIP.
- Changed S/W codebase to run same S/W stack on FPGA and FVP.

Fixes
~~~~~
- Fixed firewall driver to disable error generation during tamper interrupts.

Version 2019.09.23
------------------

Features added
~~~~~~~~~~~~~~
- RTX RTOS software running on External system.
- Adding two test-app related to External system.
- Firewall driver in boot firmware with protection extension.
- Firewall driver in host system with protection and lock extension.

Changes
~~~~~~~
- Improvements in MHUv2 driver in linux kernel.
- Rewritten firewall driver with translation functionality.
- Changes in boot processor MPU for accessing host system memory.

--------------

*Copyright (c) 2019-2020, Arm Limited. All rights reserved.*
