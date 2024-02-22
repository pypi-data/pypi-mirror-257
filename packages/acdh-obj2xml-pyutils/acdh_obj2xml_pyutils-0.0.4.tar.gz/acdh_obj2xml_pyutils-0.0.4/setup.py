#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open("README.md") as readme_file:
    readme = readme_file.read()


requirements = [
    "lxml",
    "jinja2"
]

setup_requirements = []

test_requirements = []

setup(
    author="Daniel Stoxreiter",
    author_email="daniel.stoxreiter@oeaw.ac.at",
    python_requires=">=3.8",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
    ],
    description="Utility functions to serialize xml from object",
    install_requires=requirements,
    license="MIT license",
    long_description=readme,
    long_description_content_type="text/markdown",
    include_package_data=True,
    name="acdh_obj2xml_pyutils",
    packages=find_packages(include=["acdh_obj2xml_pyutils", "acdh_obj2xml_pyutils.*"]),
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/acdh-oeaw/acdh-obj2xml-pyutils",
    version="v0.0.4",
    zip_safe=False,
)
