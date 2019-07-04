Release Notes
=============

.. section-numbering::
    :suffix: .

.. contents::


Features and Fixes
------------------
The following is a summary of the key software features of the ALPHA2 release.

- All 4 Neoverse N1 cores running at 2.4 GHz.
- PCIe Link speed now support GEN3 - 8 GT/s.
- Multicore SMP Linux 5.1 kernel.
- Full blown Ubuntu 18.04 distribution supported now.
- SMMUv3 enabled to support PCIe ATS.
- EDK2/EDK2-Platforms rebased from github. ACPI Tables updated to expose SMMU to kernel.
- Multi-segment support enabled. Now the CCIX RC and PCIe RC are both enabled, hence normal PCIe card will
  be functional in any of the PCIe/CCIX open slot available on the board from Linux.
- PCIe card hosting a switch is supported on the PCIe slot behind the PLX switch.
- DDR speed enhanced to 2667 MTS. Single rank 8 GB per DIMM (Total 16 GB RAM) supported.
- Boot sequence optimized to improve the boot time.

Precautions
-----------
- The system thermal monitoring and control features are not yet calibrated,
  therefore do not operate the unit above room temperature (approximately 25°C):

  - The thermal shutdown features are currently disabled.
  - The chassis fan speed is currently fixed.

- The N1SDP is intended for use within a laboratory or engineering development
  environment. Do not use the N1SDP near equipment that is sensitive to
  electromagnetic emissions, for example, medical equipment.

- Never subject the board to high electrostatic potentials.
  Observe Electrostatic Discharge (ESD) precautions when handling any board.

  - Always wear a grounding strap when handling the board.
  - Avoid touching the component pins or any other metallic elements.

- Note: The case front panel USB 3.0 ports and & audio jacks are NOT connected/usable.
  They will be removed on later versions.

PCIe Testing
------------
Following are the PCIe Cards tested - PCIe and CCIX slot:
- DW-PCIe-M2(Ver A) with Samsung EVO 970 Pro NVMe M.2 (GEN3 x4)
- TUSB7340 DEMO EVM REV C USB hub card (GEN2 x1)
- Mellanox ConnectX-5
- PEXSAT34 - Two sata controller behind switch (GEN2 X2)


Known Issues or limitations
---------------------------
- To boot a standard distribution on N1SDP platform the kernel must be patched
  with the PCIe quirks. See the article `PCIE`_
- PCIe/CCIX Link speed supports upto GEN3. GEN4 is yet not enabled.
- No support for PCIe SRIOV.
- CCIX traffic not supported over CCIX RC.
- Currently only Micron 8GB single Rank DIMM (part number: 9ASF1G72PZ-2G6D1) is supported.

Next Release Target
-------------------
- All 4 Neoverse N1 cores running at 3 GHz.
- DIMM frequency 3200 MTS.
- DIMM capacity 32 GB/Dual Rank(Total 64 GB) from Multiple Vendors.

Support
-------
For support email: support-subsystem-enterprise@arm.com

--------------

*Copyright (c) 2019, Arm Limited. All rights reserved.*


.. _PCIE: pcie-support.rst
