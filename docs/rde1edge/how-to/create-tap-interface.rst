How to create tap interface to enable networking for FVPs
=========================================================


.. section-numbering::
    :suffix: .

.. contents::


Context
-------

RD-E1-Edge fast model supports virtual networking and it can interface with the
host PC network through the tap interface setup on the host machine. The steps
to setup a TAP interface on the host PC are listed below. This requires Ubuntu
16.04 or Ubuntu 18.04 as the host PC.


How to setup tap interface
--------------------------

- Install the ``bridge-utils`` package

  ::

        sudo apt-get install bridge-utils

- The first step is to create a bridge and add the host PC network as its
  interface. Here, ``br0`` is the bridge name and ``enp0s3`` is the host PC
  network device name. Replace these names with the names of the interfaces
  used on the host PC.

  ::

        sudo brctl addbr br0
        sudo brctl addif br0 enp0s3
        sudo ifconfig enp0s3 0.0.0.0
        sudo ifconfig br0 up
        sudo dhclient br0

- Next setup is to add the tap interface. Here, ``tap0`` is the name of the tap
  interface.

  ::

        sudo ip tuntap add dev tap0 mode tap user $(whoami)
        sudo ifconfig tap0 0.0.0.0 promisc up
        sudo brctl addif br0 tap0

Note: These steps do not make a persistent instance of the bridge and the tap
interface. After the host PC reboots, these steps have to be repeated again.

Refer `this documentation <https://wiki.linuxfoundation.org/networking/bridge>`_
for more details.

--------------

*Copyright (c) 2019, Arm Limited. All rights reserved.*
