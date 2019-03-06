How to build SGI-575 platform software to validate KVM feature
==============================================================

.. section-numbering::
    :suffix: .

.. contents::

What is KVM
-----------

Kernel Virtual Machine (KVM) is an virtualization module built in the linux
kernel which lets the user to turn linux into a hypervisor to allow hosting
single/multiple isolated guests or virtual machine. KVM requires a processor
with hardware virtualization extensions.

Currently, KVM is part of linux kernel. Some of the features of KVM are:

-  Over-committing     : KVM allows to allocate more virtulized CPU or memory
   for the virtual machine than that of the host.
-  Thin provisioning   : KVM allows to allocate and optimize the flexible
   storage for the virtual machines.
-  Disk throttling     : KVM allows to set limits fror disk I/O requests.
-  Virtual CPU hot plug: KVM allows ability to increase the CPU count of the
   virtual machine durting run time.


What does KVM test on SGI-575 demonstrate
-----------------------------------------

The SGI-575 platform demonstrates boot up 2+ instances of guest OS's using
`lvkm tool <https://github.com/lkvm/lkvm>`_. Linux KVM tool supports booting
guest OS's of the same architecture. For SGI-575 booting only ARM based virtual
machine is supported. KVM test for SGI-575 demonstrates booting
Linux Kernel v4.18 or Linux Kernel v4.13 as guest with Linux Kernel v4.18 as
the host.


Procedure to build KVM test for SGI platforms
---------------------------------------------

Execution of the KVM test requires booting a Fedora distribution system with the
kernel built for the SGI-575 platform. The first step would be to
get a `installed Fedora distribution`_ satadisk image and `prepare the image`_.
After the Fedora satadisk image has been prepared, the ``fedora.satadisk`` image
file has to be placed in the ``prebuilts/refinfra`` directory. Now, build the
firmware components and the kernel image needed for running the KVM test. For
generation of these image, the build command to be used is listed below.

To build the SGI software stack, the following command can be used

   ::

        ./build-scripts/sgi/build-test-kvm.sh -p sgi575 <command>

Supported command line options are listed below

   -  <command>

      -  Supported commands are

         -  ``clean``
         -  ``build``
         -  ``package``
         -  ``all`` (all the three above)


Examples of the build command are

   -   ::

        ./build-scripts/sgi/build-test-kvm.sh -p sgi575 all

      - This command cleans, builds and packages the SGI software stack needed
        for the KVM test for SGI-575 platform.

   -   ::

        ./build-scripts/sgi/build-test-kvm.sh -p sgi575 build

      - This command performs an incremental build of the software components
        included in the software stack for the SGI-575 platform. Note: this
        command should be followed by the 'package' command to complete the
        preparation of the fip and the disk image.

   -   ::

        ./build-scripts/sgi/build-test-kvm.sh -p sgi575 package

      - This command packages the previously build software stack and prepares
        the fip and the loads the kernel into the disk image.


Procedure for validating KVM test for SGI-575 platform
------------------------------------------------------

After the build for the KVM test is complete, to boot upto the Fedora login
prompt using the SGI software stack, the command to be used is

   ::

        cd model-scripts/sgi
        ./kvm.sh -p sgi575 -a <additional_params> -n [true|false]

Note: ``fedora.satadisk`` is expected at the location ``prebuilts/refinfra`` for
this command to work.

Supported command line options are listed below

   -  -n [true|false] (optional)

      -  Controls the use of network ports by the model. If network ports have
         to be enabled, use 'true' as the option. Default value is set to
         'false'.

   -  -a <additional_params>

      -  Specify any additional model parameters to be passed. The model
         parameters and the data to be passed to those parameters can be found
         in the FVP documentation.


Example commands to validate the KVM functionality are as listed below.

   -   ::

        ./kvm.sh -p sgi575

      - This command starts the execution of the SGI-575 model and the software
        boots upto the Fedora login prompt.

   -   ::

        ./kvm.sh -p sgi575 -n true

      - This command starts the execution of the SGI-575 model and the
        software boots upto the Fedora login prompt. The model supports
        networking allowing the software running within the model to access
        the network.

   -   ::

        ./kvm.sh -p sgi575 -n true -a "-C board.flash0.diagnostics=1"

      - This command starts the execution of the SGI-575 model with networking
        enabled and the software boots upto the Fedora login prompt. Additional
        parameters to the model are supplied using the -a command line
        parameter.


During the system boot, select the 'Fedora (refinfra) 27 (Server Edition)'
kernel on the grub menu. After the boot is complete, login as the root user.

   -  IMPORTANT: In the ``/root/`` directory, the lkvm executable is made
      available as part of the `prepare fedora disk process`_. Before using
      the lkvm tool, two dependencies (``glibc-static`` and ``libfdt-devel``)
      need to be installed using the ``yum`` tool. This requires
      `tap interface setup on the host`_ and the network parameter (``-n``) set
      to be true while starting the test. Enabling the network interface allows
      to model to connect to the internet through the network bridge interface
      of the host PC. The command to install the dependencies for ``lkvm`` is:

       -  ::

            yum install -y glibc-static libfdt-devel

   -  After the dependencies are installed, kvm test can be done using the
      following command:

       -  ::

            ./lkvm run -k <path-to-linux-image> -c 8 --irqchip gicv3 -p "console=ttyS0,115200 earlycon=uart,mmio,0x3f8 debug"

   -  For example to run the sgi kernel on the kvm, following command can be used:
       -  ::

            ./lkvm run -k /boot/vmlinux-refinfra -c 8 --irqchip gicv3 -p "console=ttyS0,115200 earlycon=uart,mmio,0x3f8 debug"

This completes the validation of the KVM functionality.

--------------

*Copyright (c) 2019, Arm Limited. All rights reserved.*

.. _installed Fedora distribution: fedora-test.rst
.. _prepare the image: prepare-fedora-disk.rst
.. _prepare fedora disk process: prepare-fedora-disk.rst
.. _tap interface setup on the host: create-tap-interface.rst
