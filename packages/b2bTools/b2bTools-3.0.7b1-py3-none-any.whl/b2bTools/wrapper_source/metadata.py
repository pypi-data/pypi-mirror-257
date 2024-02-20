import os
import re
import datetime
import platform
from ..singleSeq import constants

class Bio2ByteMetadata:
    def __init__(self, execution_type, tools):
        self.execution_type = execution_type
        self.tools = tools
        self.version = self.find_version()

    def find_version(self):
        current_dir = os.path.dirname(os.path.realpath(__file__))
        module_dir = os.path.dirname(current_dir)
        general_dir = os.path.dirname(module_dir)

        setup_file_path = os.path.join(general_dir, "setup.py")
        version_match = re.compile(r"^.*version=['\"]([^'\"]*)['\"],.*$", re.M)
        with open(setup_file_path, 'r') as f:
            setup_contents = f.read()

        version = version_match.search(setup_contents)

        if version:
            return version.group(1)
        return "Version could not be extracted from setup.py"

    def build_metadata_dict(self):
        metadata_dict = {
            "title": "Prediction results of B2BTools package",
            "description": "This file contains the results of Bio2Byte predictors for proteins",
            "mode": self.execution_type,
            "package": {
                "name": "b2bTools",
                "version": self.version,
                "URL": f"https://pypi.org/project/b2bTools/{self.version}/",
                "releaseDate": "2024-02-15",
            },
            "URL": [
                {
                    "Homepage": "https://bio2byte.be",
                    "REST API": "https://bio2byte.be/b2btools/package-documentation",
                    "Repository": "http://bitbucket.org/bio2byte/b2btools",
                    "PyPI (Python Package Index)": "https://pypi.org/project/b2bTools/",
                    "Conda": "https://anaconda.org/Bio2Byte/b2bTools",
                    "BioConda": "https://bioconda.github.io/recipes/b2btools/README.html"
                }
            ],
            "containers": self.containers_metadata(),
            "email": [
                "bio2byte@vub.be"
            ],
            "publications": [
                {
                    "identifierType": "DOI",
                    "identifier": "https://doi.org/10.1093/nar/gkab425",
                    "title": "b2bTools: online predictions for protein biophysical features and their conservation",
                    "authors": "Luciano Porto Kagami, Gabriele Orlando, Daniele Raimondi, Francois Ancien, Bhawna Dixit, Jose Gavaldá-García, Pathmanaban Ramasamy, Joel Roca-Martínez, Konstantina Tzavella, Wim Vranken",
                    "journal": "Nucleic Acids Research",
                    "year": 2021
                }
            ],
            "tools": self.tools_metadata(),
            "executionDetails": self._execution_metadata(),
            "copyright": "© Wim Vranken, Bio2Byte group, Vrije Universiteit Brussel (VUB), Belgium",
            "license": "GNU General Public License v3 (GPLv3)",
        }

        return metadata_dict

    def containers_metadata(self):
        return [
            {
                "type": "Docker",
                "URL": "https://hub.docker.com/r/diazadriang/b2btools/",
                "image": f"diazadriang/b2btools:{self.version}_pypi_py3.7",
                "description": f"b2bTools v{self.version} for Python v3.7 using PyPI to install dependencies"
            },
            {
                "type": "Docker",
                "URL": "https://hub.docker.com/r/diazadriang/b2btools/",
                "image": f"diazadriang/b2btools:{self.version}_pypi_py3.8",
                "description": f"b2bTools v{self.version} for Python v3.8 using PyPI to install dependencies"
            },
            {
                "type": "Docker",
                "URL": "https://hub.docker.com/r/diazadriang/b2btools/",
                "image": f"diazadriang/b2btools:{self.version}_pypi_py3.9",
                "description": f"b2bTools v{self.version} for Python v3.9 using PyPI to install dependencies"
            },
            {
                "type": "Docker",
                "URL": "https://hub.docker.com/r/diazadriang/b2btools/",
                    "image": f"diazadriang/b2btools:{self.version}_pypi_py3.10",
                "description": f"b2bTools v{self.version} for Python v3.10 using PyPI to install dependencies"
            },
            {
                "type": "Docker",
                "URL": "https://hub.docker.com/r/diazadriang/b2btools/",
                    "image": f"diazadriang/b2btools:{self.version}_pypi_py3.11",
                "description": f"b2bTools v{self.version} for Python v3.11 using PyPI to install dependencies"
            },
            {
                "type": "Docker",
                "URL": "https://hub.docker.com/r/diazadriang/b2btools/",
                "image": f"diazadriang/b2btools:{self.version}_conda_py3.7",
                "description": f"b2bTools v{self.version} for Python v3.7 using MiniConda3 to install dependencies"
            },
            {
                "type": "Docker",
                "URL": "https://hub.docker.com/r/diazadriang/b2btools/",
                "image": f"diazadriang/b2btools:{self.version}_conda_py3.8",
                "description": f"b2bTools v{self.version} for Python v3.8 using MiniConda3 to install dependencies"
            },
            {
                "type": "Docker",
                "URL": "https://hub.docker.com/r/diazadriang/b2btools/",
                "image": f"diazadriang/b2btools:{self.version}_conda_py3.9",
                "description": f"b2bTools v{self.version} for Python v3.9 using MiniConda3 to install dependencies"
            },
            {
                "type": "Docker",
                "URL": "https://hub.docker.com/r/diazadriang/b2btools/",
                    "image": f"diazadriang/b2btools:{self.version}_conda_py3.10",
                "description": f"b2bTools v{self.version} for Python v3.10 using MiniConda3 to install dependencies"
            },
            {
                "type": "Docker",
                "URL": "https://hub.docker.com/r/diazadriang/b2btools/",
                    "image": f"diazadriang/b2btools:{self.version}_conda_py3.11",
                "description": f"b2bTools v{self.version} for Python v3.11 using MiniConda3 to install dependencies"
            }
        ]

    def tools_metadata(self):
        tools_metadata = {}
        if constants.TOOL_DYNAMINE in self.tools:
            tools_metadata[constants.TOOL_DYNAMINE] = self.add_dynamine_metadata()
        if constants.TOOL_DISOMINE in self.tools:
            tools_metadata[constants.TOOL_DISOMINE] = self.add_disomine_metadata()
        if constants.TOOL_AGMATA in self.tools:
            tools_metadata[constants.TOOL_AGMATA] = self.add_agmata_metadata()
        if constants.TOOL_EFOLDMINE in self.tools:
            tools_metadata[constants.TOOL_EFOLDMINE] = self.add_efoldmine_metadata()
        if constants.TOOL_PSP in self.tools:
            tools_metadata[constants.TOOL_PSP] = self.add_psp_metadata()
        if constants.TOOL_SHIFTCRYPT in self.tools:
            tools_metadata[constants.TOOL_SHIFTCRYPT] = self.add_shiftcrypt_metadata()

    def add_dynamine_metadata(self):
        return {
            "predictorName": "DynaMine",
            "URL": ["https://bio2byte.be/b2btools/dynamine/"],
            "publications": [
                {
                    "identifierType": "DOI",
                    "identifier": "https://doi.org/10.1038/ncomms3741",
                    "title": "From protein sequence to dynamics and disorder with DynaMine",
                    "authors": "Elisa Cilia, Rita Pancsa, Peter Tompa, Tom Lenaerts, Wim Vranken",
                    "journal": "Nature Communications",
                    "year": 2013
                },
                {
                    "identifierType": "DOI",
                    "identifier": "https://doi.org/10.1093/nar/gku270",
                    "title": "The DynaMine webserver: predicting protein dynamics from sequence",
                    "authors": "Elisa Cilia, Rita Pancsa, Peter Tompa, Tom Lenaerts, Wim Vranken",
                    "journal": "Nucleic Acids Research",
                    "year": 2014
                }
            ],
        }

    def add_disomine_metadata(self):
        return {
            "predictorName": "DisoMine",
            "URL": ["https://bio2byte.be/b2btools/disomine/"],
            "publications": [
                {
                    "identifierType": "DOI",
                    "identifier": "https://doi.org/10.1016/j.jmb.2022.167579",
                    "title": "Prediction of Disordered Regions in Proteins with Recurrent Neural Networks and Protein Dynamics",
                    "authors": "Gabriele Orlando, Daniele Raimondi, Francesco Codicè, Francesco Tabaro, Wim Vranken",
                    "journal": "Journal of Molecular Biology",
                    "year": 2022
                }
            ],
        }

    def add_agmata_metadata(self):
        return {
            "predictorName": "AgMata",
            "URL": ["https://bio2byte.be/b2btools/agmata/"],
            "publications": [
                {
                    "identifierType": "DOI",
                    "identifier": "https://doi.org/10.1093/bioinformatics/btz912",
                    "title": "Accurate prediction of protein beta-aggregation with generalized statistical potentials",
                    "authors": "Gabriele Orlando, Alexandra Silva, Sandra Macedo-Ribeiro, Daniele Raimondi, Wim Vranken",
                    "journal": "Bioinformatics",
                    "year": 2020
                }
            ],
        }

    def add_efoldmine_metadata(self):
        return {
            "predictorName": "EFoldMine",
            "URL": ["https://bio2byte.be/b2btools/efoldmine/"],
            "publications": [
                {
                    "identifierType": "DOI",
                    "identifier": "https://doi.org/10.1093/bioinformatics/btz912",
                    "title": "Exploring the Sequence-based Prediction of Folding Initiation Sites in Proteins",
                    "authors": "Daniele Raimondi, Gabriele Orlando, Rita Pancsa, Taushif Khan, Wim Vranken",
                    "journal": "Scientific Reports",
                    "year": 2017
                }
            ],
        }

    def add_psp_metadata(self):
        return {
            "predictorName": "PSP (Phase Separating Protein)",
            "URL": ["https://bio2byte.be/b2btools/psp/"],
            "publications": [
                {
                    "identifierType": "DOI",
                    "identifier": "https://doi.org/10.1093/bioinformatics/btz274",
                    "title": "Computational identification of prion-like RNA-binding proteins that form liquid phase-separated condensates",
                    "authors": "Gabriele Orlando, Daniele Raimondi, Francesco Tabaro, Francesco Codicè, Yves Moreau, Wim Vranken",
                    "journal": "Bioinformatics",
                    "year": 2019
                }
            ],
        }

    def add_shiftcrypt_metadata(self):
        return {
            "predictorName": "ShiftCrypt",
            "URL": ["https://bio2byte.be/b2btools/shiftcrypt/"],
            "publications": [
                {
                    "identifierType": "DOI",
                    "identifier": "https://doi.org/10.1038/s41467-019-10322-w",
                    "title": "Auto-encoding NMR chemical shifts from their native vector space to a residue-level biophysical index",
                    "authors": "Gabriele Orlando, Daniele Raimondi, Wim Vranken",
                    "journal": "Nature Communications",
                    "year": 2019
                },
                {
                    "identifierType": "DOI",
                    "identifier": "https://doi.org/10.1093/nar/gkaa391",
                    "title": "ShiftCrypt: a web server to understand and biophysically align proteins through their NMR chemical shift values",
                    "authors": "Gabriele Orlando, Daniele Raimondi, Luciano Porto Kagami, Wim Vranken",
                    "journal": "Nucleic Acids Research",
                    "year": 2020
                }
            ],
        }

    def _execution_metadata(self):
        execution_time = datetime.datetime.now().isoformat()
        processor_info = platform.processor()
        os_info = platform.platform()

        execution_metadata = {
            "executionTime": execution_time,
            "hostDetails": {
                "processor": processor_info,
                "operatingSystem": os_info,
            },
            "tools": [],
            # "inputs": self._files_metadata([]),
            # "outputs": self._files_metadata([])
        }
        if constants.TOOL_DYNAMINE in self.tools:
            execution_metadata['tools'].append(constants.TOOL_DYNAMINE)
        if constants.TOOL_DISOMINE in self.tools:
            execution_metadata['tools'].append(constants.TOOL_DISOMINE)
        if constants.TOOL_AGMATA in self.tools:
            execution_metadata['tools'].append(constants.TOOL_AGMATA)
        if constants.TOOL_EFOLDMINE in self.tools:
            execution_metadata['tools'].append(constants.TOOL_EFOLDMINE)
        if constants.TOOL_PSP in self.tools:
            execution_metadata['tools'].append(constants.TOOL_PSP)
        if constants.TOOL_SHIFTCRYPT in self.tools:
            execution_metadata['tools'].append(constants.TOOL_SHIFTCRYPT)

        return execution_metadata

    def _files_metadata(self, files):
        files_metadata = []

        for file in files:
            files_metadata.append({
                {
                    "type": "file",
                    "format": "FASTA",
                    "required": True
                }
            })
