CCIX Accelerator support on Neoverse N1SDP
==========================================

.. section-numbering::
    :suffix: .

.. contents::


CCIX Overview
-------------
Cache Coherent Interconnect for Accelerators (CCIX) is an architecture for data
sharing between a host(N1SDP) and peripheral attached memory and accelerators
connected to the CCIX aware PCIe Slot. CCIX provides coherency between
accelerators, processors and memory, enabling seamless data movement among them.
The CCIX architecture relieves the operating system, or drivers, from having to
execute cache management operations in either processor or accelerator caches,
when data is being shared between them.

For detailed description refer to `CCIX-consortium`_ to get the CCIX base
specification and software guide.

The CCIX PoC (Proof of Concept) software framework for N1SDP is based on the
Alveo-U280 FPGA and reliant on bit files and software deliverables from Xilinx.
These components are are not included in this release. Please contact Xilinx for
more information and for Alveo-U280 specific support issues using `Xilinx-Lounge`_

Alveo U280 card Installation
----------------------------

**Prerequisites**

The following hardware is required
 - N1SDP as the host
 - Xilinx Alveo U280 as the Accelerator Card

**Connect Alveo U280 card to N1SDP**

Follow the below steps to connect the Alveo U280 on N1SDP board:
    1. Switch off the SMPS switch on N1SDP to power off the board.
    2. Connect the Alevo U280 into the CCIX Slot.
    3. Connect power supply to the Alveo U280. Refer to `Xilinx-Lounge`_ on how
       to connect power supply to the card.
    4. Connect a micro USB cable between the Alveo U280 and the host preferably
       an x86 Ubuntu machine.
    5. Ensure software tools required by Alveo U280 are installed on the Host
       machine. Refer to `Xilinx-Lounge`_ on how to install them.

**Flash bitfiles on Alveo U280 Card**

    1. Refer to `Xilinx-Lounge`_ to power on Alveo U280 card.
    2. Refer to `run-on-n1sdp`_ to power ON the N1SDP board.
    3. Refer to `Xilinx-Lounge`_ to program the bitfiles on Alveo U280.
    4. Once the bitfiles have been flashed reboot the N1SDP board using
       ``REBOOT`` command in MCC console.

How to build CCIX on N1SDP
---------------------------
Refer to the `user-guide`_ to sync the software stack. Select the appropriate
option for CCIX accelerator usecase while syncing the software stack through the
sync script.
Refer to `Xilinx-Lounge`_ to apply patches on the stack required for the bitfile.
Refer to `run-on-n1sdp`_ to build the software stack.

Verification of CCIX Accelerator Framework
------------------------------------------
Refer to `run-on-n1sdp`_ to boot the N1SDP board. Once the board has booted edit
the file /etc/default/grub. Add pcie_acs_override=id:13b5:0100 option to the
GRUB_CMDLINE_LINUX_DEFAULT. Save this file and run update-grub command.

Install the below utility if not already present::

  $ apt-get install memtester

If the bit file has only Request Agent(RA), then there can be two traffic flows
which can be tested. These are:

    1. Host RA to Host HA
    2. Remote RA to Host HA

The above traffic flows are described in detail below.

**Host RA to Host HA**

This is the traffic within the host(N1SDP) and the traffic flow happens between
Host RA and Host HA. This can be tested with the following command::

  $ memtester 1M 1

In the above command, memtester utility is used to allocate and stress test 1 MB
of memory once. Refer to the memtester linux man page for the list of supported
options.

**Remote RA to Host HA**

This is the traffic between the Host(N1SDP) and Remote(Alveo U280) and the
traffic flow happens between Remote RA and Host HA. This can be tested with the
following commands for the relevant bitfiles::

  $ ./bind_tst -n <VFIO_ID>
  $ ./pri_tst -n <VFIO_ID>

Refer `Xilinx-Lounge`_ to get the binaries *<bind_tst>*, *<pri_tst>* and source code
of the proprietary test applications along with the *<VFIO_ID>* to be used for the
relevant bitfiles.

References
----------
- http://infocenter.arm.com/help/topic/com.arm.doc.101489_0000_01_en/arm_neoverse_n1_system_development_platform_technical_reference_manual_101489_0000_01_en.pdf

.. _CCIX-consortium: https://www.ccixconsortium.com/ccix-library/
.. _Xilinx-Lounge: https://www.xilinx.com/member/ccix.html

----------

*Copyright (c) 2020, Arm Limited. All rights reserved.*

.. _user-guide: ../../user-guide.rst
.. _run-on-n1sdp: ../run-on-n1sdp.rst
