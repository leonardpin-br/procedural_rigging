# Python project for procedural rigging in Autodesk Maya.

This project is based on my [python-maya-boilerplate](https://github.com/leonardpin-br/python-maya-boilerplate).



## It includes
    1. The code is heavly documented (using Sphinx and Google style docstrings), and HTML generation
    is preconfigured.
    2. The documentation is generated using the interpreter that comes with Maya (mayapy.exe)
    3. The project is organized as instructed in the course, but using my boilerplate.
    4. Unit tests and coverage are preconfigured (but not used).
    5. The package.json file has many useful scripts for cleaning the project,
    documentation and unit tests.
    6. The scripts directory has very useful BASH scripts.



## Before you begin
Make sure you clone this repository to a path without spaces in it. Maya can and do execute without problems, but Sphinx will throw an error if there are any spaces in the path.



## Inspirations and reference
This code is heavily influenced by the course
[Procedural Rigging with Python in Maya](https://www.pluralsight.com/courses/procedural-rigging-python-maya-2283),
taught by Jakub Krompolc. I chose to make changes of my own, though.



## External code
As instructed in the course, external code was integrated to complete functionality.
[bSkinSaver 1.1.0 for Maya (maya script)](https://www.highend3d.com/maya/script/bskinsaver-for-maya),
by Thomas Bittner, was placed inside the `rigTools` folder. It was necessary to
alter the original code because it did not work with Maya 2020.



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
|   `-- example_files           (files that can be used as reference)
|-- scripts                     (usefull bash scripts)
|-- tests                       (Should contain unit tests, if you decide to use them.)

```



## Dependencies

### Node.js
It depends on Node.js, but only for development (documentation and unit tests).

Install Node.js and navigate to the root folder of this project. Install node
dependencies with the command:

```
npm install
```

The provided `package.json` file has many useful scripts.

### Python version and virtual environments

In my case, I installed a Python 3 version first (so I can install tools like Qt Designer later) and them installed the virtualenv package. This will allow you to create virtual environments.

You can do it with only one Python version ([Create virtualenv in Python 2.7 on windows 10 while other virtualenv are working in Python 3.8](https://stackoverflow.com/a/64940580/3768670)) if you want.

```
pip install virtualenv
```

After that, install the correct version (2.7.11 for Maya 2020)
in the operating system.

Then, create a virtual environment (`py27env` folder)
in the root folder of this project. Run this command from the project's root folder:

```
virtualenv --python="C:/Program Files/Python27/python.exe" "./py27env"
```

Activate the virtual environment with the command:
```
source ./py27env/Scripts/activate   => Cygwin and Git Bash
py27env\Scripts\activate            => Command Prompt
py27env\Scripts\activate.ps1        => PowerShell
```

After that, it is important to install the necessary packages using the command below from the project root:
```
pip install -r requirements.txt
```
It will install all the packages, including the appropriate version of Sphinx.



## Documentation
By now, you should have installed Sphinx inside the virtual environment (`py27env` folder).

### Terminals on Windows systems
On Windows systems, the terminal you are using makes a big difference. On my tests, I used
- Command Prompt
- Cygwin
- Git Bash
- Powershell

Even after activating the virtual environment in all of them, the results may differ.

### The shebang line

Windows do not support the shebang line (the first line starting with `#! `). But, since Python 3.3 ([Should I put #! (shebang) in Python scripts, and what form should it take?](https://stackoverflow.com/a/14599026/3768670)), Python installs launchers like

```
"C:\Windows\pyw.exe"
```

The `.py` files should be associated with the above laucher as the default program to execute them.

___________

In my tests, **the shebang line only makes a difference if the main script file is executed directly.** That is what will be discussed below.

___________

#### The tested shebang lines

The laucher **does read** the shebang lines. The commands for each terminal are:
```
code/python/src/procedural_rigging.py       => Cygwin and Git Bash
code\python\src\procedural_rigging.py       => Command Prompt
.\code\python\src\procedural_rigging.py     => PowerShell
```

The result is:

```
#! mayapy.exe                                           => Cygwin only accepts this one.
#! /c/Progra~1/Autodesk/Maya2020/bin/mayapy.exe         => Git Bash accepts the first and this one.
#! "C:\Program Files\Autodesk\Maya2020\bin\mayapy.exe"  => Only accepted by Command Prompt and PowerShell.
```

The only shebang line that worked in all of the tested terminals is `#! mayapy.exe`. That line depends on the alteration of the system environment variables. The steps are listed below.

### Step-by-step on Windows systems
For the documentation generation to work as expected, it is necessary to do the following:

#### 1. Edit the environment variables
Add the path to the `mayapy.exe` to the system variables. The default path is
```
C:\Program Files\Autodesk\Maya2020\bin
```
Move it tho the top of the list.

#### 2. Edit the make.bat file
Sphinx will be configured to use the Maya interpreter (`mayapy.exe`) instead of the interpreter in the virtual environment.

`sphinx-quickstart` created two important files (they are inside the `<project_root>/docs/sphinx` folder):

```
make.bat    => Edit this one if you are on Windows.
Makefile
```

There is a script in the `package.json` file to make it easy. Just run this command
in a terminal like **Cygwin** or **Git Bash**:

```
npm run update:make_bat
```

It executes a BASH script (`<project_root>/scripts/update_make_bat.sh`). In turn, that script edits the `make.bat` file with the follwing:

```
set SPHINXBUILD=mayapy "full/path/to/the/build_sphinx_mayadoc.py"
```

The `mayapy` command is important. Without it, all terminals fail to generate the documentation.

The above file (`build_sphinx_mayadoc.py`) is a custom config file that instructs Sphinx to work with the Maya modules.

___________

**With the `mayapy` command, the shebang line (`#! mayapy.exe`) inside `build_sphinx_mayadoc.py` makes absolutely no difference. It works with or without it.**

___________

### If the Makefile is edited instead of the make.bat

The result is the same on all terminals:

- The Python executable is the one inside the py27env.

- That interpreter does not now any Maya module. So, it fails to import them.



## Which file will be executed?
Using this project, the procedural_rigging.py (``<project_root>/code/python/src/procedural_rigging.py``) will be
the file being executed from Autodesk Maya.

It is recommended to create a shelf button that imports the procedural_rigging.py file (there is
an example in the ``resources/example_files`` folder).
