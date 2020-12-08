Release Notes
=============

.. section-numbering::
    :suffix: .

.. contents::


Features and Fixes
------------------
The following is a summary of the key software features of the tagged N1SDP-2020.12.15 release.

- Yocto based BSP build to generate Poky distribution image and board firmware binary package.
- Restructuring the ubuntu build and packaging scripts to generate the custom ubuntu image.
- Support for both single and multi-chip configurations.

This release is made to restructure the N1SDP profile majorly considering the single and multi-chip profiles, for CCIX accelerator profile please refer to `N1SDP community portal`_.

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
  refer to `potential damage`_ page for more information

- Note: The case front panel USB 3.0 ports and & audio jacks are NOT connected/usable.
  They will be removed on later versions.

Known Issues or limitations
---------------------------
- If either of the two boards needs to boot-up in a single chip mode with a C2C setup,
  then the other board should be powered off.
- To boot a standard distribution on N1SDP platform the kernel must be patched
  with the PCIe quirks. See the article `PCIE`_
- PCIe root port is limited to GEN3 speed due to the on-board PCIe switch supporting maximum GEN3 speed.
- Page Request Interface (PRI) feature is not available in both SMMUs interfaced with PCIe root ports.
- Currently only Micron 8GB single Rank DIMM (part number: MTA9ASF1G72PZ-2G6D1) and
  16GB dual Rank DIMMs (part number:MTA18ASF2G72PDZ-2G6E1) are supported.
- Stability issues have been observed on long stress tests of the system.
- On-board HDMI connection is not supported for graphics output. PCIe graphics card can be used for graphics support.

Disclaimer
------------
- Limited Testing for now due to current global scenario, to be revisited once we get back on site.

Support
-------
For support email: support-subsystem-enterprise@arm.com

--------------

*Copyright (c) 2019-2020, Arm Limited. All rights reserved.*


.. _PCIE: pcie-support.rsti
.. _N1SDP community portal: https://community.arm.com/developer/tools-software/oss-platforms/w/docs/458/neoverse-n1-sdp
.. _potential damage: https://community.arm.com/developer/tools-software/oss-platforms/w/docs/604/notice-potential-damage-to-n1sdp-boards-if-using-latest-firmware-release
