# Python project for procedural rigging in Autodesk Maya.

This project is based on my [python-maya-boilerplate](https://github.com/leonardpin-br/python-maya-boilerplate).

## It includes
    1. The code is heavly documented (using Sphinx and Google style docstrings) and HTML generation
    is preconfigured.
    2. The project is organized as instructed in the course, but using my boilerplate.
    3. Unit tests and coverage are preconfigured (but not used).
    4. The `package.json` file has many useful scripts for cleaning the project,
    documentation and unit tests.

## Inspirations and reference
This code is heavily influenced by the course
[Procedural Rigging with Python in Maya](https://www.pluralsight.com/courses/procedural-rigging-python-maya-2283)
taught by Jakub Krompolc. I chose to make changes of my own, though.

## External code
As instructed in the course, external code was integrated to complete functionality.
[bSkinSaver 1.1.0 for Maya (maya script)](https://www.highend3d.com/maya/script/bskinsaver-for-maya),
by Thomas Bittner, was placed inside the `rigTools` folder. It was necessary to
alter the original code because it did not work with Maya 2020.

## Naming conventions
This project is dependent on rigid naming conventions.

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
|   `-- example_files           (files that can be used as reference)
|-- scripts                     (usefull bash scripts)
|-- tests                       (Should contain unit tests, if you decide to use them.)

```

## Dependencies
It depends on Node.js, but only for development (documentation and unit tests).

Install Node.js and navigate to the root folder of this project. Install node
dependencies with the command:
```
npm install
```

The `package.json` file has many useful scripts.

It is important to install the correct Python version (2.7.11 for Maya 2020)
in the operating system and to create a virtual environment (py27env folder)
in the root folder of this project.

Activate the virtual environment with the command:
```
source ./py27env/Scripts/activate
```

After that, it is important to install the necessary packages (inside the virtual
environment) using:
```
pip install -r requirements.txt
```

## Which file will be executed?
Using this project, the procedural_rigging.py (``<project_root>/code/python/src/procedural_rigging.py``) will be
the file being executed from Autodesk Maya.

It is recommended to create a shelf button that imports the procedural_rigging.py file (there is
an example in the ``resources/example_files`` folder).
