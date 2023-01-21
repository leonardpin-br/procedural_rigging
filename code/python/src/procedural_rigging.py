#!/c/Progra~1/Autodesk/Maya2020/bin/mayapy.exe
# -*- coding: utf-8 -*-
u"""Main file used to run the application.

References:
    `3.7 Shebang Line`_

.. _3.7 Shebang Line:
   https://google.github.io/styleguide/pyguide.html#37-shebang-line
"""

import sys

import komodoRig

characterName = "komodo"
komodoRig.komodo.build(characterName)

print("\n\n===========================================================\n")
print("Python executable full path:")
print(sys.executable)
print("komodoRig.komodo.build() function executed successfully!")
print("\n===========================================================\n\n")