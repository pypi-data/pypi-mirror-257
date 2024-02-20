# make a setup.py for data-processing package

from typing import List

from setuptools import find_packages, setup


def load_requirements() -> List[str]:
    requirements: List[str] = []
    with open("requirements.txt", encoding="utf-8") as f:
        requirements.extend(f.readlines())
    return requirements

setup(
    name="kubeagi",
    description="Data Processing is used for data processing through MinIO, databases, Web APIs, etc.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    keywords="PDF WORD WEB parsing preprocessing",
    url="https://github.com/kubeagi/core-library",
    python_requires=">=3.8",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
    ],
    version="0.0.4",
    install_requires=load_requirements(),

)
