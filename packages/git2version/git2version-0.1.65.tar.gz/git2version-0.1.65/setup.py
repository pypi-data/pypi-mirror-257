"""
git2version, a simple utiltiy to make PEP 440 version strings based on git history
"""
from setuptools import setup


try:
    from git2version import get_git_version
except ModuleNotFoundError:
    import pip

    pip.main(["install", "GitPython"])  # call pip to install them
    from git2version import get_git_version
except ImportError:
    from .git2version import get_git_version


setup(
    name="git2version",
    version=get_git_version(
        major=0,
        minor=None,  # Optionally set, default (None) will count the number of merges
        patch=None,  # Optionally set, default (None) will count the number of commits
        path=".",
    ),  # This is the version of the package
    license="MIT",
    author="Joseph McKenna",
    author_email="jtkmckenna@quantifiedcarbon.com",
    description="A tool to create a project version number from a git repository",
    packages=["git2version"],
    install_requires=[
        "GitPython",
    ],
    setup_requires=[
        "GitPython",
    ],
    long_description=r"""A tool to create a project version number from a git repository

    Generates a PEP 440 compliant string based on the git history of the repository.

    The version string is generated as follows:
    {major_version}.{minor_version}.{patch_version}{a{number_of_files_changed}}{b{number_of_untracked_files}}
    Where the {major_version} is set by the user
    The {minor_version} is the number of merges
    The {patch_version} is the number of commits
    The {number_of_files_changed} is the number of files changed
    The {number_of_untracked_files} is the number of untracked files

    If the repoistory is prestine, then with will not be marked as 'alpha' or 'beta'

    """,
)
