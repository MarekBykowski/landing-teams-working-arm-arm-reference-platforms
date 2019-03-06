How to prepare a fedora disk image for RAS and KVM test
=======================================================


.. section-numbering::
    :suffix: .

.. contents::


Why to prepare the fedora disk image?
-------------------------------------

Some of the feature validation on the SGI-575 platform requires a fedora
enterprise linux as the root filesystem. In this release, RAS and KVM feature
validation are the ones that require fedora enterprise linux as the root file
system.

To simplify the validation of RAS and KVM features, it is recommended that the
disk with a installed version of the fedora enterprise linux is created. This
disk will be used as the root filesystem for the validation of RAS and KVM
features.


Preparing the fedora disk image
-------------------------------

- Install a Fedora 27 Enterprise Linux distribution disk image. Refer to the
  `procedure for installing Fedora`_ for detailed instructions on this.

- Create the directory ``prebuilts/refinfra`` (if that does not exist) at the
  root of the workspace.

- Copy the installed fedora disk image at ``prebuilts/refinfra/fedora.satadisk``

- Use the following command to update the grub menu, download/unpack/load the
  lvkm executable to the /root/ directory of the fedora disk.
  Note: sudo permission is required for completing this step.

  ::

   sudo ./build-scripts/sgi/prepare-fedora-disk.sh

This completes the procedure to prepare the fedora disk image.

--------------

*Copyright (c) 2019, Arm Limited. All rights reserved.*

.. _procedure for installing Fedora: fedora-test.rst
