# Python project for procedural rigging in Autodesk Maya.

This project is based on my [python-maya-boilerplate](https://github.com/leonardpin-br/python-maya-boilerplate).

## Inspirations and reference
This code is heavily influenced by the course
[Procedural Rigging with Python in Maya](https://www.pluralsight.com/courses/procedural-rigging-python-maya-2283)
taught by Jakub Krompolc.

## Folder structure
```
<project_root>
|-- assets                      (Contain static 3D element (e.g. Model, Rig, Textured Model, 3d environment))
|   `-- komodo                  (The character's name)
|       |-- builder             (The skeleton folder containing the .mb file)
|       |-- model               (The geometry folder containing the .mb file)
|       |-- rig                 (The resulting rig)
|       `-- weights
|           `-- skinCluster     (Weight files are saved here in .swt format)
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
|-- resources                   (good to have and needed files)
|   `-- example_files           (files that can be used as reference)
|-- scripts                     (usefull bash scripts)
|-- tests                       (unit tests)

```

## It includes
    1. Easy password hashing and verification (bcrypt). Even though Autodesk Maya is not able to load
    the BCrypt package, if the user of this kit needs to hash and verify a password, it is already
    preconfigured.
    2. An abstract class to be inherited by all the others that access
    the database. It is an application of the __active record__ design pattern.
    3. Two example subclasses are provided. One for a product and one for
    an admin, both are subclasses of the database one (active record).
    4. The code is heavly documented (using Sphinx and Google style docstrings) and HTML generation
    is preconfigured.
    5. General and validation functions that can be easily reused in other
    projects.
    6. Unit tests and coverage are preconfigured.

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
