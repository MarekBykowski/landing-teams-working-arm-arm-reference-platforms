CoreSight support on Neoverse N1 SDP
====================================

.. section-numbering::
    :suffix: .

.. contents::


CoreSight Introduction
----------------------
CoreSight Debug and Trace components are invariably described in a graph-like
topology which describes the port connections amongst the various components.
The topology includes, but is not limited to, the following major components.

* ETM(s)
* ETF(s)/ETB(s)
* Dynamic/Static Funnel(s)
* Dynamic/Static Replicator(s)
* TPIU(s)/ETR(s)

In CoreSight terminology, a component can be roughly described as a source -
that produces/generates the debug & trace data, and/or a sink - that consumes/stores
the data, or a link - which routes the data.
Depending on the "type" of component, it may have 1 or more input port(s),
1 or more output port(s), a single input port only, or a single output port only.

For instance -

* ETM is a source component which only has a single output port.
* TPIU/ETR is a sink component which only has a single input port.
* Funnel is a link component which can be thought of as a MUX having multiple
  input ports and a single output port.
* Replicator is a link component which can be thought of as a DEMUX having a single
  input port and multiple output ports.
* ETF is a link component which can act both as a source and a sink (it has a
  FIFO buffer to store the data) and thus has a single input and a single output port.

Refer to `CoreSight_Technical_Introduction`_ for more information about
CoreSight Debug and Trace elements.

It is worth mentioning that all static components in CoreSight world are not
addressable and only facilitate intermediate connections between the other
non-static/Dynamic CoreSight components. They are, however, described in the
DT/ACPI and get discovered by their respective kernel drivers.

CoreSight components can be described either/both in a device tree or/and in a
DSDT table within ACPI - similar to other components/peripherals, to get
enumerated by the Linux kernel.

Every CoreSight component has a corresponding kernel driver which takes care of
its initialization. There are configuration changes required in the kernel to
build the appropriate CoreSight components' drivers.

Upon a successful probe of a CoreSight component driver, the particular
component gets enumerated under ``/dev`` and appears under ``/sys/bus/coresight/devices/``
in the booted kernel.

Enabling CoreSight on N1SDP
---------------------------

* ACPI bindings:

	CoreSight topology for N1SDP has been described as a _DSD graph within DSDT
	table for N1SDP package - the support is enabled by default.


* Linux Kernel:

	The default configuration for the kernel is to build without the CoreSight drivers.
	The build flag to enable CoreSight kernel configuration options to build CoreSight
	kernel drivers is ``LINUX_CORESIGHT_BUILD_ENABLED`` which is set to ``0`` by default.
	Modify the file ``n1sdp`` under ``build_scripts/platforms/n1sdp`` by setting
	``LINUX_CORESIGHT_BUILD_ENABLED`` to ``1`` from its default ``0``.

Verifying CoreSight support
---------------------------

Assuming the kernel has been built with the CoreSight configuration, the booted
kernel should have CoreSight components enumerated under sysfs within
``/sys/bus/coresight/devices/``. The components should also be seen listed under ``/dev``.

Running perf with CoreSight
---------------------------

CoreSight framework has been integrated with the standard perf core in the kernel
to assist with trace capturing and decoding. To exercise this, perf needs to be
built with openCSD (Open CoreSight Decoding) library support.

Execute the following script to build the perf executable with open CSD library

		::

		./build-scripts/build-perf.sh

This will generate the perf executable in the output/n1sdp/build_artifact/ directory which
can then be transferred to the kernel running on the N1SDP board.

Here's an example showcasing trace capture and decode of a simple application:

1. Build the demo application code:

   *aarch64-linux-gnu-gcc -static -o test main.c*

..	code-block::

	#include <stdio.h>

	int main()
	{
		printf("N1SDP\n");

		return 0;
	}

2. Disassemble the binary:

   *aarch64-linux-gnu-objdump test.out*

..	code-block::

	0000000000400580 <main>:
	400580:	a9bf7bfd 	stp	x29, x30, [sp,#-16]!
	400584:	910003fd 	mov	x29, sp
	400588:	90000000 	adrp	x0, 400000 <_init-0x3b0>
	40058c:	9118e000 	add	x0, x0, #0x638
	400590:	97ffffa4 	bl	400420 <puts@plt>
	400594:	52800000 	mov	w0, #0x0
	400598:	a8c17bfd 	ldp	x29, x30, [sp],#16
	40059c:	d65f03c0 	ret

3. Trace the application from the start address ``0x400580`` to ``0x4006f0``

   *./perf record -e cs_etm/@tmc_etr0/u --filter 'start 0x400580@test, stop 0x4006f0@test' --per-thread ./test*

   This step will generate *perf.data* in the current working directory.

4. Decode the trace data with perf

   *./perf report --stdio --dump*

   This step will dump all the captured trace data on stdio.

Refer to the man page of ``perf-record`` for more information on perf options, filters, etc.

References
----------

- http://infocenter.arm.com/help/topic/com.arm.doc.epm039795/coresight_technical_introduction_EPM_039795.pdf?_ga=2.263237196.1385850732.1581332707-419757503.1576059061
- http://infocenter.arm.com/help/topic/com.arm.doc.101489_0000_01_en/arm_neoverse_n1_system_development_platform_technical_reference_manual_101489_0000_01_en.pdf
- https://www.linaro.org/blog/stm-and-its-usage/


.. _CoreSight_Technical_Introduction: http://infocenter.arm.com/help/topic/com.arm.doc.epm039795/coresight_technical_introduction_EPM_039795.pdf?_ga=2.263237196.1385850732.1581332707-419757503.1576059061

--------------


*Copyright (c) 2019-2020, Arm Limited. All rights reserved.*

