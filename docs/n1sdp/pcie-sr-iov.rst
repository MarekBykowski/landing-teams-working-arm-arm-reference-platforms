PCIe SR-IOV on Neoverse N1 SDP
==============================

.. section-numbering::
    :suffix: .

.. contents::


Introduction
------------
The Neoverse N1 System Development Platform (N1SDP) supports two PCIe root ports each
supporting the standard PCIe features including the Single Root I/O Virtualization (SR-IOV)
feature. This document gives an overview of how to enable and test the SR-IOV feature on
N1SDP.

Note:
Due to the PCIe limitations in N1SDP platform (`pcie-support`_), the SR-IOV feature has not been completely validated.

Pre-Requisite
-------------
    1. Latest software stack synced by following steps given in `user-guide`_
    2. Ensure that the Linux tree in the synced workspace contains the SR-IOV and PCI ACS override patches. This should have been already applied when syncing the code.

Steps to verify SR-IOV
----------------------
    1. Add kernel config CONFIG_IXGBEVF=y to linux/arch/arm64/configs/defconfig file. This is required to enable drivers for the mentioned Intel card.
    2. Build the software stack and flash the Ubuntu image onto the boot device. Do initial boot of the board which installs Ubuntu and perform second boot which boots Ubuntu kernel.
    3. Login to target Ubuntu console and edit the file /etc/default/grub. Add pcie_acs_override=id:13b5:0100 option to the GRUB_CMDLINE_LINUX_DEFAULT. Save this file and run update-grub command.
    4. Reboot the board from Ubuntu console using reboot now command.
    5. Now Linux probes and assigns separate IOMMU groups for all PCIe devices.
    6. Virtual functions can be enabled from sysfs using following command:

       *echo 63 > /sys/bus/pci/devices/0001\:01\:00.0/sriov_numvfs*

       Note that in test environment the Intel card's ethernet port 0 is identified in Segment:1 Bus:1 Dev:0 Function:0

Limitations
-----------
    1. SR-IOV feature is only supported in CCIX slot and not in the PCIe slots. This is due to the
       on-board PCIe switch not supporting the ARI capability to which the PCIe slots are connected.
    2. Only Intel X540-T2 card has been validated for the SR-IOV feature.

References
----------
- http://infocenter.arm.com/help/topic/com.arm.doc.101489_0000_01_en/arm_neoverse_n1_system_development_platform_technical_reference_manual_101489_0000_01_en.pdf

----------

*Copyright (c) 2020, Arm Limited. All rights reserved.*

.. _user-guide: ../user-guide.rst
.. _run-on-n1sdp: run-on-n1sdp.rst
.. _pcie-support: pcie-support.rst
