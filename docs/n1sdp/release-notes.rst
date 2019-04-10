Release Notes
=============

.. section-numbering::
    :suffix: .

.. contents::


Features
--------
The following is a summary of the key software features of the ALPHA1 release.

- Multicore SMP Linux 5.0 kernel booting to an OpenEmbedded LAMP filesystem.
- All 4 Neoverse N1 cores running at 2 GHz.
- All on board PCIe devices USB3/GbE/SATA enabled and functional.
- 16GB DDR4 memory running at 1600MT/s speed.


Precautions
-----------
- The system thermal monitoring and control features are not yet calibrated,
  therefore do not operate the unit above room temperature (approximately 25°C):

  - The thermal shutdown features are currently disabled.
  - The chassis fan speed is currently fixed.

- The N1 SDP is intended for use within a laboratory or engineering development
  environment. Do not use the N1 SDP near equipment that is sensitive to
  electromagnetic emissions, for example, medical equipment.

- Never subject the board to high electrostatic potentials.
  Observe Electrostatic Discharge (ESD) precautions when handling any board.

  - Always wear a grounding strap when handling the board.
  - Avoid touching the component pins or any other metallic elements.

- Note: The case front panel USB 3.0 ports and & audio jacks are NOT connected/usable.
  They will be removed on later versions.


Known Issues or limitations
---------------------------
- To boot a standard distribution on N1SDP platform the kernel must be patched
with the PCIe quirks. See the article `PCIE`_
- PCIe slots limited testing done with few cards like SATA card and GbE card.
- PCIe tested with GEN1 speed only.
- No support for PCIe SRIOV.
- CCIX RC not supported.

Support
-------
For support email: support-subsystem-enterprise@arm.com

--------------

*Copyright (c) 2019, Arm Limited. All rights reserved.*


.. _PCIE: pcie-support.rst
