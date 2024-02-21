"""
Test the version string is PEP 440 compliant
"""

import re
import os.path
from git2version.make_git_version import get_git_version


def test_version():
    """
    Test the version string is PEP 440 compliant
    """

    def is_canonical(version):
        # from https://peps.python.org/pep-0440/
        return (
            re.match(
                r"^([1-9][0-9]*!)?(0|[1-9][0-9]*)(\.(0|[1-9][0-9]*))*((a|b|rc)(0|[1-9][0-9]*))?\
                (\.post(0|[1-9][0-9]*))?(\.dev(0|[1-9][0-9]*))?$",
                version,
            )
            is not None
        )

    current_path = os.path.dirname(os.path.abspath(__file__))
    version = get_git_version(
        0,
        path=current_path,
    )
    print(f"Version: {version}")
    assert is_canonical(version)
