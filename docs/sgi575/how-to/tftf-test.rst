How to build SGI-575 platform software to execute TF-A Tests
============================================================


.. section-numbering::
    :suffix: .

.. contents::

What are TF-A Tests
-------------------

The Trusted Firmware-A Tests (TF-A Tests) is a suite of bare metal tests to
exercise the Trusted Firmware-A (TF-A) features from the normal world.
It enables strong TF-A functional testing without dependency on a rich OS.
It mainly interacts with TF-A through its SMC interface. It provides a basis
for TF-A developers to validate their own platform ports and add their own
test cases.

TF-A Tests on SGI-575 platform
------------------------------

TF-A firmware on SGI-575 platform has a significant importance in supporting
multiple features on the SGI-575 platform. For instance, secure partition
manager component of TF-A is used in RAS and PSCI component is used for managing
idle states on the platform. There are many more important uses of TF-A in the
SGI-575 platform software stack. So it becomes imperative that the SGI-575
platform implementation in TF-A is well tested. TF-A Tests on SGI-575 platform
helps to serve this purpose.

Tests to Skip
-------------

The TF-A Test suite supports quite a lot of tests covering various aspects of
the TF-A platform implementation. It is possible to selectively disable the
tests that are not supported by listing those tests in the platform specific
``tests_to_skip.txt`` file.

System suspend/resume related tests are not supported for SGI-575 platform
as there are no wakeup sources in SGI-575 FVP platforms. So such tests and tests
that fail are currently listed in the ``tests_to_skip.txt`` file and listed
below as well.

- PSCI STAT/Stats test cases after system suspend
- PSCI System Suspend Validation
- PSCI SYSTEM SUSPEND stress tests

Procedure to build TF-A Tests for SGI-575 platform
--------------------------------------------------

The procedure to build the TF-A Test cases along with the SGI-575 platform
software stack is listed below. The components of the SGI-575 platform software
stack that are built is limited to those that provide the ability to execute
the TF-A Tests as a BL33 stage binary (i.e, SCP and TF-A).

To build the SGI software stack and TF-A Tests, the command to be used is

   ::

        ./build-scripts/build-test-tftf.sh -p sgi575 <command>

Supported command line options are listed below

   -  <command>

      -  Supported commands are

         -  clean
         -  build
         -  package
         -  all (all the three above)


Examples of the build command are

   -   ::

        ./build-scripts/build-test-tftf.sh -p sgi575 all

      - This command cleans, builds the required components of the SGI-575
        platform software stack (SCP, TF-A) and TF-A Tests. It then prepares
        the FIP image that can be used for executing the tests.

   -   ::

        ./build-scripts/build-test-tftf.sh -p sgi575 build

      - This command performs an incremental build of the required software
        components in the software stack for the SGI-575 platform and TF-A Tests.
        Note: this command should be followed by the 'package' command to
        complete the preparation of the FIP image.

   -   ::

        ./build-scripts/build-test-tftf.sh -p sgi575 package

      - This command packages the previously built software stack and prepares
        the FIP image.

Procedure to execute TF-A Tests for SGI-575 platform
----------------------------------------------------

After the build for the TF-A Tests is complete to execute the TF-A Tests, the
command to be used is

   ::

        cd model-scripts/sgi
        ./tftf.sh -p sgi575 -a <additional_params>


Supported command line options are listed below

   -  -a <additional_params>

      -  Specify any additional model parameters to be passed. The model
         parameters and the data to be passed to those parameters can be found
         in the FVP documentation.


Example commands to execute the TF-A Tests are as listed below.

   -   ::

        ./tftf.sh -p sgi575

      - This command starts the execution of the TF-A Tests on the SGI-575 model
        and the results are displayed on the console.

   -   ::

        ./tftf.sh -p sgi575 -a "-C board.flash0.diagnostics=1"

      - This command starts the execution of the TF-A Tests on the SGI-575 model
        and the results are displayed on the console. Additional parameters to
        the model are supplied using the -a command line parameter.

--------------

*Copyright (c) 2019, Arm Limited. All rights reserved.*
