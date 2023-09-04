
# Pystrap

Wellcome to the official hosting site of pystrap, the project-setup-tool for python. The tool can be used to create all files needed for a minimal installable python project.
The goal of the project is to provide a simple method to create and setup the files needed to start developing a python application.

## Installation
Installing the script can be done using pip via the link to this repository.

```
pip install https://github.com/MaxWeise/pystrap
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

