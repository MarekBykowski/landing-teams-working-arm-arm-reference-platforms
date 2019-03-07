How to setup PXE server on Ubuntu
=================================


.. section-numbering::
    :suffix: .

.. contents::


Context
-------

Preboot Execution Environment (PXE) boot is a standardized server-client
environment to boot an OS remotely through network. This allows multiple client
to install/boot OS remotely from a single server. All major distributions such
as Fedora, Ubuntu, Debian, Red Hat supports PXE boot. The virtio network device
available in the RD-E1-Edge platform can be leveraged to do PXE boot of linux
distributions. Ubuntu in particular allows installation through CDROM or PXE
only. To install Ubuntu on RD-E1-Edge Platform, PXE boot should be used.

How to setup TFTP server
------------------------

Before beginning the installation, on the host PC (sever), TFTP, apache2 and
DHCP servers must be setup. The following steps can be used as reference to
setup the PXE server.

- Download the required linux distribution network installer for arm64
  architecture. For example, the Ubuntu network installer for arm64 can be
  downloaded from `here <http://ports.ubuntu.com/ubuntu-ports/dists/bionic-updates/main/installer-arm64/current/images/netboot/netboot.tar.gz>`_.

- Extract the downloaded tar files

        ::

                tar -xvzf netboot.tar.gz

- Install the TFTP server, DHCP server and dependencies

        ::

                sudo apt-get install apache2 tftpd-hpa inetutils-inetd isc-dhcp-server

- Configure the PXE server to point the tftpboot directory

        - Open ``/etc/default/tftpd-hpa`` to edit

                ::

                        sudo vi /etc/default/tftpd-hpa

        - Append the following lines to the end

                ::

                        RUN_DAEMON="yes"
                        OPTIONS="-l -s /var/lib/tftpboot"

        - Open ``/etc/inetd.conf`` file to edit

                ::

                        sudo vi /etc/inetd.conf

        - Append the following line to the end

                ::

                        tftp    dgram   udp    wait    root    /usr/sbin/in.tftpd /usr/sbin/in.tftpd -s /var/lib/tftpboot

- Copy the installer files into the ``/var/lib/tftpboot`` folder

        ::

                sudo cp -fr <ubuntu-installer-path> /var/lib/tftpboot/

- Copy the installer files into the apache2 folder

        ::

                sudo mkdir /var/www/html/ubuntu
                sudo cp -fr <ubuntu-installer-path> /var/www/html/ubuntu/

- Restart the TFTF server

        ::

                sudo systemctl restart tftpd-hpa

- Check the status of the TFTP server to see if it is active

        ::

                sudo systemctl status tftpd-hpa


        - If the status is displayed as ``Stopped``, try the following commands
          to start the TFTP server again

                ::

                        sudo /etc/init.d/inetutils-inetd stop
                        sudo systemctl restart tftpd-hpa
                        sudo systemctl status tftpd-hpa
                        sudo /etc/init.d/inetutils-inetd start
                        sudo systemctl status tftpd-hpa

This completes the setup of the TFTP server.


How to setup DHCP server
------------------------

- Verify whether the DHCP server is stopped

        ::

                sudo systemctl status isc-dhcp-server

        - If the status is shown as ``Running``, the service can be stopped by
          using the following command

                ::

                        sudo systemctl stop isc-dhcp-server

- Follow the instructions on `how to create tap interface`_ to setup the tap
  interface in the host PC.

- Configure the DHCP server to point the grub config file (assuming the PXE
  server and DHCP server are running on the same PC)

        ::

                sudo vi /etc/dhcp/dhcpd.conf

        - Add the following lines at the end

          ::

                ddns-update-style none;
                log-facility local7;

                default-lease-time 600;
                max-lease-time 7200;

                authoritative;
                allow booting;
                allow bootp;

                subnet 192.168.130.0 netmask 255.255.255.0 {
                        option routers                  192.168.130.1;
                        option subnet-mask              255.255.255.0;
                        option broadcast-address        192.168.130.255;
                        option domain-name-servers      10.118.10.61;
                        option ntp-servers              time.nist.gov;
                        option netbios-name-servers     192.168.130.1;
                        option netbios-node-type 2;
                        default-lease-time 86400;
                        max-lease-time 86400;
                        range 192.168.130.100 192.168.130.150;
                        filename "ubuntu-installer/arm64/bootnetaa64.efi";
                   }
                   group {
                           next-server 10.162.0.155;
                           host tftp {
                                   filename "ubuntu-installer/arm64/bootnetaa64.efi";
                                   hardware ethernet 00:02:F7:EF:50:A0; # Check your ethernet mac address
                                   fixed-address 10.162.0.157;
                           }
                   }


- Add the following lines at the end of ``/etc/default/isc-dhcp-server``

        ::

                INTERFACES="br0"
                INTERFACESv4="br0"
                INTERFACESv6=""

- Restart the DHCP server

        ::

                sudo systemctl restart isc-dhcp-server

        - Check the status of the DHCP server

        ::

                sudo systemctl status isc-dhcp-server

This completes the PXE setup on the host PC side. Following this, linux
distribution installation can be done through the network. For example, refer
`how to install Ubuntu on RD-E1-Edge`_ for the complete installation steps.

--------------

*Copyright (c) 2019, Arm Limited. All rights reserved.*

.. _how to create tap interface: create-tap-interface.rst
.. _how to install Ubuntu on RD-E1-Edge: ubuntu-test.rst
