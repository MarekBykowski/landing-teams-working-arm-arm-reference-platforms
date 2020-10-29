Change Log
==========

This document contains a summary of the new features, changes and
fixes in each release of TC0 software stack.

Version 2020.10.29
------------------

Features added
~~~~~~~~~~~~~~
- Power management features: cpufreq and cpuidle.
- SCMI (System Control and Management Interface) support.
- Verified u-boot for authenticating fit image (containing kernel + ramdisk) during poky boot.
- Android Verified Boot (AVB) for authenticating boot and system image during android boot.
- Software rendering on android with DRM Hardware Composer offloading composition to Mali D71 DPU.
- Initial support for Hafnium as Secure Partition Manager (SPM) at S-EL2, managing cactus S-EL1 test Secure Partitions (SPs). The git SHA used for Hafnium is 764fd2eb and for Trusted Firmware-A is 00ad74c7.

Changes
~~~~~~~
- Changed from Android Common Kernel 4.19 to 5.4.
- Changed from Cortex-M7 to Cortex-M3 based System Control Processor.

Version 2020.08.14
------------------

Features added
~~~~~~~~~~~~~~
- Poky Distribution support.
- Android Q/10 Support.
- Android Common Kernel 4.19.
- Trusted Firmware-A.
- Support secure boot based on TBBR specification https://developer.arm.com/documentation/den0006/latest
- System Control Processor firmware.
- Yocto based build system.
- U-Boot bootloader.

--------------

*Copyright (c) 2020, Arm Limited. All rights reserved.*
