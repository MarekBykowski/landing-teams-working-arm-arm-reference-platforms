Change Log
==========

.. section-numbering::
    :suffix: .

.. contents::

This document contains a summary of the incremental features, changes, fixes and known
issues in each release of N1SDP stack. It is listed in the order of latest to oldest

Tagged Version - N1SDP-2020.12.15
----------------------------------------
New Features
^^^^^^^^^^^^
- Yocto based BSP build to generate Poky image.
- Streamlining of build-scripts to build only ubuntu image and perf package. Use yocto framework for other components.
- Enable PCIe devices on secondary chip.

Known Issues and Limitations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- If either of the two boards needs to boot-up in a single chip mode with a C2C setup,
  then the other board should be powered off.
- PCIe root port is limited to GEN3 speed due to the on-board PCIe switch itself only supporting
  upto GEN3 speed.
- Page Request Interface (PRI) feature is not available in both SMMUs interfacing with the
  PCIe root ports.
- Currently only Micron 8GB single Rank DIMM (part number: MTA9ASF1G72PZ-2G6D1) and
  16GB dual Rank DIMMs (part number:MTA18ASF2G72PDZ-2G6E1) are supported.
- Stability issues have been observed on long stress tests of the system.
- On-board HDMI connection is not supported for graphics output. A PCIe graphics card can be used
  for graphics support.

Tagged Version - N1SDP-2020.07.27
----------------------------------------
New Features
^^^^^^^^^^^^
- Stability improvement over the GEN4 x16 link on CCIX slot. Verified with Mellanox Card (MCX516A-CDAT).
- Switched to user space dhcp client from the kernel space dhcp client for the initial ubuntu boot.
- Updated MCC firmware (mbb_v107) – This prompt for the recommended PMIC firmware.
- Added new PMIC firmware (300k_8c2) – This supports for boards manufactured post Nov 2019.
- Added latest PCC firmware (pcc_v050) – This allows to update of older boards.

Known Issues and Limitations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- If either of the two boards needs to boot-up in a single chip mode with a C2C setup,
  then the other board should be powered off.
- PCIe root port is limited to GEN3 speed due to the on-board PCIe switch itself only supporting
  upto GEN3 speed.
- GEN4 x16 link in CCIX slot has not been tested for performance.
- CCIX use-cases (Accelerator/Multichip) are limited to GEN3 speed.
- Page Request Interface (PRI) feature is not available in both SMMUs interfacing with the
  PCIe & CCIX root ports.
- Currently only Micron 8GB single Rank DIMM (part number: MTA9ASF1G72PZ-2G6D1) and
  16GB dual Rank DIMMs (part number:MTA18ASF2G72PDZ-2G6E1) are supported.
- Multichip use-case only enables access to peripherals and PCIe endpoints in the master chip.
- Stability issues have been observed on long stress tests of the system.
- On-board HDMI connection is not supported for graphics output. A PCIe graphics card can be used
  for graphics support.

Tagged Version - N1SDP-2020.03.26
----------------------------------------
New Features
^^^^^^^^^^^^
- CCIX accelerator support with CCIX endpoint having just a Request Agent (RA).
    - Reference CCIX platform library in EDK2-Platforms will dynamically discover the endpoint
      RA topology and configures both the N1SDP host and CCIX endpoint.
    - The framework is verified with the endpoint RA design programmed in Xilinx Alveo U280
      accelerator FPGA card.
    - For all CCIX specific documents please refer to the CCIX consortium link:
      https://www.ccixconsortium.com/ccix-library/
    - Please contact the CCIX consortium to get access to the documents if not already available.
    - Please contact Xilinx for supporting bit files and userspace applications for the Alveo-U280

- Multichip SMP support over CCIX/PCIe link.
    - Dual socket SMP boot with two N1SDP boards connected over CCIX/PCIe link.
    - Linux sees 8 cores and DDR memories from both primary and secondary N1SDP boards.
    - CCIX/PCIe link running at GEN3 x16 speed.

- PCIe GEN4 x16 support in CCIX slot. GEN4 x16 link verified with Mellanox Card (MCX516A-CDAT).
  No performance benchmark/tuning has been done.
- PMU counter support for CMN-600.
- Coresight Debug/Trace support.
- PCIe SRIOV framework support. Tested with Intel X540-T2 card.
- Device Tree support available when using new BusyBox filesystem option [Experimental]. Note that
  BusyBox filesystem option is only available when building from source and offers limited
  functionality.

Known Issues and Limitation
^^^^^^^^^^^^^^^^^^^^^^^^^^^
- PCIe root port is limited to GEN3 speed due to the on-board PCIe switch itself only supporting
  upto GEN3 speed.
- GEN4 x16 link in CCIX slot has not been tested for performance.
- CCIX use-cases (Accelerator/Multichip) are limited to GEN3 speed.
- Page Request Interface (PRI) feature is not available in both SMMUs interfacing with the
  PCIe & CCIX root ports.
- Currently only Micron 8GB /16GB single/dual Rank DIMMs (part number: 9ASF1G72PZ-2G6D1) are
  supported.
- Multichip use-case only enables access to peripherals and PCIe endpoints in the master chip.
- Stability issues have been observed on long stress tests of the system.
- On-board HDMI connection is not supported for graphics output. A PCIe graphics card can be used
  for graphics support.

Tagged Version - N1SDP-2019.09.13
----------------------------------------
New Features
^^^^^^^^^^^^
- This release is performance tuned stack.
- Supports dual rank 16GB DIMM and single rank 8GB DIMM @ 2667 MTS. Total 32GB or 16GB RAM could be accessible.
- Core frequency bumped up to 2.6GHz
- Workaround for Erratum 1315703 is disabled, so that the N1 CPU
  performance is improved in N1SDP. This may be applied for N1 software that does not require Spectre Variant 4 mitigation.
- Thermal shutdown supported - The system is shutdown automatically when the SOC temperature rises beyond 80 degrees.
- SLC Cache Stashing supported for increased PCIe ingress network packet performance.

Known Issues and Limitation
^^^^^^^^^^^^^^^^^^^^^^^^^^^
- PCIe/CCIX Link speed supports up to GEN3. GEN4 is yet not enabled.
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
- PCIe/CCIX Link speed supports up to GEN3. GEN4 is yet not enabled.
- No support for PCIe SRIOV.
- Currently only Micron 8GB single Rank DIMM (part number: 9ASF1G72PZ-2G6D1) is supported.CCIX traffic not supported over CCIX RC.



Tagged Version - N1SDP-ALPHA2-19.07
------------------------------------
New Features
^^^^^^^^^^^^
- All 4 Neoverse N1 cores running at 2.4 GHz.
- PCIe Link speed now supports GEN3 - 8 GT/s.
- Multicore SMP Linux 5.1 kernel.
- Full blown Ubuntu 18.04 distribution supported now.
- SMMUv3 enabled to support PCIe ATS.
- EDK2/EDK2-Platforms rebased from github. ACPI Tables updated to expose SMMU to kernel.
- Multi-segment support enabled. Now the CCIX RC and PCIe RC are both enabled, hence normal PCIe card will
  be functional in any of the PCIe/CCIX open slots available on the board from Linux.
- PCIe card hosting a switch is supported on the PCIe slot behind the PLX switch.
- DDR speed enhanced to 2667 MTS. Single rank 8 GB per DIMM (Total 16 GB RAM) supported.
- Boot sequence optimized to improve the boot time.

Known Issues and Limitation
^^^^^^^^^^^^^^^^^^^^^^^^^^^
- PCIe/CCIX Link speed supports up to GEN3. GEN4 is yet not enabled.
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
