#!/usr/bin/env python
# -*- coding: utf-8 -*-
u"""Main file used to run the application.
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