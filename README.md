
# Pystrap

Wellcome to the official hosting site of pystrap, the project-setup-tool for python. The tool can be used to create all files needed for a minimal installable python project.
The goal of the project is to provide a simple method to create and setup the files needed to start developing a python application. The util is targeted towards developers
who want a standardized method to setup python projects. The script does not download any additional dependencies, so it is lightweigt and does not need any further configuration.

## Installation
To install the script, clone the latest version of the production branch and install the application using pip.

```
git clone https://github.com/MaxWeise/pystrap
cd pystrap/
pip install .
```

The script can be installed with or without a virtual environment, depending on your needs.

## Usage
To create a simple environment, use the command ` pystrap <project_name> `.
This will create the following project layout:

```
    | src/
    |   | <project_name>/
    |   |   | __init__.py
    | tests/
    |   | __init__.py
    | pyproject.toml

```

The files contain default parameters that allow the project to be directly installed into a virtual environment.
For more information on how to use the script, please refer to the docs.

