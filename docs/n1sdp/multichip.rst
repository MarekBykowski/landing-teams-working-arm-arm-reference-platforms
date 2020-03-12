Multichip SMP boot on Neoverse N1 SDP with CCIX
===============================================

.. section-numbering::
    :suffix: .

.. contents::


Introduction
------------
The Neoverse N1 System Development Platform (N1SDP) supports dual socket operation wherein
two N1SDP boards are connected over a CCIX enabled PCIe link. One board is designated as the
master board whose CCIX enabled PCIe controller is configured in root port mode and the other
board is configured as slave board whose CCIX enabled PCIe controller is configured in
endpoint mode. Linux boots in the master board and powers ON the slave board cores such that
the operating system sees CPU cores and memories from both master and slave boards in separate
NUMA nodes making a dual socket SMP configuration.

Note:
Only cores and DDR memory from slave chip are exposed to the operating system. No I/O peripherals
from slave chip are exposed to the operating system.

Connection Details
------------------
For the purpose of connecting two N1SDP boards over PCIe link, a specialized PCIe riser card
(Part No: V2M-N1SDP-0343A) has to be used. The riser card package includes two PCIe form factor
riser cards, two high speed low latency PCIe cables and one USB cable (for PCIe REFCLK).
A 20-pin flat ribbon cable that comes along with N1SDP board accessories should also be used. This
is used for I2C connection between master and slave board SCP & MCP and other timer synchronization
handshake signals.
Setup has to be made following the steps given below:

    1. Designate one N1SDP board as master board and the other N1SDP board as slave board.
    2. Ensure that both board are powered off.
    3. Plug in the riser cards, one in each board, in the CCIX slot (the last x16 PCIe slot
       close to the edge of the board).
    4. Connect the high speed PCIe cables between the riser cards in respective slots
       (make one to one connection and not criss-cross connection).
    5. Connect the USB cable between the riser cards.
    6. Connect the 20-pin flat ribbon cable between the boardsto the connector named as 'C2C'
       which should be in the back side of the board.
    7. Connect the USB/SATA boot media to the respective slot in the master board.

Board Files Setup
-----------------
    1. Power ON the master board and open the MCC console of master board using a terminal
       application (like minicom or putty).
    2. Run USB_ON command which mounts the micro SD card content of master board in host machine.
    3. Assuming the micro SD card is mounted with the name 'MASTER' in host. Open the file
       MASTER/MB/HBI0316A/board.txt file and note the APPFILE name. It should be like 'io_v123f.txt'
       or similar.
    4. Now close the board.txt file and open the io_v123f.txt (the one noted in step 3) which will
       be in the same folder.
    5. Set the C2C_ENABLE flag as TRUE and C2C_SIDE flag as MASTER.
    6. Set the SCC PLATFORM_CTRL register to enable multichip mode and CHIPID=0. For this, uncomment
       the SOCCON with offset 0x1170 and set the value 0x00000100
       The line should now read: **SOCCON: 0x1170 0x00000100 ; SoC SCC PLATFORM_CTRL**
    7. Save and close the file. If the host is Linux run a 'sync' command in one of the terminals to
       be safe.
    8. Repeat from step 1 to 4 for slave board. Let's assume host has mounted the slave board's
       micro SD card with name 'SLAVE'.
    9. Set the C2C_ENABLE flag as TRUE and C2C_SIDE flag as SLAVE.
    10. Set the PLATFORM_CTRL register to enable multichip mode and CHIPID=1. For this, uncomment
        the SOCCON with offset 0x1170 and set the value 0x00000101. Save and close the file. Run
        sync command in case of Linux host.
        The line should now read: **SOCCON: 0x1170 0x00000101 ; SoC SCC PLATFORM_CTRL**

Booting the Setup
-----------------
    1. Copy all the firmware binaries to SOFTWARE folder in both master and slave board's micro SD
       card. Run sync command in case of Linux host. Note that uefi.bin file is not required to be
       copied to slave micro SD card as UEFI will be run only in the master chip.
       For getting the sources and building the binaries please refer to `user-guide`_
    2. Shutdown both the boards.
    3. Reboot the slave board first and let it boot. Then reboot the master board. This is done
       because the SCP firmware running in master board expects the slave board to respond to the
       I2C command when it boots. If the slave board is not responding for the I2C command then
       master assumes that it is running in single chip environment and continues to boot in single
       chip mode. This is explicitly done to avoid any delays in waiting for slave to respond that
       will affect single chip environment where there is no slave connected at all.
    4. If master SCP finds a slave connected and responding then master SCP will perform several
       handshakes with slave SCP to bring-up the CCIX link and boot the slave chip's cores.

After Booting
-------------
    1. UEFI's Dynamic ACPI framework exposes both master and slave chip's processors and memories to
       Linux. Assuming 16GB DDR memory connected each on master and slave boards, Linux will see
       8 cores (4 cores in master chip + 4 cores in slave chip) and 32GB DDR memory space.
    2. Once Linux has booted, /proc/cpuinfo and /proc/meminfo can be dumped to see the total core
       and memory information that Linux currently sees.
    3. Also the slave board resources (slave CPUs and slave DDR memory) is treated as separate NUMA
       node in Linux which can be seen using the numactl --hardware command.

Limitations
-----------
    1. Though the multichip high speed connection is made using CCIX enabled PCIe controllers which
       supports GEN4 speed, only GEN3 speed has been validated for multichip operation. This affects
       the cross-chip memory access latency.
    2. The timer synchronization internal logic doesn't accounted for the external sync signals pad
       timings. So the PIK clock for timer synchronization module has to be reduced to 150MHz from
       actual 800MHz.
    3. The REFCLK counter values on both master and slave chips has to be reset before starting the
       synchronization process.
    4. Timer synchronization interrupt flag has no information on the source of interrupt. So
       synchronization is retriggered everytime an interrupt was hit.

References
----------
- http://infocenter.arm.com/help/topic/com.arm.doc.101489_0000_01_en/arm_neoverse_n1_system_development_platform_technical_reference_manual_101489_0000_01_en.pdf
- https://www.ccixconsortium.com/ccix-library/

----------

*Copyright (c) 2020, Arm Limited. All rights reserved.*

.. _user-guide: ../user-guide.rst
