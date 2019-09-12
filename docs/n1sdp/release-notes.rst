Release Notes
=============

.. section-numbering::
    :suffix: .

.. contents::


Features and Fixes
------------------
The following is a summary of the key software features of the N1SDP-ALPHA2-PERF-19.09 release.

- ** This release is performance tuned stack.**
- Supports dual rank 16GB DIMM and single rank 8GB DIMM @ 2667 MTS. Total 32GB or 16GB RAM could be accessible.
- Core frequency bumped up to 2.6GHz
- Workaround for Erratum 1315703 is disabled, so that the N1 CPU
  performance is improved in N1SDP.This may be applied for N1 software that does not require Spectre Variant 4 mitigation.
- Thermal shutdown supported - The system is shutdown automatically when the SOC temperature rises beyond 80 degrees.
- SLC Cache Stashing supported for increased PCIe ingress network packet performance.

Note:
This release is an add-on to the N1SDP-ALPHA2-CCIX-19.07 release published before.
For ALPHA2 release features, please refer to N1SDP-ALPHA2-CCIX-19.07 release notes.

Precautions
-----------
- The system thermal monitoring and control features are not yet calibrated,
  therefore do not operate the unit above room temperature (approximately 25°C):

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
- Xilinx U280 CCIX card.


Known Issues or limitations
---------------------------
- To boot a standard distribution on N1SDP platform the kernel must be patched
  with the PCIe quirks. See the article `PCIE`_
- PCIe/CCIX Link speed supports upto GEN3. GEN4 is yet not enabled.
- No support for PCIe SRIOV.
- Currently supports only Micron 8GB/16GB single/dual Rank DIMM (part number: 9ASF1G72PZ-2G6D1) is supported.
- There could be stability issues on long stress test of the system.

Next Release Target
-------------------
- Full CCIX support
- H/W accelerator and C2C use cases over CCIX.

Support
-------
For support email: support-subsystem-enterprise@arm.com

--------------

*Copyright (c) 2019, Arm Limited. All rights reserved.*


.. _PCIE: pcie-support.rst
