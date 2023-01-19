#!/usr/bin/env python
# -*- coding: utf-8 -*-
u"""main project file with central variables
"""

import os

cwd = os.getcwd()
cwd = cwd.replace("\\", "/")

# Dealing with Sphinx limitation:
if "sphinx" in cwd:
    pathList = cwd.split("/")

    # Removing "docs" and "sphinx" form path:
    pathList = pathList[:-2]

    cwd = "/".join(pathList)

sceneScale = 1.0
mainProjectPath = os.path.join(cwd, "assets").replace("\\", "/")
