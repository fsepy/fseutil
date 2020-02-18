# fseutil

Fire Safety Engineering Tools.


## Getting Started

Documentation is under construction.

### Installation

[Python](https://www.python.org/downloads/) 3.7 or later is required. [Anaconda Distribution](https://www.anaconda.com/distribution/#download-section) is recommended for new starters, it includes Python and few useful packages including a package management tool pip (see below).

[pip](https://pypi.org/) is a package management system for installing and updating Python packages. pip comes with Python, so you get pip simply by installing Python. On Ubuntu and Fedora Linux, you can simply use your system package manager to install the `python3-pip` package. [The Hitchhiker's Guide to Python](https://docs.python-guide.org/starting/installation/) provides some guidance on how to install Python on your system if it isn't already; you can also install Python directly from [python.org](https://www.python.org/getit/). You might want to [upgrade pip](https://pip.pypa.io/en/stable/installing/) before using it to install other programs.

1. to use `pip` install from PyPI:

    [![Downloads](https://pepy.tech/badge/sfeprapy)](https://pepy.tech/project/sfeprapy)

    ```sh
    pip install --upgrade sfeprapy
    ```

2. to use `pip` install from GitHub (requires [git](https://git-scm.com/downloads)):  

    *Note installing `SfePrapy` via this route will include the lastest commits/changes to the library.*  

    ```sh
    pip install --upgrade "git+https://github.com/fsepy/SfePrapy.git@master"
    ```


### Command line interface

`sfeprapy` command line interface (CLI) uses the current working directory to obtain and/or save files.


## Authors

**Ian Fu** - *fuyans@gmail.com*

## License

This project is licensed under the Apache License version 2.0 - see the [LICENSE](LICENSE) file for details
