Release Notes
=============

.. section-numbering::
    :suffix: .

.. contents::


Features and Fixes
------------------
The following is a summary of the key software features of the N1SDP-ALPHA2-CCIX-19.07 release.

- Support for CCIX parser following CCIX software specification added in EDK2
- Reference CCIX platform library added in EDK2-Platforms
- Validated CCIX parser and platform library with remote Requesting Agent (RA)
  design programmed in Xilinx Alveo U280 accelerator FPGA card
- For all CCIX specific documents please refer to the following link
  https://www.ccixconsortium.com/ccix-library/
  Please contact CCIX consortium to get access to the documents if not already available

Note:
This release is an add-on to the ALPHA2 release published before.
For ALPHA2 release features, please refer to ALPHA2 release notes.

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
