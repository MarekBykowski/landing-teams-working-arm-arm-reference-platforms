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

Get Linux version 4.18 or above (5.4.0 used in this example).

Two Linux images are required

- Monolithic Linux image: Used during first boot
- Linux debian package: Installed by Ubuntu in first boot and used after second boot onwards.

**Building monolithic linux image**
 Apply n1sdp-pcie-quirk patches available inside <workspace/n1sdp-pcie-quirk/linux/>.
 Also available here https://git.linaro.org/landing-teams/working/arm/n1sdp-pcie-quirk.git/tree/linux/

    ::
         $ export ARCH=arm64
         $ export CROSS_COMPILE=/usr/bin/aarch64-linux-gnu-
         $ make defconfig
         $ make Image

Generated Image name : Image

**Building linux deb package**

Along with the N1SDP Quirk patches get the following 5 patches from https://kernel.ubuntu.com/~kernel-ppa/mainline provided by Ubuntu and required to build linux debian package.Patches version should match with linux kernel version e.g. for 5.4 use patches under https://kernel.ubuntu.com/~kernel-ppa/mainline/v5.4/

Ubuntu Patches:
        - 0001-base-packaging.patch
        - 0002-UBUNTU-SAUCE-add-vmlinux.strip-to-BOOT_TARGETS1-on-p.patch
        - 0003-UBUNTU-SAUCE-tools-hv-lsvmbus-add-manual-page.patch
        - 0004-debian-changelog.patch
        - 0005-configs-based-on-Ubuntu-5.4.0-7.8.patch

Build Commands:
     ::

         $ export ARCH=arm64
         $ export CROSS_COMPILE=/usr/bin/aarch64-linux-gnu-
         $ cat debian.master/config/config.common.ubuntu debian.master/config/arm64/config.common.arm64 > $UBUNTU_OUT_DIR/.config
         $ make oldconfig
         $ sed -ie 's/CONFIG_DEBUG_INFO=y/# CONFIG_DEBUG_INFO is not set/' .config
         $ make bindeb-pkg

Generated Image name: linux-image-5.4.0+_5.4.0+-1_arm64.deb rename it to "linux-image-n1sdp.deb"

Creating Ubuntu Root FS
-----------------------------

Download the Ubuntu minimal root file system image from
"http://cdimage.ubuntu.com/ubuntu-base/bionic/daily/current/bionic-base-arm64.tar.gz".
This image will be extracted and modified to boot a fully fledged Ubuntu 18.04
distro.

An initramfs is provided containing the necessary firmware and hardware support.
The initramfs PID 1 should configure the network interface and then
execute the installation script.

During the first boot an installation script will configure a minimal working
base-system.

The provided installation script preforms the following tasks:

- Set root as password for root
- Add 8.8.4.4 and 8.8.8.8 as nameservers
- Resize the second partion (and file-system) to end of disk
- Install a minimal set of package with apt-get


Content of the provided installation script (assumes that network is up):
    ::

        #!/bin/sh

        on_exit() {
            test $? -ne 0 || exit 0
            echo "something unexpected happend, bailing to a recovery shell!" >&2
            exec /bin/bash
        }

        trap "on_exit" EXIT TERM

        set -u
        set -e

        mount -t proc proc /proc
        mount -t sysfs sysfs /sys
        mount -o remount,rw /
        chown -Rf root:root / || true
        chmod 777 /tmp
        PATH=/usr/local/sbin:/usr/sbin:/sbin:/usr/local/bin:/usr/bin:/bin
        export PATH
        apt-get update
        apt-get install -y \
        	apt-utils \
        	grub-efi-arm64 \
        	ifupdown \
        	initramfs-tools \
        	isc-dhcp-client \
        	kmod \
        	linux-firmware \
        	net-tools \
        	openssh-server \
        	resolvconf \
        	sudo \
        	systemd \
        	udev \
        	vim \

        ln -s /dev/null /etc/systemd/network/99-default.link
        echo "nameserver 8.8.4.4" >> /etc/resolvconf/resolv.conf.d/head
        echo "nameserver 8.8.8.8" >> /etc/resolvconf/resolv.conf.d/head
        service resolvconf restart
        echo "LABEL=Ubuntu-18.04 /  ext4 defaults 0 0" >> etc/fstab
        echo "LABEL=ESP /boot/efi vfat defaults 0 0" >> etc/fstab
        mkdir /boot/efi
        mount /boot/efi
        grub-install || true
        [ -e /linux-image-n1sdp.deb ] && dpkg -i /linux-image-n1sdp.deb
        [ -e /linux-headers-n1sdp.deb ] && dpkg -i /linux-headers-n1sdp.deb
        sed -ie 's/^GRUB_TIMEOUT_STYLE=.*$/GRUB_TIMEOUT_STYLE=menu/; s/^GRUB_TIMEOUT=.*$/GRUB_TIMEOUT=2/; s/GRUB_CMDLINE_LINUX_DEFAULT=.*$/GRUB_CMDLINE_LINUX_DEFAULT="earlycon vfio-pci.ids=10ee:9038"/' /etc/default/grub
        update-grub
        sync
        # change root password
        echo "root:root" | chpasswd
        # Create user ubuntu:ubuntu
        adduser ubuntu --gecos "ubuntu" --disabled-password
        echo "ubuntu:ubuntu" | chpasswd
        usermod -aG sudo ubuntu
        cat <<EOF >/etc/modprobe.d/vfio.conf
        # cat /etc/modprobe.d/vfio.conf
        options vfio-pci ids=10ee:9038
        softdep radeon pre: vfio-pci
        softdep amdgpu pre: vfio-pci
        softdep nouveau pre: vfio-pci
        softdep drm pre: vfio-pci
        options kvm_amd avic=1
        EOF
        update-initramfs -u
        cat <<EOF >/etc/modules-load.d/vfio-pci.conf
        # cat /etc/modules-load.d/vfio-pci.conf
        vfio-pci
        EOF
        sync

Content of /etc/network/interfaces
     ::

         #!/bin/sh
         # Network setup
         # interfaces(5) file used by ifup(8) and ifdown(8)
         auto eth0
         iface eth0 inet dhcp


Creating Ubuntu disk Image
--------------------------
- Create "grub-ubuntu.img" disk image which will have two partitions, first a
  FAT partition of 20MB and second an EXT4 partiton of 4GB.

- FAT partition labeled as ESP which contains grub configuration for **first** boot.
  ::

      set debug="loader,mm"
      set term="vt100"
      set default="0"
      set timeout="1"

      set root=(hd1,msdos2)

      menuentry 'Install Ubuntu on N1SDP Platform' {
      	linux /Image acpi=force earlycon=pl011,0x2A400000
      	initrd /ramdisk.img
      }

- EXT4 partition labeled as Ubuntu-18.04 which contains extracted Ubuntu-18.04
  root file system created earlier along with both kernel images and initramfs.

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

- The GRUB configuration stored on the ESP partition is used
- The monolithic kernel image and initramfs are used
- /init configures the network and mount the real root
- /init executes the installation script
- The installation script installs the base packages
- The installation script installs the Linux deb package and creates a
  new initramfs and grub entry

**Second Boot**

- Second boot onwards a minimal Ubuntu-18.04 will be booted which already has a grub entry created during first boot.
- It will also use linux debian image and initramfs installed during first boot.

--------------

*Copyright (c) 2020, Arm Limited. All rights reserved.*

