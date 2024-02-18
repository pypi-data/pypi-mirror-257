from setuptools import find_packages, setup

FILE_NAME = "VERSION"


def get_version():
    with open(FILE_NAME) as file:
        return file.read()


def get_base_requirements():
    with open("requirements.txt") as file:
        return file.readlines()


def get_long_description():
    with open("README.md", encoding="utf-8") as file:
        return file.read()


setup(
    name="popug_legacy_sdk",
    version=get_version(),
    package_data={"popug_legacy_sdk": ["py.typed"]},
    description="Package for popug_legacy project",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/harroowd/popyg_legacy",
    author="Andrei Kazlou",
    author_email="andrey.vs1998@gmail.com",
    packages=find_packages(),
    install_requires=get_base_requirements(),
    include_package_data=True,
    zip_safe=False,
)
