import shlex
import subprocess
from pathlib import Path

import setuptools


def read_multiline_as_list(file_path: str) -> list[str]:
    with open(file_path) as fh:
        contents = fh.read().split("\n")
        if contents[-1] == "":
            contents.pop()
        return contents


def get_version() -> str:
    raw_git_cmd = "git describe --tags --abbrev=0"
    git_cmd = shlex.split(raw_git_cmd)
    git = subprocess.check_output(git_cmd)
    return git.decode().strip()


with open("README.md", "r") as fh:
    long_description = fh.read()

requirements = read_multiline_as_list("requirements.txt")

setuptools.setup(
    name="crypteia",
    version=get_version(),
    author="Nei Cardoso de Oliveira Neto",
    author_email="nei@teialabs.com",
    description="Cryptographer's content-addressing companion.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    python_requires=">=3.11",
    install_requires=requirements,
)
