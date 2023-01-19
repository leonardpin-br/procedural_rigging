#!/usr/bin/env python
# -*- coding: utf-8 -*-
u"""main project file with central variables

References:
    `Get directory of current Python script`_

.. _Get directory of current Python script:
   https://www.geeksforgeeks.org/get-directory-of-current-python-script/

"""

import os

# Gets the full path of this script file dinamically.
THIS_FILE_PATH = os.path.realpath(os.path.dirname(__file__)).replace("\\", "/")

# Gets the full path of the project's root folder:
pathList = THIS_FILE_PATH.split("/")
pathList = pathList[:-4]
project_root = "/".join(pathList)


sceneScale = 1.0
u"""float: The default scene scale."""

mainProjectPath = os.path.join(project_root, "assets").replace("\\", "/")
u"""str: The full path to the `assets` folder."""
