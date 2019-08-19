User guide
==========


.. section-numbering::
    :suffix: .

.. contents::


Notice
------

In the current release, software stacks for some platforms are manually synced
instead of using ``sync_workspace.py``:

- System Guidance for Infrastructure (SGI): `SGI-575 <sgi575/user-guide.rst>`__

- Neoverse(TM) Reference Design (RD): `RD-N1-Edge <rdn1edge/user-guide.rst>`__,
  `RD-E1-Edge <rde1edge/user-guide.rst>`__, `RD-Daniel <rddaniel/user-guide.rst>`__

Please use the links above to sync a software stack for one of these platforms.

Prerequisites
-------------

These instructions assume your host PC is running Ubuntu Linux 16.04.1 LTS.
Windows users may also follow these instructions but will only be able to use
prebuilt configurations.

If building from source:

-  The ``sync_workspace.py`` script will automatically detect and list any
   missing prerequisite packages, which you will need to manually install
   before proceeding.

-  You will also need to configure ``git``, otherwise the ``sync_workspace.py``
   script will hang at the ``Initialising repo...`` stage.

::

  $ git config --global user.name "John Doe"
  $ git config --global user.email "john.doe@example.com"
  $ git config --global color.diff auto

Initialising your workspace
---------------------------

Simply run the ``sync_workspace.py`` script using Python 3, then follow the
on-screen menus to select your platform and software stack configuration::

  $ git clone https://git.linaro.org/landing-teams/working/arm/arm-reference-platforms.git
  $ cd arm-reference-platforms/
  $ python3 sync_workspace.py

Building from source
--------------------

How you proceed will depend on your platform and chosen software stack.

The following platforms support different build systems

* Corstone-700 : `Corstone-700 User guide <corstone-700/user-guide.rst>`__
* Cortex A5 DesignStart : `Cortex A5 DesignStart User guide <ca5ds/user-guide.rst>`__

For Other platforms:

To clean, build, and package the software in a build from source workspace::

  $ ./build-scripts/build-all.sh all

You can also individually perform each of these steps::

  $ ./build-scripts/build-all.sh clean
  $ ./build-scripts/build-all.sh build
  $ ./build-scripts/build-all.sh package

You can invoke a particular software component's build script in the same way in
order to build just that component rather than the whole software stack, for
example ``./build-scripts/build-linux.sh`` targets just the Linux kernel.

Running the software
--------------------

How you proceed will depend on your platform and chosen software stack.

The following platform user guides are maintained in this git repository:

- `Neoverse(TM) N1 SDP <n1sdp/run-on-n1sdp.rst>`__
- `Corstone-700 <corstone-700/user-guide.rst>`__
- `Cortex A5 DesignStart User guide <ca5ds/user-guide.rst>`__

The following platform user guides are currently still maintained on our
`Arm Community wiki <https://community.arm.com/developer/tools-software/oss-platforms/w/docs>`__:

- `Juno <https://community.arm.com/developer/tools-software/oss-platforms/w/docs/391/run-the-arm-platforms-deliverables-on-juno>`__

- `TC2 <https://community.arm.com/developer/tools-software/oss-platforms/w/docs/408/run-the-arm-platforms-deliverables-on-tc2>`__

- `Armv8-A Base Platform <https://community.arm.com/developer/tools-software/oss-platforms/w/docs/392/run-the-arm-platforms-deliverables-on-an-fvp>`__

- `Armv8-A Foundation Model <https://community.arm.com/developer/tools-software/oss-platforms/w/docs/392/run-the-arm-platforms-deliverables-on-an-fvp>`__

- System Guidance for Mobile (SGM): `SGM-775 <https://community.arm.com/developer/tools-software/oss-platforms/w/docs/392/run-the-arm-platforms-deliverables-on-an-fvp>`__

Note: If you wish to run Android on SGM-775, see `here <https://community.arm.com/developer/tools-software/oss-platforms/w/docs/428/run-android-on-sgm-775>`__
instead.
