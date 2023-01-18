# -*- coding: utf-8 -*-
u"""Maya shelf button for this app to run.

This is a (Maya) shelf button example to make this code run without conflict
with the Sphinx's sphinx-apidoc tool.
"""

import sys

module_path = 'E:\\cloud\\Videoaulas\\Digital Tutors - Procedural Rigging with Python in Maya\\procedural_rigging\\code\\python\\src'

# If the path is not in sys.path:
for path in sys.path:
    if path == module_path:
        break
else:
    sys.path.insert(0, module_path)

import procedural_rigging
reload(procedural_rigging)