Release notes - 2019.09.16
==========================

.. section-numbering::
    :suffix: .

.. contents::


Software Features
-----------------
The following is a summary of the key software features of the release:

 - Linux kernel version 5.2.
 - Trusted firmware A with Cortex A5 Designstart platform port.
 - U-Boot changes with memory mapped timer support.
 - Build and Packaging using yocto based poky-tiny distro.
 - Detailed change log can be viewed here `Change Log <change-log.rst>`__

Hardware Features
-----------------

 - Memory mapped generic timer support
 - Generic interrupt controller (GIC) support
 - UART PL011
 - RTC


Platform Support
----------------
This Software release is tested on Cortex A5 Designstart Fast Model
platform (FVP) and not on FPGA.Supported Fast model version for
this release is 11.8.37


Known Issues or Limitations
---------------------------

 - The provided software stack has only been tested on
   an Arm Fixed Virtual Platform (FVP).
 - Software supports single core boot only in this
   release.

Support
-------
For support email: support-subsystem-iot@arm.com

--------------

*Copyright (c) 2019, Arm Limited. All rights reserved.*
