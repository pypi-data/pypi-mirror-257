"""
git2version, a simple utiltiy to make PEP 440 version strings based on git history
"""
from setuptools import setup


try:
    from git2version import get_git_version
except ImportError:

    def get_git_version(major, minor, patch, *_, **__):
        """
        Version string for when get_git_version isn't installed...
        """
        if minor is None:
            minor = 0
        if patch is None:
            patch = 1
        return f"{major}.{minor}.{patch}"


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
)
