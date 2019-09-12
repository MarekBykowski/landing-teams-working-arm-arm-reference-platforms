Prepare a distro image for N1SDP: Ubuntu 18.04 as an example
============================================================


.. section-numbering::
    :suffix: .

.. contents::


Introduction
------------

The Neoverse N1 System Development Platform (N1SDP) is an enterprise class reference board based on the Neoverse N1 core.
This document is a guide on how to prepare a Linux distro image for N1SDP platform taking Ubuntu 18.04 as an example.

All the steps mentioned below are implemented in build-scripts provided with N1SDP Software stack.

Building Linux Images
---------------------

Get Linux version 4.18 or above (5.2.8 used in this example).

Two Linux images are required

- Monolithic Linux image: Used during first boot
- Linux debian package: Installed by Ubuntu in first boot and used after second boot onwards.

**Building monolithic linux image**
 Apply n1sdp-pcie-quirk patches available inside <workspace/n1sdp-pcie-quirk/linux/0001-N1SDP-PCIe-Enablement-Quirks-for-N1SDP-PCie-controll.patch>.
 Or it could be found here https://git.linaro.org/landing-teams/working/arm/n1sdp-pcie-quirk.git/tree/linux/

    ::
         $ export ARCH=arm64
         $ export CROSS_COMPILE=/usr/bin/aarch64-linux-gnu-
         $ make defconfig
         $ make Image

Generated Image name : Image

**Building linux deb package**

Along with N1SDP Quirk patches get following 6 patches from https://kernel.ubuntu.com/~kernel-ppa/mainline provided by Ubuntu and required to build linux debian package.Patches version should match with linux kernel version e.g. for 5.2.8 use patches under https://kernel.ubuntu.com/~kernel-ppa/mainline/v5.2.8/

Ubuntu Patches:
        - 0001-base-packaging.patch
        - 0002-UBUNTU-SAUCE-kbuild-add-fcf-protection-none-when-usi.patch
        - 0003-UBUNTU-SAUCE-add-vmlinux.strip-to-BOOT_TARGETS1-on-p.patch
        - 0004-UBUNTU-SAUCE-tools-hv-lsvmbus-add-manual-page.patch
        - 0005-debian-changelog.patch
        - 0006-configs-based-on-Ubuntu-5.2.0-11.12.patch

Build Commands:
     ::

         $ export ARCH=arm64
         $ export CROSS_COMPILE=/usr/bin/aarch64-linux-gnu-
         $ cat debian.master/config/config.common.ubuntu debian.master/config/arm64/config.common.arm64 > $UBUNTU_OUT_DIR/.config
         $ make oldconfig
         $ sed -ie 's/CONFIG_DEBUG_INFO=y/# CONFIG_DEBUG_INFO is not set/' .config
         $ make bindeb-pkg

Generated Image name: linux-image-5.2.8+_5.2.8+-1_arm64.deb rename it to "linux-image-n1sdp.deb"

Creating Ubuntu Root FS
-----------------------------

Download Ubuntu minimal root file system image from "http://cdimage.ubuntu.com/ubuntu-base/bionic/daily/current/bionic-base-arm64.tar.gz"
This image will be extracted and modified to boot full fledged Ubuntu 18.04 distro.

Do following modifications to extracted Ubuntu minimal root FS
      ::

          Create a init script in /bin/init required for first boot.
          Clear root password(so that we can actually login) from /etc/passwd.
          Add nameserver 8.8.8.8 in /etc/resolv.conf
          Create /etc/network/interfaces with following content

    Content of init script
      ::

         #!/bin/sh
         mount -t proc proc /proc
         mount -t sysfs sysfs /sys
         mount -t sysfs sysfs /sys
         PATH=/usr/local/sbin:/usr/sbin:/sbin:/usr/local/bin:/usr/bin:/bin
         export PATH
         apt-get update
         apt-get install -y isc-dhcp-client systemd udev apt-utils resolvconf grub-efi-arm64 kmod ifupdown net-tools vim initramfs-tools
         ln -s /dev/null /etc/systemd/network/99-default.link
         echo "nameserver 8.8.4.4" >> /etc/resolvconf/resolv.conf.d/head
         echo "nameserver 8.8.8.8" >> /etc/resolvconf/resolv.conf.d/head
         service resolvconf restart
         echo "LABEL=Ubuntu-18.04 /  ext4 defaults 0 0" >> etc/fstab
         echo "LABEL=ESP /boot/efi vfat defaults 0 0" >> etc/fstab
         mkdir /boot/efi
         mount /boot/efi
         grub-install
         [ -e /linux-image-n1sdp.deb ] && dpkg -i /linux-image-n1sdp.deb
         sed -ie 's/^GRUB_TIMEOUT_STYLE=.*$/GRUB_TIMEOUT_STYLE=menu/; s/^GRUB_TIMEOUT=.*$/GRUB_TIMEOUT=2/; s/GRUB_CMDLINE_LINUX_DEFAULT=.*$/GRUB_CMDLINE_LINUX_DEFAULT="earlycon"/' /etc/default/grub
         update-grub
         sync
         bash

    Content of /etc/network/interfaces
      ::

        # Network setup
        # interfaces(5) file used by ifup(8) and ifdown(8)
        auto eth0
        iface eth0 inet dhcp


Creating Ubuntu disk Image
--------------------------
- Create "grub-ubuntu.img" disk image which will have two partitions, first a FAT partition of 20MB and second an EXT3 partiton of 8GB.

- FAT partition labeled as ESP which contains grub configuration for first boot.

    content of grub configuration: used during first boot only
      ::

        # Network setup
        set debug="loader,mm"
        set term="vt100"
        set default="0"
        set timeout="1"

        set root=(hd1,msdos2)

        menuentry 'Booting Ubuntu on N1SDP Platform' {
        linux /Image acpi=force ip=dhcp console=ttyAMA0,115200 root=/dev/sda2 rootwait systemd.journald.forward_to_console=no
        initrd /ramdisk.img
        }

- EXT3 partition labeled as Ubuntu-18.04 which contains extracted Ubuntu-18.04 root file system created earlier along with both kernel images and initrd.

Mounting of disk Image on memory stick
--------------------------------------
      ::

        $ lsblk
        $ sudo dd if=grub-ubuntu.img of=/dev/sd<X> bs=1M
        $ sync

Note: Replace ``/dev/sdX`` with the handle corresponding to your USB stick as identified by the ``lsblk``

Booting Sequence
----------------
**First Boot**

- grub configuration kept inside ESP partition will be used.
- Monolithic kernel image and initrd will be used.
- /bin/init will be used which will install linux deb package create a new initramfs and grub entry.

**Second Boot**

- Second boot onwards Full fledged Ubuntu-18.04 will be booted which already has a grub entry created during first boot.
- It will also use linux debian image and initramfs installed during first boot.

--------------

*Copyright (c) 2019, Arm Limited. All rights reserved.*

