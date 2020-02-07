Change Log
==========

This document contains a summary of the new features, changes and
fixes in each release of Corstone-700 software stack.

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
