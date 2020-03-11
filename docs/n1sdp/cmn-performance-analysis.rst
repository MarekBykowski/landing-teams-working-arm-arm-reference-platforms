CMN-600 perf example on Neoverse N1 SDP
=======================================
The goal of this document is to give a short introduction on CMN-600
performance analysis on N1SDP.
This includes driver load verification and Linux perf usage examples.

The examples include examples such as system level cache access and traffic to
and from PCI-E devices from the view of the interconnect.

.. section-numbering::
    :suffix: .

.. contents::


Support in Arm's Neoverse N1 SDP software release
-------------------------------------------------
The software support for CMN-600 performance analysis can be divided into three
components:

* The user space Linux perf tool
* The Linux kernel arm-cmn driver
* EDK2 (DSDT table entry)

The default build of the supplied Neoverse software stack will include all
necessary changes and patches to test and explore CMN-600 performance analysis.


CMN-600 Topology and NodeIDs on Neoverse N1 SDP
-----------------------------------------------
The PMUs in CMN-600 are distributed to the nodes of the mesh interconnect.
NodeType specific events are configured per node.
Event counting is done by local counters in the XP attached to the node.
Global counters are in the Debug Trace Controller (DTC).
The arm-cmn driver uses local/global register pairing to provide 64-bit event
counters (see "Counter Allocation" section below).

All the nodes are referenced by NodeID and NodeType.
PMU events must specify the NodeID of the node on which it is to be counted
using the nodeid= parameter.
A summary of Node ID can be found the table below.
For more details contact support (support-subsystem-enterprise@arm.com).

+---------------------------------+-----------+---------+--------------------+
| Purpose                         | Node Type | Node ID | Event Name         |
+---------------------------------+-----------+---------+--------------------+
| System-Level Cache slices (SLC) | HNF       | 0x24    | arm_cmn/hnf        |
|                                 |           | 0x28    |                    |
|                                 |           | 0x44    |                    |
|                                 |           | 0x48    |                    |
+---------------------------------+-----------+---------+--------------------+
| PCI_CCIX (Expansion slot 4)     | RND       | 0x08    | arm_cmn/rnid       |
+---------------------------------+-----------+---------+--------------------+
| PCI_0 (All other PCI-E)         | RND       | 0x0c    | arm_cmn/rnid       |
+---------------------------------+-----------+---------+--------------------+
| Mesh interconnections           | XP        | 0x00    | arm_cmn/mxp        |
|                                 |           | 0x08    |                    |
|                                 |           | 0x20    |                    |
|                                 |           | 0x28    |                    |
|                                 |           | 0x40    |                    |
|                                 |           | 0x48    |                    |
|                                 |           | 0x60    |                    |
|                                 |           | 0x68    |                    |
+---------------------------------+-----------+---------+--------------------+
| Debug Trace Controller          | DTC       | 0x68    | arm_cmn/dtc_cycles |
+---------------------------------+-----------+---------+--------------------+
| ACE-lite slave                  | SBSX      | 0x64    | arm_cmn/sbsx       |
+---------------------------------+-----------+---------+--------------------+

For details on what is connected to PCI_0 check the N1SDP TRM (Figure 2-9
PCI Express and CCIX system).

Software components
-------------------

Linux perf tool
###############
No modifications of ``perf`` source is needed.
The user can opt to use any perf compatible with the built kernel or use the
included script ``build-scripts/build-perf.sh`` to build a static linked binary
from the included kernel source (binary is created as
``output/n1sdp/build_artifact/perf``).


ACPI DSDT modification
######################
The Linux driver expects a DSDT entry that describe the location of the CMN-600
configuration space.
This is included in the supplied Neoverse software stack.

Linux perf driver (arm-cmn)
###########################
The included arm-cmn driver is a work-in-progress.
A Snapshot of this driver is included in the supplied Neoverse software stack.
The driver is controller by ``CONFIG_ARM_CMN`` (enabled in default software
stack build).

Counter Allocation/Limitation
*****************************
The arm-cmn driver provides 64-bit event counts for any given event.
It accomplishes this using a combination of combined-pair local counters (in an
DTM/XP) and (uncombined) global counters (in the DTC):

* DTM/XP
    Can provide up to two 32-bit local counters (built from paired 16-bit
    counters por_dtm_pmevcnt0+1, and 2+3) for events from itself and/or the
    up-to-2 devices that are connected to its ports.

    Overflows from these counters are sent to its DTC's global counters.
    This means only up to 2 events from any of the devices connected to an XP
    can be counted at the same time without sampling.


* DTC
    Each DTC can provide up to 8 global counters (por_dt_pmevcntA .. H).
    This means only up to 8 events in a DTC domain can be counted at the same
    time without sampling.

For example, the N1SDP's two PCI-Express root complexes' RND (PCI_CCIX on RND3
at NodeID 0x8 and PCI0 on RND4 at NodeID 0xC), hang off of the same XP (0,1).
Only up to 2 RND events from either of the two PCI-E domains can be measured
simultaneously without sampling; 3 or more will require sampling.

In the following example, we try to measure 4 RND events, but perf is only
giving 50% sampling time for each count because the events have to share local
counters in the XP.
::

 $ perf stat -a \
     -e arm_cmn/rnid_txdat_flits,nodeid=8/ \
     -e arm_cmn/rnid_txdat_flits,nodeid=12/ \
     -e arm_cmn/rnid_rxdat_flits,nodeid=8/ \
     -e arm_cmn/rnid_rxdat_flits,nodeid=12/ \
     -I 1000
 #           time  counts unit events
      1.000089438       0      arm_cmn/rnid_txdat_flits,nodeid=8/     (50.00%)
      1.000089438       0      arm_cmn/rnid_txdat_flits,nodeid=12/    (50.00%)
      1.000089438       0      arm_cmn/rnid_rxdat_flits,nodeid=8/     (50.00%)
      1.000089438       0      arm_cmn/rnid_rxdat_flits,nodeid=12/    (50.00%)
      2.000231897      79      arm_cmn/rnid_txdat_flits,nodeid=8/     (50.01%)
      2.000231897       0      arm_cmn/rnid_txdat_flits,nodeid=12/    (50.01%)
      2.000231897       0      arm_cmn/rnid_rxdat_flits,nodeid=8/     (49.99%)

PMU Events
**********
``perf list`` shows the perfmon events for the node types that are detected by
the arm-cmn driver.
If a node type is not detected, perf list will not show the events for that
node type.
::

    # perf list | grep arm_cmn/hnf
    arm_cmn/hnf_brd_snoops_sent/                       [Kernel PMU event]
    arm_cmn/hnf_cache_fill/                            [Kernel PMU event]
    arm_cmn/hnf_cache_miss/                            [Kernel PMU event]
    arm_cmn/hnf_cmp_adq_full/                          [Kernel PMU event]
    arm_cmn/hnf_dir_snoops_sent/                       [Kernel PMU event]
    arm_cmn/hnf_intv_dirty/                            [Kernel PMU event]
    arm_cmn/hnf_ld_st_swp_adq_full/                    [Kernel PMU event]
    arm_cmn/hnf_mc_reqs/                               [Kernel PMU event]
    arm_cmn/hnf_mc_retries/                            [Kernel PMU event]
    [...]

The perfmon events are described in the CMN-600 TRM in the register description
section for each node type's perf event selection register (at offset 0x2000 of
each node that has a PMU).

CMN-600 TRM register summary (links to all of the node types' offset registers).
    http://infocenter.arm.com/help/index.jsp?topic=/com.arm.doc.100180_0201_00_en/bry1447971081070.html


Specifying NodeID to events in perf
***********************************
To program the CMN-600's PMUs, the NodeIDs of the components need to be
specified for each event using a nodeid= parameter.
Example:
::

    $ perf stat -a -I 1000 -e arm_cmn/hnf_mc_reqs,nodeid=0x24/


Multiple nodes can be specified for an event using bash brace expansion.
Note the comma after the -e.
::

    $ perf stat -a -I 1000 \
        -e,arm_cmn/hnf_mc_reqs,nodeid={0x24,0x28,0x44,0x48}/


Separate events on the same nodes with brace expansion should be specified
using separate -e.
::

    $ perf stat -a -I 1000 \
        -e,arm_cmn/hnf_mc_reqs,nodeid={0x24,0x28,0x44,0x48}/ \
        -e,arm_cmn/hnf_mc_retries,nodeid={0x24,0x28,0x44,0x48}/

Note this form requires the trailing '/' at the end of the event name.


Driver verification
-------------------
To verify that the arm-cmn has successfully loaded different ways:

* Check if any arm_cmn entires is available
    ::

     $ perf list | grep arm_cmn
     arm_cmn/dn_rxreq_dvmop/                            [Kernel PMU event]
     arm_cmn/dn_rxreq_dvmop_vmid_filtered/              [Kernel PMU event]
     arm_cmn/dn_rxreq_dvmsync/                          [Kernel PMU event]
     arm_cmn/dn_rxreq_retried/                          [Kernel PMU event]
     arm_cmn/dn_rxreq_trk_occupancy_all/                [Kernel PMU event]
     arm_cmn/dn_rxreq_trk_occupancy_dvmop/              [Kernel PMU event]
     [...]


* Sysfs entries
    ::

     $ ls -x /sys/bus/event_source/devices/arm_cmn/
     cpumask
     dtc_domain_0
     events
     format
     perf_event_mux_interval_ms
     power
     subsystem
     type
     uevent


Example
-------

HN-F PMU
########
Make sure to issue some memory load operation(s) in parallel, such as
memtester, while executing the following perf example.

Memory Bandwidth using hnf_mc_reqs
**********************************
Measure memory bandwidth using hnf_mc_reqs; assumes bandwidth comes from SLC
misses.
::

 $ perf stat -e,arm_cmn/hnf_mc_reqs,nodeid={0x24,0x28,0x44,0x48}/ -I 1000 -a
 2.000394365        121,713,206      arm_cmn/hnf_mc_reqs,nodeid=0x24/
 2.000394365        121,715,680      arm_cmn/hnf_mc_reqs,nodeid=0x28/
 2.000394365        121,712,781      arm_cmn/hnf_mc_reqs,nodeid=0x44/
 2.000394365        121,715,432      arm_cmn/hnf_mc_reqs,nodeid=0x48/
 3.000644408        121,683,890      arm_cmn/hnf_mc_reqs,nodeid=0x24/
 3.000644408        121,685,839      arm_cmn/hnf_mc_reqs,nodeid=0x28/
 3.000644408        121,682,684      arm_cmn/hnf_mc_reqs,nodeid=0x44/
 3.000644408        121,685,669      arm_cmn/hnf_mc_reqs,nodeid=0x48/


Generic bandwith formula:
::

 hnf_mc_reqs/second/hnf node  * 64 bytes = X MB/sec

Subsitute with data from perf output:
::

 (121713206 + 121715680 + 121712781 + 121715432) * 64 = 29715 MB/sec



PCI-E RX/TX bandwidth
#####################
The RN-I/RN-D events are defined from the perspective of the bridge to the
interconnect, so the "rdata" events are outbound writes to the PCI-E device
and "wdata" events are inbound reads from PCI-E.

Measure RND (PCI-E) bandwidth to/from NVMe SSD when running fio
***************************************************************
The NVMe SSD (Optane SSD 900P Series) is on PCI-E Root Complex 0 (PCI0, the
Gen3 slot, behind the PCI-E switch).

Run ``fio`` to read from NVME SSD using 64KB block size for 1000 seconds in
one terminal:
::

 $ fio \
     --ioengine=libaio --randrepeat=1 --direct=1 --gtod_reduce=1 \
     --time_based --readwrite=read --bs=64k --iodepth=64k --name=r0 \
     --filename=/dev/nvme0n1p5 --numjobs=1 --runtime=10000
 r0: (g=0): rw=read, bs=(R) 64.0KiB-64.0KiB, (W) 64.0KiB-64.0KiB, (T) 64.0KiB-64.0KiB, ioengine=libaio, iodepth=65536
 fio-3.1
 Starting 1 process
 ^Cbs: 1 (f=1): [R(1)][0.5%][r=2586MiB/s,w=0KiB/s][r=41.4k,w=0 IOPS][eta 16m:35s]
 fio: terminating on signal 2

 r0: (groupid=0, jobs=1): err= 0: pid=1443: Thu Dec 19 12:12:10 2019
    read: IOPS=41.3k, BW=2581MiB/s (2706MB/s)(12.3GiB/4894msec) <------------------------------- read bandwidth = 2706 MB/sec
    bw (  MiB/s): min= 2276, max= 2587, per=98.10%, avg=2532.02, stdev=125.43, samples=6
    iops        : min=36418, max=41392, avg=40512.33, stdev=2006.90, samples=6
   cpu          : usr=3.15%, sys=35.15%, ctx=16686, majf=0, minf=1049353
   IO depths    : 1=0.1%, 2=0.1%, 4=0.1%, 8=0.1%, 16=0.1%, 32=0.1%, >=64=100.0%
      submit    : 0=0.0%, 4=100.0%, 8=0.0%, 16=0.0%, 32=0.0%, 64=0.0%, >=64=0.0%
      complete  : 0=0.0%, 4=100.0%, 8=0.0%, 16=0.0%, 32=0.0%, 64=0.0%, >=64=0.1%
      issued rwt: total=202101,0,0, short=0,0,0, dropped=0,0,0
      latency   : target=0, window=0, percentile=100.00%, depth=65536

 Run status group 0 (all jobs):
    READ: bw=2581MiB/s (2706MB/s), 2581MiB/s-2581MiB/s (2706MB/s-2706MB/s), io=12.3GiB (13.2GB), run=4894-4894msec

 Disk stats (read/write):
   nvme0n1: ios=202009/2, merge=0/19, ticks=4874362/51, in_queue=3934760, util=98.06%

Measure with ``perf`` in an other terminal.
Measure rdata/wdata beats.  Each beat is 32 bytes.
::

 $ perf stat -e,arm_cmn/rnid_s0_{r,w}data_beats,nodeid=0xc/ -I 1000 -a
 3.000383383            248,145      arm_cmn/rnid_s0_rdata_beats,nodeid=0xc/
 3.000383383         84,728,162      arm_cmn/rnid_s0_wdata_beats,nodeid=0xc/
 4.000522271            248,199      arm_cmn/rnid_s0_rdata_beats,nodeid=0xc/
 4.000522271         84,743,908      arm_cmn/rnid_s0_wdata_beats,nodeid=0xc/
 5.000680779            248,209      arm_cmn/rnid_s0_rdata_beats,nodeid=0xc/
 5.000680779         84,746,976      arm_cmn/rnid_s0_wdata_beats,nodeid=0xc/
 6.000835927            247,899      arm_cmn/rnid_s0_rdata_beats,nodeid=0xc/
 6.000835927         84,417,098      arm_cmn/rnid_s0_wdata_beats,nodeid=0xc/

Calculate read bandwidth from perf measurement:
::

 84.74e6 wdata beats * 32 bytes per beat = 2711 MB/sec

Measure RND (PCI-E) bandwidth from Ethernet NIC
***********************************************
``netperf`` is executed on the N1SDP to generate network traffic.

``netperf`` executing in on terminal...
::

 $ netperf -D 10 -H remote-server-in-astlab -t TCP_MAERTS -l 0
 Interim result:  941.52 10^6bits/s over 10.000 seconds ending at 1576269135.608
 Interim result:  941.52 10^6bits/s over 10.000 seconds ending at 1576269145.608
 Interim result:  941.52 10^6bits/s over 10.000 seconds ending at 1576269155.608
 Interim result:  941.52 10^6bits/s over 10.000 seconds ending at 1576269165.608

...and ``perf`` in an other at the same time.
::

 $ perf stat -e,arm_cmn/rnid_s0_{r,w}data_beats,nodeid=0xc/ -I 1000 -a
 12.001904404            308,803      arm_cmn/rnid_s0_rdata_beats,nodeid=0xc/
 12.001904404          4,024,328      arm_cmn/rnid_s0_wdata_beats,nodeid=0xc/
 13.002047284            308,994      arm_cmn/rnid_s0_rdata_beats,nodeid=0xc/
 13.002047284          4,024,287      arm_cmn/rnid_s0_wdata_beats,nodeid=0xc/
 14.002233364            309,035      arm_cmn/rnid_s0_rdata_beats,nodeid=0xc/
 14.002233364          4,024,470      arm_cmn/rnid_s0_wdata_beats,nodeid=0xc/
 15.002390125            309,162      arm_cmn/rnid_s0_rdata_beats,nodeid=0xc/
 15.002390125          4,024,376      arm_cmn/rnid_s0_wdata_beats,nodeid=0xc/

Calculate bandwidth from perf measurement:
::

 4.024e6 wdata beats/second * 32 bytes/beat * 8 bits/byte = 1030e6 bits/second


*Copyright (c) 2019, Arm Limited. All rights reserved.*
