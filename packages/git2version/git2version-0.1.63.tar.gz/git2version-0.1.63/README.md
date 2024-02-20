git2version

A simple tool to build a version number of a python package (PEP 440) from git history

The PEP 440 version string is: {major}.{minor}.{patch}

'major' is controlled by the user
'minor' is calculated from the number of merges in the git history
'patch' is calculated from the nubmer of commits in the git history

To use this in your setup.py, simple add:

```
import pip
pip.main(['install', 'git2version'])    # call pip to install them
from git2version import get_git_version
```

At the top of your setup.py (this will install git2version for you if its not already installed, 
then import it)

The version string can be calculated in the setuptools call, eg:

```
setup(
    name="My Project",
    version=get_git_version(major=0),
    author="Your Name",
    author_email="user.name@email.com",
    install_requires=["numpy", "pandas"],
    python_requires=">=3.9",
)
```