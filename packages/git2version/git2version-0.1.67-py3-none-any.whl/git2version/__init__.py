"""
git2version module to create a PEP 440 version string from a git repository's history
"""

from .make_git_version import get_git_version

__all__ = ["get_git_version"]
