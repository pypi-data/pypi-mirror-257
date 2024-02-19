from setuptools import setup, find_packages

import todo


with open("requirements.txt") as f:
    required = f.read().splitlines()


setup(
    name=todo.__title__,
    version=todo.__version__,
    description=todo.__description__,
    author=todo.__author__,
    install_requires=required,
    author_email=todo.__author_email__,
    packages=find_packages(exclude=["tests", "tests.*"]),
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
