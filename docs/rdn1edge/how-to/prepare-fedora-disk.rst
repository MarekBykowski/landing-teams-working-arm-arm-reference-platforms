How to prepare a fedora disk image for RAS and KVM test
=======================================================


.. section-numbering::
    :suffix: .

.. contents::


Why to prepare the fedora disk image
------------------------------------

The RAS and KVM tests on the RD-N1-Edge platform requires a Fedora enterprise
linux as the root filesystem. The build and run scripts for these tests
require a pre-installed disk image of Fedora 27 to be present in the
prebuilts/refinfra directory. This pre-installed disk image can then be
preloaded with all the tools required to validate the KVM and RAS tests.

Preparing the fedora disk image
-------------------------------

- Install a Fedora 27 Enterprise Linux distribution disk image. Refer to
  [refer] for detailed instructions on this.

- Create the directory ``prebuilts/refinfra`` (if that does not exist) at the
  root of the workspace.

- Copy the installed fedora disk image at ``prebuilts/refinfra/fedora.satadisk``

- Use the following command to update the grub menu, download/unpack/load the
  lvkm executable to the /root/ directory of the fedora disk.
  Note: sudo permission is required for completing this step.

  ::

   sudo ./build-scripts/rdinfra/prepare-fedora-disk.sh

This completes the procedure to prepare the fedora disk image.

--------------

*Copyright (c) 2019, Arm Limited. All rights reserved.*
