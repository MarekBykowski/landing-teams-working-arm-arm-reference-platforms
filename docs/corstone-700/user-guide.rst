User Guide
==========

.. section-numbering::
    :suffix: .

.. contents::

Notice
------
The Corstone-700 software stack uses the `Yocto project <https://www.yoctoproject.org/>`__ to build
a tiny Linux distribution suitable for the Corstone-700 platform. The yocto project relies on the
`Bitbake <https://www.yoctoproject.org/docs/1.6/bitbake-user-manual/bitbake-user-manual.html>`__
tool as its build tool.

Prerequisites
-------------
These instructions assume your host PC is running Ubuntu Linux 18.04 LTS.
The following instructions expect that you are using a bash shell.

The following prerequisits must be available on the host system:
 * chrpath
 * gawk
 * makeinfo
 * openssl headers
 * diffstat

To resolve these dependencies, run:

::

    sudo apt-get update
    sudo apt-get install chrpath gawk texinfo libssl-dev diffstat


Provided components
-------------------
Within the Yocto project, each component included in the Corstone-700 software stack is specified as
a `bitbake recipe <https://www.yoctoproject.org/docs/1.6/bitbake-user-manual/bitbake-user-manual.html#recipes>`__.
The recipes specific to the Corstone-700 project may be located at:
``<corstone700_workspace>/layers/meta-corstone700``.

Software for Host
#################

Trusted Firmware-A
******************
Based on `ARM Trusted Firmware-A <https://github.com/ARM-software/arm-trusted-firmware>`__

+--------+------------------------------------------------------------------------------------+
| Recipe | <corstone700_workspace>/layers/meta-corstone700/recipes-bsp/trusted-firmware-a     |
+--------+------------------------------------------------------------------------------------+
| Files  | * corstone700.fip                                                                  |
+--------+------------------------------------------------------------------------------------+

Linux
*****
The recipe responsible for building a tiny version of linux.
The layer is based on the `poky-tiny <https://wiki.yoctoproject.org/wiki/Poky-Tiny>`__ distribution
which is a Linux distribution stripped down to a minimal configuration.

The provided distribution is based on busybox and built using muslibc.

+--------+--------------------------------------------------------------------------+
| Recipe | <corstone700_workspace>/layers/meta-corstone700/recipes-kernel           |
+--------+--------------------------------------------------------------------------+
| Files  | * xipImage                                                               |
|        | * iota-tiny-image-corstone700.cpio.gz (rootfs)                           |
+--------+--------------------------------------------------------------------------+


Test App
********
+--------+--------------------------------------------------------------------------+
| Recipe | <corstone700_workspace>/layers/meta-corstone700/recipes-test             |
+--------+--------------------------------------------------------------------------+
| Files  | * test-app (Contained within rootfs)                                     |
+--------+--------------------------------------------------------------------------+


Software for Boot Processor (a.k.a Secure Enclave)
##################################################

The boot firmware has ROM firmware and a RAM firmware which is based on
`ARM CMSIS <https://github.com/ARM-software/CMSIS_5>`__, using RTX as its RTOS.

Internally, the OpenAMP framework has been implemented, using the MHU driver as a mailbox service.

+--------+--------------------------------------------------------------------------+
| Recipe | <corstone700_workspace>/layers/meta-corstone700/recipes-bsp/boot-firmware|
+--------+--------------------------------------------------------------------------+
| Files  | * se_ramfw.bin                                                           |
|        | * se_romfw.bin                                                           |
+--------+--------------------------------------------------------------------------+


Run scripts
###########

Within ``<corstone700_workspace>/run-scripts/`` a number of convenience functions for testing the software
stack may be found.
Usage descriptions for the various scripts are provided in the following sections.


Building the Software stack
---------------------------
Corstone-700 is a Bitbake based Yocto distro which uses bitbake commands to build the stack.
In the top directory of the synced workspace (~/corstone700), run:

::

    export DISTRO="iota-tiny"
    export MACHINE="corstone700"
    source setup-environment

By sourcing setup-enviroment, your current directory should now have switched to
``<corstone700_workspace>/build-iota-tiny/``. If not, change the current directory to this path.
Next, to build the stack, execute:

::

    bitbake iota-tiny-image

The initial clean build will be lengthy, given that all host utilities are to be built as well as
the target images.
This includes host executables (python, cmake, etc.) and the required toolchain(s).

Once the build is successful, all images will be placed in the
``<corstone700_workspace>/build-iota-tiny/tmp-iota_tiny/deploy/images/corstone700`` folder.

Everything apart from the ROM firmware is bundled into a single binary, the
``iota-tiny-image-corstone700.wic`` file.

Running the software
--------------------
An FVP (Fixed Virtual Platform) of the Corstone-700 platform must be available to execute the
included run scripts.

The run-scripts structure is as below:
::

    run-scripts
    |── run_model.sh
    └── scripts
        └── ...

Ensure that the FVP has its dependencies met by executing the FVP: ``./<Corstone-700 Model Binary>``.

All dependencies are met if the FVP launches without any errors, presenting a graphical interface
showing information about the current state of the FVP.

The ``run_model.sh`` script in "<corstone700_workspace>/run-scripts" folder will provide the previously built images as arguments to the FVP, and
launch the FVP. Execute the ``run_model.sh`` script:

::

       ./run_model.sh
       usage: run_model.sh ${FVP executable path} [ -u ]
       -u: Run unit test selector
       No additional argument: load and execute model

When the script is executed, three terminal instances will be launched, one for the boot processor
processing element and two for the Host processing element.
Once the FVP is executing, the Boot Processor will start to boot, wherein the relevant memory
contents of the .wic file are copied to their respective memory locations within the model,
enforce firewall policies on memories and peripherals and then, bring the host out of reset.

The host will boot trusted-firmware-a and then linux, and present a login prompt;
login using the username ``root``.

To explore some of the features of the platform, the ``test-app`` may be executed. This has been
placed in the ``/usr/bin/`` directory.
The test application may be run with an integer argument, specifying which test to execute.
::

    cd /usr/bin
    ./test-app [ 1 | 2 | 3 | 4 ]

The test apps are as follows:
 1. **External System reset test**
        a. User-space application on the host system opens an endpoint corresponding to the
           External System.
        b. External System is then reset.
 2. **External System MHU test**
        a. User-space application on the host system opens an RPMsg endpoint corresponding to the
           MHU channel between the External System and Host and between External System and BP.
        b. A combined message and command is written to the file descriptor associated with the
           endpoint. This command indicates that the External System should print the received message,
           increment the message value by 1 and transmit the message to the Host.
        c. Once the message is received and returned to the host, the Host userspace application
           will read from the endpoint file descriptor, and print the read value.
        d. A combined message and command is written to the file descriptor associated with the
           endpoint. This command indicates that the External System to increment the message value
           by 1 and transmit the message to the BP.
 3. **Boot Processor MHU test**
        a. User-space application on the host system opens an RPMsg endpoint corresponding to the
           MHU channel between the Host and BP.
        b. A combined message and command is written to the file descriptor associated with the
           endpoint. This command indicates that the BP should print the received message,
           increment the message value by 1 and transmit the message to the host.
        c. Once the message is received and returned to the Host, the Host userspace application
           will read from the endpoint file descriptor, and print the read value.
 4. **Host Timer & Interrupt Router and Collator test**
        a. User-space application on the host system opens an RPMsg endpoint corresponding to the
           MHU channel between the Host and BP.
        b. A command is written to the file descriptor associated with the endpoint.
           This command indicates that the BP should start a specified timer. The timer interrupt
           has been specified to be routed to the BP during BP firmware boot.
        c. Once the timer timeouts, an interrupt handler is executed, printing to the BP console
           indicating that the timer interrupt was handled.

Automated unit tests
--------------------
To run the included automated unit test suite, PyCADI must be available and sourced into the current
environment.

The PyCADI library is available within the Arm FastModelPortfolio package.
This package is shipped with most FVPs. If this has not been shipped and installed with the
Corstone-700 FVP, it may be retreived as follows:

Download the Fast Models evaluation package:
https://developer.arm.com/tools-and-software/simulation-models/fast-models

Unzip the downloaded file and execute the ``setup.sh`` script contained within.
Once prompted for which Fast Model packages to install, tick the "Fast Model Portfolio" package.
Note the installation directory. We will refer the installation directory as being
``~/ARM/FastModelsPortfolio_<version>``.

To make the PyCADI library available to python, the following file must be sourced into your
current environment:
::

    source ~/ARM/FastModelsPortfolio_<version>/etc/setup.sh

For convenience, the above command may be added to your ``.bashrc`` file.
The Arm PyCADI library requires Python 2.7.

With the PyCADI library made available in the current environment, the ``run_model.sh``
script may now be executed with the ``-u`` argument, short for unit tests.
Running the automated unit tests are done through a command line interface. This interface
has the ``console-menu`` python package as a prerequisite, which may be met by the following
command:

::

    pip install console-menu

Next, execute:

::

    <corstone700_workspace>/run-scripts/run_model.sh -u

This will prompt a command line menu. Select platform "corstone700".
This will now present the unit tests available in the system. These unit tests are the same as those
presented earlier in the ``test-app``. Executing a unit test will automatically log-in, navigate to
and execute the test-app, and verify correct execution by snooping the consoles presented by the
various processing elements.

Before a unit test is executed, a prompt regarding executing in "usermode" is shown.
In usermode, the unit test framework will spawn xterm instances which will mirror the contents
of the UARTs in the FVP, similar to the xterm instances spawned when the FVP is normally executed.
These xterm sessions are *read only* and solely ment for monitoring the progress of the unit test.
