Release Notes
=============

.. section-numbering::
    :suffix: .

.. contents::


Features and Fixes
------------------
The following is a summary of the key software features of the tagged N1SDP-2020.03.26 release.

- CCIX accelerator support with CCIX endpoint having a Request Agent (RA).
    - Reference CCIX platform library in EDK2-Platforms will dynamically discover the endpoint RA topology and configures both the N1SDP host and CCIX endpoint.
    - The framework is verified with the endpoint Requesting Agent design programmed in Xilinx Alveo U280 accelerator FPGA card.
    - For all CCIX specific documents please refer to the CCIX consortium link: https://www.ccixconsortium.com/ccix-library/
    - Please contact CCIX consortium to get access to the documents if not already available.
    - Please contact Xilinx for supporting bit files and userspace applications for the Alveo-U280

- Multichip SMP support over CCIX/PCIe link.
    - Dual socket SMP boot with two N1SDP boards connected over CCIX/PCIe link.
    - Linux sees 8 cores and DDR memories from both master and slave N1SDP boards.
    - CCIX/PCIe link running at GEN3 x16 speed.

- PCIe GEN4 x16 support in CCIX slot. GEN4 x16 link verified with Mellanox Card (MCX516A-CDAT). No performance benchmark/tuning has been done.
- PMU counter support for CMN-600.
- Coresight Debug/Trace support.
- PCIe SRIOV framework support. Tested with Intel X540-T2 card.
- Device tree support with busybox filesystem [Experimental]. Only supported when building from sources. Simple Busybox filesystem offers limited functionality.

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
- PEXSAT34 - Two SATA controller behind switch (GEN2 X2)
- Xilinx U280 CCIX card.


Known Issues or limitations
---------------------------
- To boot a standard distribution on N1SDP platform the kernel must be patched
  with the PCIe quirks. See the article `PCIE`_
- PCIe root port is limited to GEN3 speed due to the on-board PCIe switch supporting maximum GEN3 speed.
- GEN4 x16 link in CCIX slot has not been performance tested.
- CCIX usecases (Accelerator/Multichip) is limited to GEN3 speed.
- Page Request Interface (PRI) feature is not available in both SMMUs interfaced with PCIe & CCIX root ports.
- Currently only Micron 8GB /16GB single/dual Rank DIMMs supported (part number: 9ASF1G72PZ-2G6D1) are supported.
- Multichip usecase does not enable peripheral access in the slave chip.
- Stability issues have been observed on long stress tests of the system.
- On-board HDMI connection is not supported for graphics output. PCIe graphics card can be used for graphics support.

Disclaimer
------------
- Limited Testing for now due to current global scenario, to be revisited once we get back on site.

Support
-------
For support email: support-subsystem-enterprise@arm.com

--------------

*Copyright (c) 2019, Arm Limited. All rights reserved.*


.. _PCIE: pcie-support.rst
