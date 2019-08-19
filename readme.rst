Arm Reference Platforms
=======================

.. contents::

Introduction
------------

Arm produce open source software stacks for a variety of platforms, serving as a
reference to help enable product development based on Arm IP for a range of
target markets and applications.

We use these software stacks to demonstrate:

- Integration of multiple open source software components, including firmware,
  operating systems, applications, and services

- Upstream support for configuring the latest Arm IP

- Software features including secure boot, secure services, power management,
  and reliability/availablility/serviceability (RAS) error handling

- Alignment with Arm specifications and open source community initiatives


Software stacks
---------------

For Armv8-A platforms we provide integrated Linux and Android software stacks.

Mobile segment platforms include:

- SCP-firmware
- Trusted Firmware-A
- OP-TEE
- U-Boot port
- Android Common Kernel (ACK)
- Android Open Source Project (AOSP) based distribution with graphics support

Infrastructure segment platforms include:

- SCP-firmware
- Trusted Firmware-A
- EDK II UEFI port
- GRUB loaded distro such as Fedora Enterprise
- Booting multiple instances of a guest OS using Linux KVM & kvmtool is also
  supported

Rich IoT segment platforms include:

- Boot-firmware
- Trusted Firmware-A
- Mainline Linux kernel
- Yocto build and packaging using poky tiny filesystem

All platforms also support a basic Linux boot to a BusyBox ramdisk filesystem.

These software stacks are updated and tested as part of a quarterly release and
are made available to build from source, with prebuilt binaries also being
available for a limited subset of configurations.


Supported platforms
-------------------

The following platforms are supported:

- `Juno <https://community.arm.com/developer/tools-software/oss-platforms/w/docs/303/juno>`__
- `Neoverse N1 SDP <https://community.arm.com/developer/tools-software/oss-platforms/w/docs/440/neoverse-n1-sdp>`__
- `Armv8-A Base Platform FVP <https://community.arm.com/developer/tools-software/oss-platforms/w/docs/228/fvps>`__
- `Armv8-A Foundation Model FVP <https://community.arm.com/developer/tools-software/oss-platforms/w/docs/228/fvps>`__
- System Guidance for Mobile (SGM): `SGM-775 <https://community.arm.com/developer/tools-software/oss-platforms/w/docs/388/system-guidance-for-mobile-sgm>`__
- `TC2 <https://community.arm.com/developer/tools-software/oss-platforms/w/docs/227/tc2>`__
- `Corstone-700 <https://community.arm.com/developer/tools-software/oss-platforms/w/docs/444/corstone-700>`__
- `Cortex A5 DesignStart <https://community.arm.com/developer/tools-software/oss-platforms/w/docs/447/cortex-a5-designstart>`__

The following platforms are also supported, but currently require users to
manually sync the software stack sources:

- Neoverse Reference Design (RD): `RD-N1-Edge <https://developer.arm.com/products/system-design/reference-design/neoverse-reference-design>`__,
  `RD-E1-Edge <https://developer.arm.com/products/system-design/reference-design/neoverse-reference-design>`__

- System Guidance for Infrastructure (SGI): `SGI-575 <https://developer.arm.com/products/system-design/reference-design>`__


Getting started
---------------

Please follow the `user guide <docs/user-guide.rst>`__ to sync, build, and run an
Arm Reference Platforms software stack.

For questions and discussions, visit `our Arm Community forums <https://community.arm.com/developer/tools-software/oss-platforms/f/dev-platforms-forum>`__.

For additional resources, tutorials, and FAQs, browse the ``docs/`` directory or
visit `our wiki <https://community.arm.com/developer/tools-software/oss-platforms/w/docs>`__.

For technical support or to provide feedback, please contact us at `support@arm.com <mailto:support@arm.com>`__.
