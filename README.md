# Python project for procedural rigging in Autodesk Maya.

This project is based on my [python-maya-boilerplate](https://github.com/leonardpin-br/python-maya-boilerplate).



## It includes
    1. The code is heavly documented (using Sphinx and Google style docstrings),
    and HTML generation is preconfigured.
    2. The documentation is generated using the interpreter that comes with Maya (mayapy.exe)
    3. The project is organized as instructed in the course, but using my boilerplate.
    4. Unit tests and coverage are preconfigured (but not used).
    5. The package.json file has many useful scripts for cleaning the project,
    documentation and unit tests.
    6. The scripts directory has very useful BASH scripts.
    7. There are useful VSCODE tasks preconfigured.



## Before you begin
Read the instructions in the boilerplate's page ([python-maya-boilerplate](https://github.com/leonardpin-br/python-maya-boilerplate)).



## Inspirations and reference
This code is heavily influenced by the course
[Procedural Rigging with Python in Maya](https://www.pluralsight.com/courses/procedural-rigging-python-maya-2283),
taught by Jakub Krompolc. I chose to make changes of my own, though.



## External code
As instructed in the course, external code was integrated to complete functionality.
[bSkinSaver 1.1.0 for Maya (maya script)](https://www.highend3d.com/maya/script/bskinsaver-for-maya),
by Thomas Bittner, was placed inside the `rigTools` folder.
It was necessary to alter the original code because it did not work with
Maya 2020.



## Naming conventions
This project is dependent on rigid naming conventions.

### Folder naming conventions

### File naming conventions

### Naming conventions inside the Maya files
| Nodes    | convention  | Example    |
|----------|-------------|------------|
| Joints   | name#_jnt   | spine1_jnt |
| Curves   | name_crv    | spine_crv  |
| Locators | name_loc    | body_loc   |



## Folder structure
```
<project_root>
|-- .vscode                     (Visual Studio Code specific files)
|-- assets                      (for static 3D elements (Model, Rig, Textured Model, 3D environment))
|   `-- komodo                  (Should be the character's name)
|       |-- builder             (Should contain the skeleton file in .mb format)
|       |-- model               (Should contain the geometry file in .mb format)
|       |-- rig                 (Should contain the resulting rig)
|       `-- weights
|           `-- skinCluster     (Skin weight files should be saved here in .swt format)
|-- code                        (This folder may contain Python, MEL, etc.)
|   `-- python
|       `-- src                 (the python app)
|           |-- komodoRig
|           |-- rigLib
|           |   |-- base
|           |   |-- rig
|           |   |-- utils
|           |-- rigTools
|-- docs                        (for the generated HTML documentation and coverage reports)
|   |-- coverage                (for the generated HTML code coverage reports)
|   `-- sphinx                  (for the generated HTML documentation)
|-- node_modules                (Node.js specific files)
|-- py27env                     (virtual environment folder)
|-- resources                   (good to have and needed files)
|   `-- documentation_config    (configuration file for Sphinx)
|   `-- example_files           (files that can be used as reference)
|-- scripts                     (usefull bash scripts)
|-- tests                       (Should contain unit tests, if you decide to use them.)

```



## Dependencies
Read the instructions in the boilerplate's page ([python-maya-boilerplate](https://github.com/leonardpin-br/python-maya-boilerplate)).



## Which file will be executed?
Using this project, the procedural_rigging.py (``<project_root>/code/python/src/procedural_rigging.py``) will be
the file being executed from Autodesk Maya.

It is recommended to create a shelf button that imports the procedural_rigging.py file (there is
an example in the ``resources/example_files`` folder).
