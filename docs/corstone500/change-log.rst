Change Log
==========

This document contains a summary of the new features, changes and
fixes in each release of Corstone-500.

Version 2020.11.27
------------------

Features added
~~~~~~~~~~~~~~

None.

Changes
~~~~~~~
- Branding CA5DS to Corstone-500.
- Upgrading the kernel to v5.3.
- Using Yocto meta-arm layers aligned with Yocto Gatesgarth.
- Upgrading Trusted firmware A to v2.3 with a fix for the system timer issue.
- Upgrading u-boot to 2020.07 with a fix for the generic timer MMIO access issue.

Version 2020.03.06
------------------

Features added
~~~~~~~~~~~~~~
- Support for Snoop Control Unit and its device driver.
- Support for Cortex-A5 DesignStart on MPS3 FPGA.

Changes
~~~~~~~
- Changes to make the same software work on FPGA and FVP.
- Changes to Linux kernel config to run from DRAM (DDR).

Version 2019.09.16
------------------

Features added
~~~~~~~~~~~~~~
- Platform port of Cortex-A5 DesignStart including GICv1 changes.
- Support for Arm v7 architecture in Trusted firmware A.
- Support for non-LPAE mapping in Trusted firmware A.
- Division functionality for cores that don't have divide hardware.
- Support for mmio based generic timer in u-boot.

--------------

*Copyright (c) 2019-2020, Arm Limited. All rights reserved.*
