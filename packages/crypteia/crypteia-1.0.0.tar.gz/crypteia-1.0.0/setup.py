from setuptools import find_packages, setup


def read_multiline_as_list(file_path: str) -> list[str]:
    with open(file_path) as fh:
        contents = fh.read().split("\n")
        if contents[-1] == "":
            contents.pop()
        return contents


requirements = read_multiline_as_list("requirements.txt")

setup(
    name="crypteia",
    version="1.0.0",
    author="Nei Cardoso de Oliveira Neto",
    author_email="nei@teialabs.com",
    description="Cryptographer's content-addressing companion.",
    packages=find_packages("crypteia"),
    install_requires=requirements,
)
