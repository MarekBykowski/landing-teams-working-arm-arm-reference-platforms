Change Log
==========

.. section-numbering::
    :suffix: .

.. contents::

This document contains a summary of the incremental features, changes, fixes and known
issues in each release of N1SDP stack. It is listed in the order of latest to oldest


Tagged Version - N1SDP-2019.09.13
----------------------------------------
New Features
^^^^^^^^^^^^
- This release is performance tuned stack.
- Supports dual rank 16GB DIMM and single rank 8GB DIMM @ 2667 MTS. Total 32GB or 16GB RAM could be accessible.
- Core frequency bumped up to 2.6GHz
- Workaround for Erratum 1315703 is disabled, so that the N1 CPU
  performance is improved in N1SDP.This may be applied for N1 software that doesnot require Spectre Variant 4 mitigation.
- Thermal shutdown supported - The system is shutdown automatically when the SOC temperature rises beyond 80 degrees.
- SLC Cache Stashing supported for increased PCIe ingress network packet performance.

Known Issues and Limitation
^^^^^^^^^^^^^^^^^^^^^^^^^^^
- PCIe/CCIX Link speed supports upto GEN3. GEN4 is yet not enabled.
- No support for PCIe SRIOV.
- Currently only Micron 8GB /16GB single/dual Rank DIMMs supported (part number: 9ASF1G72PZ-2G6D1) is supported.CCIX traffic not supported over CCIX RC.



Tagged Version - N1SDP-ALPHA2-CCIX-19.07
----------------------------------------
New Features
^^^^^^^^^^^^
- CCIX traffic supported over CCIX RC.
- Remote RA to Host HA traffic tested.
- Support for CCIX parser following CCIX software specification added in EDK2
- Reference CCIX platform library added in EDK2-Platforms
- Validated CCIX parser and platform library with remote Requesting Agent (RA)
  design programmed in Xilinx Alveo U280 accelerator FPGA card
- For all CCIX specific documents please refer to the following link
  https://www.ccixconsortium.com/ccix-library/

  Please contact CCIX consortium to get access to the documents if not already available

Known Issues and Limitation
^^^^^^^^^^^^^^^^^^^^^^^^^^^
- PCIe/CCIX Link speed supports upto GEN3. GEN4 is yet not enabled.
- No support for PCIe SRIOV.
- Currently only Micron 8GB single Rank DIMM (part number: 9ASF1G72PZ-2G6D1) is supported.CCIX traffic not supported over CCIX RC.



Tagged Version - N1SDP-ALPHA2-19.07
------------------------------------
New Features
^^^^^^^^^^^^
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

Known Issues and Limitation
^^^^^^^^^^^^^^^^^^^^^^^^^^^
- PCIe/CCIX Link speed supports upto GEN3. GEN4 is yet not enabled.
- No support for PCIe SRIOV.
- CCIX traffic not supported over CCIX RC.
- Only Micron 8GB single Rank DIMM (part number: 9ASF1G72PZ-2G6D1) is supported.



Tagged Version - N1SDP-ALPHA1-19.04
------------------------------------
New Features
^^^^^^^^^^^^
- Multicore SMP Linux 5.0 kernel booting to an OpenEmbedded LAMP filesystem.
- All 4 Neoverse N1 cores running at 2 GHz.
- All on board PCIe devices USB3/GbE/SATA enabled and functional.
- 16GB DDR4 memory running at 1600MT/s speed.
- Busybox Filesystem supported.

Known Issues and Limitation
^^^^^^^^^^^^^^^^^^^^^^^^^^^
- PCIe slots limited testing done with few cards like SATA card and GbE card.
- PCIe tested with GEN1 speed only.
- No support for PCIe SRIOV.
- CCIX RC not supported.
- Only Micron 8GB single Rank DIMM (part number: 9ASF1G72PZ-2G6D1) is supported.
