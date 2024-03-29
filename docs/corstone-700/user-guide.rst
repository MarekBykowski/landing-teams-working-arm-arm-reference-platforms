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

The following prerequisites must be available on the host system:
 * chrpath
 * gawk
 * makeinfo
 * openssl headers
 * diffstat
 * compression library
 * yocto
 * pip

To resolve these dependencies, run:

::

    sudo apt-get update
    sudo apt-get install chrpath gawk texinfo libssl-dev diffstat wget git-core unzip gcc-multilib \
     build-essential socat cpio python python3 python3-pip python3-pexpect xz-utils debianutils \
     iputils-ping python3-git python3-jinja2 libegl1-mesa libsdl1.2-dev pylint3 xterm git-lfs openssl \
     curl libncurses-dev libz-dev python-pip


Provided components
-------------------
Within the Yocto project, each component included in the Corstone-700 software stack is specified as
a `bitbake recipe <https://www.yoctoproject.org/docs/1.6/bitbake-user-manual/bitbake-user-manual.html#recipes>`__.
The recipes specific to the Corstone-700 BSP is located at:
``<corstone700_workspace>/meta-arm/meta-arm-bsp/``.
The Yocto machine conf files for the Corstone-700 is:
``<corstone700_workspace>/meta-arm/meta-arm-bsp/conf/machine/include/corstone700.inc``.


Software for Host
#################

Trusted Firmware-A
******************
Based on `ARM Trusted Firmware-A <https://github.com/ARM-software/arm-trusted-firmware>`__

+--------+--------------------------------------------------------------------------------------------------+
| Recipe | <corstone700_workspace>/layers/meta-arm/meta-arm-bsp/recipes-bsp/trusted-firmware-a              |
+--------+--------------------------------------------------------------------------------------------------+
| Files  | * fip.bin                                                                                        |
+--------+--------------------------------------------------------------------------------------------------+

Linux
*****
The recipe responsible for building a tiny version of linux.
The layer is based on the `poky-tiny <https://wiki.yoctoproject.org/wiki/Poky-Tiny>`__ distribution
which is a Linux distribution stripped down to a minimal configuration.

The provided distribution is based on busybox and built using muslibc.

+--------+-------------------------------------------------------------------------------+
| Recipe | <corstone700_workspace>/layers/meta-arm/meta-arm-bsp/recipes-kernel/linux/    |
+--------+-------------------------------------------------------------------------------+
| Files  | * xipImage                                                                    |
|        | * arm-reference-image-corstone700-[fvp/mps3].cramfs-xip (xip rootfs)          |
+--------+-------------------------------------------------------------------------------+


Test App
********
+--------+--------------------------------------------------------------------------------------------+
| Recipe | <corstone700_workspace>/layers/meta-arm/meta-arm-bsp/recipes-test/corstone700-test-app/    |
+--------+--------------------------------------------------------------------------------------------+
| Files  | * test-app (Contained within rootfs)                                                       |
+--------+--------------------------------------------------------------------------------------------+


Software for Boot Processor (a.k.a Secure Enclave)
##################################################

The boot firmware has ROM firmware and a RAM firmware which is based on
`ARM CMSIS <https://github.com/ARM-software/CMSIS_5>`__, using RTX as its RTOS.

Internally, the OpenAMP framework has been implemented, using the MHU driver as a mailbox service.

+--------+-----------------------------------------------------------------------------------------------------+
| Recipe | <corstone700_workspace>/layers/meta-arm/meta-arm-bsp/recipes-bsp/boot-firmware/                     |
+--------+-----------------------------------------------------------------------------------------------------+
| Files  | * se_ramfw.bin                                                                                      |
|        | * se_romfw.bin                                                                                      |
+--------+-----------------------------------------------------------------------------------------------------+

Software for External System
############################

+--------+---------------------------------------------------------------------------------------------------------+
| Recipe | <corstone700_workspace>/layers/meta-arm/meta-arm-bsp/recipes-bsp/external-system                        |
+--------+---------------------------------------------------------------------------------------------------------+
| Files  | * es_flashfw.bin                                                                                        |
+--------+---------------------------------------------------------------------------------------------------------+

Run scripts
###########

Within ``<corstone700_workspace>/run-scripts/iot/`` several convenience functions for testing the software
stack may be found.
Usage descriptions for the various scripts are provided in the following sections.


Building the Software stack
---------------------------
Corstone-700 is a Bitbake based Yocto distro which uses bitbake commands to build the stack.
In the top directory of the synced workspace (~/corstone700), run:

::

    source setup-environment
    --> select corstone700-fvp or corstone700-mps3 machine based on the environment.
    --> select poky-tiny

By sourcing setup-environment, your current directory should now have switched to
``<corstone700_workspace>/build-poky-tiny/``. If not, change the current directory to this path.
Next, to build the stack, execute:

::

    bitbake arm-reference-image

The initial clean build will be lengthy, given that all host utilities are to be built as well as
the target images.
This includes host executables (python, cmake, etc.) and the required toolchain(s).

Once the build is successful, all images will be placed in the
``<corstone700_workspace>/build-poky-tiny/tmp-poky_tiny/deploy/images/corstone700-*/`` folder.

Everything apart from the ROM firmware is bundled into a single binary, the
``arm-reference-image-corstone700-*.wic.nopt`` file.

Running the software on FVP
---------------------------
An FVP (Fixed Virtual Platform) of the Corstone-700 platform must be available to execute the
included run scripts.

The run-scripts structure is as below:
::

    run-scripts
    |── iot
        |── run_model.sh
        └── scripts
            └── ...

Ensure that the FVP has its dependencies met by executing the FVP: ``./<Corstone-700 Model Binary>``.

All dependencies are met if the FVP launches without any errors, presenting a graphical interface
showing information about the current state of the FVP.

The ``run_model.sh`` script in "<corstone700_workspace>/run-scripts/iot/" folder will provide the
previously built images as arguments to the FVP, and launch the FVP.
Execute the ``run_model.sh`` script:

::

       ./run_model.sh
       usage: run_model.sh ${FVP executable path/<Corstone-700 Model Binary>} [ -u ]
       -u: Run unit test selector
       No additional argument: load and execute model

When the script is executed, three terminal instances will be launched, one for the boot processor
processing element and two for the Host processing element.
Once the FVP is executing, the Boot Processor will start to boot, wherein the relevant memory
contents of the .wic file are copied to their respective memory locations within the model,
enforce firewall policies on memories and peripherals and then, bring the host out of reset.

The host will boot trusted-firmware-a and then linux, and present a login prompt;
login using the username ``root``.

Automated unit tests
--------------------
To run the included automated unit test suite, PyIRIS must be available and sourced into the current
environment.

The PyIRIS library is available within the Arm Fast Models evaluation package.
This package is shipped with most FVPs. If this has not been shipped and installed with the
Corstone-700 FVP, it may be retrieved as follows:

Download the Fast Models evaluation package:
https://developer.arm.com/tools-and-software/simulation-models/fast-models

Unzip the downloaded file and execute the ``setup.sh`` script contained within.
Once prompted for which Fast Model packages to install, select all available packages.
Note the installation directory. We will refer the installation directory as being
``~/ARM/FastModelsxxx_<version>``.

To make the PyIRIS library available to python, the following file must be sourced into your
current environment:
::

    source ~/ARM/FastModelsTools_<version>/source_all.sh

For convenience, the above command may be added to your ``.bashrc`` file.
The Arm PyIRIS library requires Python 2.7.

With the PyIRIS library made available in the current environment, the ``run_model.sh``
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
of the UARTs in the FVP, like the xterm instances spawned when the FVP is normally executed.
These xterm sessions are *read only* and solely meant for monitoring the progress of the unit test.

Running the software on FPGA
----------------------------

Download the FPGA bundle and extract it. The directory structure of the FPGA bundle is shown below.
::

    ├── config.txt
    ├── LOG.TXT
    ├── MB
    │   ├── BRD_LOG.TXT
    │   └── HBI0309A
    │   └── HBI0309B
    │   └── HBI0309C
    │       ├── AN543
    │       │   ├── AN543_v1.bit
    │       │   ├── an543_v1.txt
    │       │   └── images.txt
    │       ├── board.txt
    │       └── mbb_v138.ebf
    └── SOFTWARE
        └── Selftest.axf

Depending upon the MPS3 board version (printed on the MPS3 board) you should update the images.txt file
(in corresponding HBI0309x folder) so that the file points to the images under SOFTWARE directory.
Here is an example
::

    [IMAGES]
    TOTALIMAGES: 3                      ;Number of Images (Max: 32)

    IMAGE0ADDRESS: 0x00000000           ;Please select the required executable program
    IMAGE0UPDATE: RAM                   ;Image Update:NONE/AUTO/FORCE/RAM/AUTOQSPI/FORCEQSPI
    IMAGE0FILE: \SOFTWARE\se_romfw.bin  ; - selftest uSD

    IMAGE1ADDRESS: 0x02000000           ;Please select the required executable program - Target > 0x0800_0000
    IMAGE1UPDATE: AUTOQSPI              ;Image Update:NONE/AUTO/FORCE/RAM/AUTOQSPI/FORCEQSPI
    IMAGE1FILE: \SOFTWARE\cs700.wic     ; - selftest uSD

    IMAGE2ADDRESS: 0x08000000           ;Please select the required executable program
    IMAGE2UPDATE: RAM                   ;Image Update:NONE/AUTO/FORCE/RAM/AUTOQSPI/FORCEQSPI
    IMAGE2FILE: \SOFTWARE\es_fw.bin     ; - selftest uSD

OUTPUT_DIR=``<corstone700_workspace>/build-poky-tiny/tmp-poky_tiny/deploy/images/corstone700-[fvp/mps3]/``

1. Copy se_romfw.bin from OUTPUT_DIR directory to SOFTWARE directory of the FPGA bundle
2. Copy arm-reference-image-corstone700-mps3.wic.nopt from OUTPUT_DIR directory
   to SOFTWARE directory of the FPGA bundle and rename the wic image to cs700.wic
3. Copy es_flashfw.bin from OUTPUT_DIR directory to SOFTWARE directory of the FPGA bundle and
   rename es_flashfw.bin to es_fw.bin

**NOTE:** Renaming of the images are required because MCC firmware has limitation of 8 characters before .(dot)
and 3 characters after (.)dot.

Now, copy the entire folder to board's SDCard and reboot the board.

On the host machine open 4 minicom sessions. In case of Linux machine it will be ttyUSB0, ttyUSB1, ttyUSB2, ttyUSB3
and it might be different on Window machine.
::

    ttyUSB0 for MCC
    ttyUSB1 for Boot Processor(Cortex-M0+)
    ttyUSB2 for Host(Cortex-A32)
    ttyUSB3 for ExternalSystem(Cortex-M3)

Once the system is booted complete, you should see console logs on the minicom sessions.
ExternalSystem is not booted by default.
Once the HOST(Cortex-A32) is booted completely, login to the shell using **"root"** login.

Running test application (applicable to both FVP and FPGA)
----------------------------------------------------------
To explore some of the features of the platform, the ``test-app`` may be executed. This has been
placed in the ``/usr/bin/`` directory.
The test application may be run with an integer argument, specifying which test to execute.
::

    test-app [ 1 | 2 | 3 | 4 ]

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
           will read from the endpoint file descriptor and print the read value.
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
           will read from the endpoint file descriptor and print the read value.
 4. **Host Timer & Interrupt Router and Collator test**
        a. User-space application on the host system opens an RPMsg endpoint corresponding to the
           MHU channel between the Host and BP.
        b. A command is written to the file descriptor associated with the endpoint.
           This command indicates that the BP should start a specified timer. The timer interrupt
           has been specified to be routed to the BP during BP firmware boot.
        c. Once the timer timeouts, an interrupt handler is executed, printing to the BP console
           indicating that the timer interrupt was handled.

--------------

*Copyright (c) 2019-2020, Arm Limited. All rights reserved.*
