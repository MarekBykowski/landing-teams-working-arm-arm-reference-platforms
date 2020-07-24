Release Notes
=============

.. section-numbering::
    :suffix: .

.. contents::


Features and Fixes
------------------
The following is a summary of the key software features of the tagged N1SDP-2020.07.27 release.

- Stability improvement over the GEN4 x16 link on CCIX slot. Verified with Mellanox Card (MCX516A-CDAT).
- Switched to user space dhcp client from the kernel space dhcp client for the initial ubuntu boot.
- Updated MCC firmware (mbb_v107) – This prompt for the recommended PMIC firmware.
- Added new PMIC firmware (300k_8c2) – This supports for boards manufactured post Nov 2019.
- Added latest PCC firmware (pcc_v050) – This allows to update of older boards.

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

- Update/Change board firmware only if MCC FW ask to do so,
  see here for more information
  https://community.arm.com/developer/tools-software/oss-platforms/w/docs/604/notice-potential-damage-to-n1sdp-boards-if-using-latest-firmware-release

- Note: The case front panel USB 3.0 ports and & audio jacks are NOT connected/usable.
  They will be removed on later versions.

PCIe Testing
------------
Limited PCIe testing done on:
- Mellanox ConnectX-5
- Xilinx U280 CCIX card

Known Issues or limitations
---------------------------
- If either of the two boards needs to boot-up in a single chip mode with a C2C setup,
  then the other board should be powered off.
- To boot a standard distribution on N1SDP platform the kernel must be patched
  with the PCIe quirks. See the article `PCIE`_
- PCIe root port is limited to GEN3 speed due to the on-board PCIe switch supporting maximum GEN3 speed.
- GEN4 x16 link in CCIX slot has not been performance tested.
- CCIX usecases (Accelerator/Multichip) is limited to GEN3 speed.
- Page Request Interface (PRI) feature is not available in both SMMUs interfaced with PCIe & CCIX root ports.
- Currently only Micron 8GB single Rank DIMM (part number: MTA9ASF1G72PZ-2G6D1) and
  16GB dual Rank DIMMs (part number:MTA18ASF2G72PDZ-2G6E1) are supported.
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
