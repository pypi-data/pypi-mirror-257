#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import setuptools
import os
import sys

parent_path = os.path.relpath(".")
path_to_file = os.path.join(parent_path, "README.md")

with open(path_to_file, "r") as f:
    long_description = f.read()

install_requires_3_7 = [
    "biopython ~= 1.81",
    "matplotlib ~= 3.5.3",
    "numpy ~= 1.21",
    "pandas ~= 1.1",
    "pomegranate ~= 0.14",
    "requests ~= 2.0",
    "scikit-learn ~= 1.0.2",
    "scipy == 1.7.3",
    "torch == 1.13.1",
    "torchvision == 0.14.1",
    "urllib3 ~= 1.26.6"
]
install_requires_3_8 = [
    "biopython ~= 1.81",
    "matplotlib ~= 3.5.3",
    "numpy ~= 1.24",
    "pandas ~= 1.1",
    "pomegranate ~= 0.14",
    "requests ~= 2.0",
    "scikit-learn ~= 1.0.2",
    "scipy == 1.10.1",
    "torch == 1.13.1",
    "torchvision == 0.14.1",
    "urllib3 ~= 1.26.6",
]
install_requires_3_9 = [
    "biopython ~= 1.81",
    "matplotlib ~= 3.5.3",
    "numpy ~= 1.24",
    "pandas ~= 1.1",
    "pomegranate ~= 0.14",
    "requests ~= 2.0",
    "scikit-learn ~= 1.0.2",
    "scipy == 1.10.1",
    "torch == 1.13.1",
    "torchvision == 0.14.1",
    "urllib3 ~= 1.26.6",
]
install_requires_3_10 = [
    "apricot-select >= 0.6.1",
    "biopython ~= 1.81",
    "matplotlib ~= 3.5.3",
    "numpy ~= 1.24",
    "pandas ~= 1.1",
    "pomegranate ~= 0.14",
    "requests ~= 2.0",
    "scikit-learn ~= 1.0.2",
    "scipy >= 1.6.2",
    "torch == 1.13.1",
    "torchvision == 0.14.1",
    "urllib3 ~= 1.26.6",
]
install_requires_3_11 = [
    "biopython ~= 1.81",
    "matplotlib ~= 3.5.3",
    "numpy ~= 1.24",
    "pandas ~= 1.1",
    "pomegranate ~= 0.14",
    "requests ~= 2.0",
    "scikit-learn ~= 1.0.2",
    "scipy >= 1.6.2",
    "torch == 1.13.1",
    "torchvision == 0.14.1",
    "urllib3 ~= 1.26.6",
]

dependencies_to_install  = []

if sys.version_info.major == 3 and sys.version_info.minor == 11:
    dependencies_to_install = install_requires_3_11
elif sys.version_info.major == 3 and sys.version_info.minor == 10:
    dependencies_to_install = install_requires_3_10
elif sys.version_info.major == 3 and sys.version_info.minor == 9:
    dependencies_to_install = install_requires_3_9
elif sys.version_info.major == 3 and sys.version_info.minor == 8:
    dependencies_to_install = install_requires_3_8
elif sys.version_info.major == 3 and sys.version_info.minor == 7:
    dependencies_to_install = install_requires_3_7

setuptools.setup(
    name="b2bTools",
    version="3.0.7b1",
    author="Wim Vranken",
    author_email="Wim.Vranken@vub.be",
    description="bio2Byte software suite to predict protein biophysical properties from their amino-acid sequences",
    license="OSI Approved :: GNU General Public License v3 (GPLv3)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    maintainer="Jose Gavalda-Garcia, Adrian Diaz, Wim Vranken",
    maintainer_email="jose.gavalda.garcia@vub.be, adrian.diaz@vub.be, wim.vranken@vub.be",
    url="https://bio2byte.be",
    project_urls={
        "Documentation": "https://bio2byte.be/b2btools/package-documentation",
        "HTML interface" : "https://bio2byte.be/b2btools"
    },
    packages=setuptools.find_packages(exclude=("**/test/**",)),
    include_package_data=True,
    keywords="bio2byte,b2bTools,biology,bioinformatics,bio-informatics,fasta,proteins,protein-folding",
    classifiers=[
        "Natural Language :: English",
        # Python 3.7 Release date: 2018-06-27, End of full support: 2020-06-27
        "Programming Language :: Python :: 3.7",
        # Python 3.8 Release date: 2019-10-14, End of full support: 2021-05-03
        "Programming Language :: Python :: 3.8",
        # Python 3.9 Release date: 2020-10-05, End of full support: 2022-05-17
        "Programming Language :: Python :: 3.9",
        # Python 3.10 Release date: 2021-10-04, End of full support: 2023-04-05
        "Programming Language :: Python :: 3.10",
        # Python 3.11 Release date: 2022-10-24, End of full support: 2024-04-01
        "Programming Language :: Python :: 3.11",
        # Python 3.12 Release date: 2023-10-02, End of full support: 2025-05
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",

        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",

        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Scientific/Engineering :: Chemistry",
        "Topic :: Scientific/Engineering :: Physics",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
        "Development Status :: 5 - Production/Stable"
    ],
    python_requires=">=3.7, <=3.12",
    install_requires=dependencies_to_install,
    entry_points={
        "console_scripts": [
            "b2bTools = b2bTools.__main__:main",
        ],
    },
)
