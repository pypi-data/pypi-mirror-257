[//]: # (Get inspiration for badges etc from morfeus, others?)
[![Testing](https://gitlab.com/aspuru-guzik-group/self-driving-lab/instruments/chemspyd/badges/main/pipeline.svg)](https://gitlab.com/aspuru-guzik-group/self-driving-lab/instruments/chemspyd/-/commits/main)
[![Coverage](https://gitlab.com/aspuru-guzik-group/self-driving-lab/instruments/chemspyd/badges/main/coverage.svg?job=coverage)](https://gitlab.com/aspuru-guzik-group/self-driving-lab/instruments/chemspyd/-/commits/main)
<!-- [![Endpoint Badge](https://img.shields.io/endpoint?url=https://gitlab.com/aspuru-guzik-group/self-driving-lab/instruments/chemspyd/-/raw/main/documentation/badge.json)](https://aspuru-guzik-group.gitlab.io/self-driving-lab/instruments/chemspyd/) -->


[![GitLab issues open](https://img.shields.io/gitlab/issues/open/aspuru-guzik-group/self-driving-lab/instruments/chemspyd?label=Issues)](https://gitlab.com/aspuru-guzik-group/self-driving-lab/instruments/chemspyd/-/issues)
[![GitLab issues close](https://img.shields.io/gitlab/issues/closed/aspuru-guzik-group/self-driving-lab/instruments/chemspyd?label=Issues&color=green)](https://gitlab.com/aspuru-guzik-group/self-driving-lab/instruments/chemspyd/-/issues)


[![Release](https://gitlab.com/aspuru-guzik-group/self-driving-lab/instruments/chemspyd/-/badges/release.svg)](https://codecov.io/gh/aspuru-guzik-group/self-driving-lab/instruments/chemspyd)
[![PyPI - Version](https://img.shields.io/pypi/v/chemspyd)](https://pypi.org/project/chemspyd/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://gitlab.com/aspuru-guzik-group/self-driving-lab/instruments/chemspyd/-/blob/main/LICENSE)
[![Python Version](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
<!-- [![Code Style: black](https://img.shields.io/badge/Code%20Style-Black-000000.svg)](https://github.com/psf/black) -->

[![DOI](https://img.shields.io/badge/ChemRxiv-10.26434-gold)](https://doi.org/10.26434/chemrxiv-2024-33sfl)
<!-- [![DOI](https://img.shields.io/badge/DOI-123.4567-blue)](https://doi.org/10.26434/chemrxiv-2024-33sfl) -->


# Chemspyd
A Python API for the Chemspeed AutoSuite software.

## Installation

#### PyPI
```shell
$ pip install chemspyd
```

#### From source
Clone this repository, navigate to the directory where ```setup.py``` is located, and install the package using pip:
```shell
$ pip install .
```

### Manager app: installation & setup
- Copy ```Manager.app``` to the computer running the Chemspeed AutoSuite software.
- Create a folder on the Chemspeed computer where the commands will be sent.
- Perform necessary adaptations for your system. This can be done automatically or manually.

#### Automatic setup
```python
from chemspyd.autosuite import get_config, clean_config

get_config(
    output_json="path/to/elements_config.json",  # Choose appropriate location for the config files.
    manager_path="path/to/Manager.app",
)

clean_config(
    config_path="path/to/elements_config.json",
    spe_specs={"default": "SPE_D", "waste": "SPE_W"},  # Only necessary if you have a SPE rack.
    inject_specs={"default": "INJECT_I", "load": "INJECT_L"},  # Only necessary if you have an HPLC injection port.
)
```

#### Manual setup
Write the configuration JSON files manually to match your Chemspeed's configuration. Follow the examples in the [```configuration```](https://gitlab.com/aspuru-guzik-group/self-driving-lab/instruments/chemspyd/-/tree/main/configuration) directory for examples of proper syntax and structure.


Further instructions can be found in the [Installation](https://aspuru-guzik-group.gitlab.io/self-driving-lab/instruments/chemspyd/intro/install.html) section of the package documentation.


## Usage
- Execute the manager app on the computer running the Chemspeed AutoSuite software.
- Import the ```chemspyd``` package in your Python script.
- Specify the path to the commands folder using e.g. ```pathlib```.
- Instantiate a ```chemspyd.ChemspeedController``` object with the path to the commands folder as an argument.
- ```simulation``` is a boolean argument that determines whether the commands are sent to the Chemspeed AutoSuite software or not. If it's false, commands will simply be printed to the console.

#### Example
```python
from pathlib import Path

from chemspyd import Controller

# Instantiate controller
target = r"\\Chemspeed_PC\Users\Operator\Commands"
configuration: Path = Path(__file__).parent / "configuration"
elements: Path = configuration / "element_config.json"
sys_liquids: Path = configuration / "system_liquids.json"
statuses: Path = configuration / "statuses.json"
chmspd = Controller(
    cmd_folder=target,
    element_config=elements,
    system_liquids=sys_liquids,
    statuses=statuses,
    verbosity=2,
    simulation=False,
)

# Transfer liquid
chmspd.transfer_liquid("RACKL:1","RACKR:1",5,1)
```

Further examples can be found in the [```demos```](https://gitlab.com/aspuru-guzik-group/self-driving-lab/instruments/chemspyd/-/tree/main/demos) directory.

## Features
Chemspyd provides a Python interface for the Chemspeed AutoSuite software that enables modular, dynamic control of Chemspeed operations. It currently allows for the following operations:

**Basic**
- Liquid transfer
- Solid transfer
- ISYNTH drawer control
- Temperature & atmosphere (ambient, vacuum, inert) control
- Stir
- Vial transport
- Measure level
- Read status
- Unmount
- Wait

**Routines**
- Prime pumps
- Inject to HPLC port
- Carry out Schlenk cycles
- Reflux
- Filter
- Set all ISYNTH drawers at once

**Advanced**
- Automatic configuration upon installation
- Track volume of liquid in wells by addition and removal
- Track amount of solid added to or removed from wells
*NOTE*: These are experimental features, and are not guaranteed to be robust.

### Contributing
We welcome contributions from the community! If there are additional features that you would like to see added, please open an issue or a merge request, and suggest an implementation.

# Acknowledgments
The following people are acknowledged for assisting in the development of Chemspyd and its functionality in various ways:
- Martin Seifrid ([@mseifrid](https://github.com/mseifrid))
- Felix Strieth-Kalthoff ([@felix-s-k](https://github.com/felix-s-k))
- Mohammad Haddadnia ([@mohaddadnia](https://github.com/Mohaddadnia))
- Tony C. Wu ([@verysure](https://github.com/verysure))
- Emre Alca ([@alcaemre](https://github.com/alcaemre))


# Cite this work
```
@article{
    Seifrid_2024,
    shorttitle={Chemspyd},
    title={Chemspyd: An Open-Source Python Interface for Chemspeed Robotic Chemistry and Materials Platforms},
    DOI={10.26434/chemrxiv-2024-33sfl},
    journal={ChemRxiv},
    author={Seifrid, Martin and Strieth-Kalthoff, Felix and Haddadnia, Mohammad and Wu, Tony and Alca, Emre and Bodo, Leticia and Arellano-Rubach, Sebastian and Yoshikawa, Naruki and Skreta, Marta and Keunen, Rachel and Aspuru-Guzik, Al{\'a}n},
    year={2024}
}
```