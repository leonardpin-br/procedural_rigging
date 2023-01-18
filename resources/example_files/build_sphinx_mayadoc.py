#!/C/Program Files/Autodesk/Maya2020/bin/mayapy
u"""(Tries to) Serve as a configuration file to Sphinx to work with Maya 2020 modules.

I do not know how to make it work yet.

References:
    `Getting Sphinx to work with Maya modules`_

.. _Getting Sphinx to work with Maya modules:
   https://geektalker.wordpress.com/2013/03/26/getting-sphinx-to-work-with-maya-modules/
"""

import os
import sys

import sphinx

import maya.standalone
maya.standalone.initialize(name='python')

if __name__ == '__main__':

    # get everything after the script name
    argv = sys.argv[1:]

    # Returns a string which stands for the current working directory.
    cwd = os.getcwd()

    # The insert() method inserts the specified value at the specified position.
    argv.insert(0, sphinx.__file__)


    sphinx.main(argv)
