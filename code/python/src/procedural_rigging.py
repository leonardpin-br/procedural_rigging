#! mayapy.exe
# -*- coding: utf-8 -*-
u"""Main file used to run the application.

Important:
    The Shebang Line does have an effect inside this main file, **if it is
    executed directly** (outside of Maya).

    The ``.py`` files should have its properties altered system wide. The
    default program to execute them should be::

        C:\\Windows\\pyw.exe

Warning:
    The Shebang Line appears to have no practical effect, at least on Windows,
    in the ``<project_root>/resources/documentation_config/build_sphinx_mayadoc.py``
    file even with the ``.py`` files associated with the launcher
    (``C:\\Windows\\pyw.exe``).

    To make that script a little bit more portable, the shebang line is:

        #! /usr/bin/env mayapy


    The use of the **mayapy** command, inside the ``make.bat`` file, makes all
    the difference in the execution of the documentation generation.

References:
    `3.7 Shebang Line`_

    `unable to run 'aws' from cygwin`_

    `Shebang Notation: Python Scripts on Windows and Linux?`_

    `4.8.2. Shebang Lines`_

    `Should I put #! (shebang) in Python scripts, and what form should it take?`_

.. _3.7 Shebang Line:
   https://google.github.io/styleguide/pyguide.html#37-shebang-line
.. _unable to run \'aws\' from cygwin:
   https://stackoverflow.com/a/62093489/3768670
.. _Shebang Notation\: Python Scripts on Windows and Linux?:
   https://stackoverflow.com/a/7574585/3768670
.. _4.8.2. Shebang Lines:
   https://docs.python.org/3/using/windows.html#shebang-lines
.. _Should I put #! (shebang) in Python scripts, and what form should it take?:
   https://stackoverflow.com/a/14599026/3768670
"""

import sys

import komodoRig
import rigLib

characterName = "komodo"
komodoRig.komodo.build(characterName)
print("komodoRig.komodo.build() function executed successfully!")

rigLib.base.control.Control(shape="sphere")

print("\n\n===========================================================\n")
print("Course finished!!!")
print("\n===========================================================\n\n")
