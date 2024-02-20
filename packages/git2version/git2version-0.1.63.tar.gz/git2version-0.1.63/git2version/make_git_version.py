"""
Simple module to estimate the version of a git repository


"""
from typing import Optional
from os import getcwd
from git import Repo, InvalidGitRepositoryError


def estimate_merges(repo):
    """
    Iterate through the commits and count the number of merges (commits with more than one parent)
    """
    merges = 0
    for commit in repo.iter_commits():
        if len(commit.parents) > 1:
            merges += 1
    return merges


def estimate_commits(repo):
    """
    Count the number of commits in the repository
    """
    return len(list(repo.iter_commits()))


def count_unstaged_files(repo):
    """
    Look for uncommitted changes in the repository

    Count the number of unstaged files in the repository
    """
    return len(repo.index.diff(None))


def count_staged_files(repo):
    """
    Look for uncommitted changes in the repository

    Count the number of staged files in the repository
    """
    return len(repo.index.diff("HEAD"))


def count_untracked_files(repo):
    """
    Look for uncommitted changes in the repository

    Count the number of untracked files in the repository (new files / data files not in .gitignore)
    """
    return len(repo.untracked_files)


def test():
    """
    Test the module
    """
    repo = Repo(search_parent_directories=True)
    merges = estimate_merges(repo)
    commits = estimate_commits(repo)
    print("Merges:", merges)
    print("Commits:", commits)
    print("Unstaged:", count_unstaged_files(repo))
    print("Staged:", count_staged_files(repo))
    print("Untracked:", count_untracked_files(repo))


def build_version_string(
    major: int,
    minor: int,
    patches: int,
    changed_files: int,
    untracked_files: int,
):
    """
    Build a version string from the major, minor, and patch numbers

    PEP 440: https://www.python.org/dev/peps/pep-0440/
    """
    version_string = f"{major}.{minor}.{patches}"

    repo_modified = bool(changed_files)
    repo_has_untracked_files = bool(untracked_files)
    if repo_modified:
        version_string += f"a{changed_files}"
    else:
        # If there are only untracked files... mark this release as 'beta'
        if repo_has_untracked_files:
            version_string += f"b{untracked_files}"
    return version_string


def get_git_version(
    major: int,
    minor: Optional[int] = None,
    patch: Optional[int] = None,
    path: Optional[str] = None,
):
    """
    Get the version of the git repository (PEP 440)

    PEP 440: https://www.python.org/dev/peps/pep-0440/

    major: int
        The major version number
    minor: int
        The minor version number
    patch: int
        The patch version number
    path: str
        The path to the git repository
    """
    try:
        repo = Repo(path, search_parent_directories=True)
    except InvalidGitRepositoryError as e:
        # Find the string git2version- in the path:
        if path == ".":
            path = getcwd()

        if "git2version-" not in path:
            raise e
        # Get the string between git2version- and /:
        version_from_path = path.split("git2version-")[1].split("/")[0]
        return version_from_path
    print(f"Generating version for repository: {repo.working_dir}")
    if minor is None:
        minor = estimate_merges(repo)
    if patch is None:
        patch = estimate_commits(repo)

    return build_version_string(
        major=major,
        minor=minor,
        patches=patch,
        changed_files=count_unstaged_files(repo) + count_staged_files(repo),
        untracked_files=count_untracked_files(repo),
    )


if __name__ == "__main__":
    test()
