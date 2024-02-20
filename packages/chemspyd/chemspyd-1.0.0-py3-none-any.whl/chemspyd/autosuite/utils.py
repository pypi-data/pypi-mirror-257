from typing import Union, List, Dict, Any
from functools import wraps

import json
import platform
from pathlib import Path
from configparser import ConfigParser

from chemspyd.utils import load_json
from chemspyd.exceptions import ChemspydAutosuiteError, ChemspydAutosuiteVBScriptError


def vbscript(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("*** Running VBScript ***")
        func(*args, **kwargs)
        print("*** Completed VBScript ***")
    return wrapper


def _get_drive() -> str:
    """ Gets the home drive."""
    return Path.home().drive


def get_cscript() -> str:
    """ Returns the path of the 32-bit `cscript`"""
    if platform.machine().endswith("64"):
        return f"{_get_drive()}\\windows\\syswow64\\cscript.exe"
    else:
        return "cscript.exe"


def verify_config(config_path: Union[str, Path]) -> None:
    """ Verifies the given config file to make sure all the required sections and keys are present."""

    if not isinstance(config_path, Path):
        config_path = Path(config_path)

    if not config_path.is_file():
        raise ChemspydAutosuiteError(
            f"config file does not exist: {config_path}"
        )

    config = ConfigParser()
    config.read(config_path)

    _REQUIRED_SECTIONS = [
        'element_names', 'addable_liquid', 'removable_liquid',
        'addable_solid', 'removable_solid',
        'thermostat', 'thermostat.temperature', 'thermostat.ramp',
        'stir', 'stir.rate', 'reflux', 'reflux.temperature',
        'vacuum_pump', 'vacuum_pump.pressure', 'drawer', 'environment'
    ]
    _REQUIRED_KEYS = ["elements", "true_value", "false_value"]
    _REQUIRED_SUB_KEYS = ["true_value", "false_value"]

    _missing_sections = []
    for section in _REQUIRED_SECTIONS:
        if section not in list(config.keys()):
            _missing_sections.append(section)
        else:
            if section == "element_names":
                pass
            else:
                _missing_keys = []
                required_keys = _REQUIRED_SUB_KEYS if "." in section else _REQUIRED_KEYS
                for k in required_keys:
                    if k not in config[section].keys():
                        _missing_keys.append(k)
                if _missing_keys:
                    raise ChemspydAutosuiteError(
                        f"config file section [{section}] is missing the following key(s): {', '.join(_missing_keys)}"
                    )

    if _missing_sections:
        raise ChemspydAutosuiteError(
            f"config file is missing the following section(s): {', '.join(_missing_sections)}"
        )


def check_error(vbscript_output: str) -> None:
    lines = vbscript_output.split("\n")
    error_lines = [line.strip("\r").split(": ")[1] for line in lines if "ERROR4Py" in line]

    if error_lines:
        raise ChemspydAutosuiteVBScriptError(error_lines[0])


def _get_name_overlap(names: List[str]) -> str:

    if len(names) == 1:
        return names[0]

    shortest = min([len(n) for n in names])
    overlap = ""

    for i in range(shortest):
        char = names[0][i]
        for n in names[1:]:
            if n[i] != char:
                break
        else:
            overlap += char

    return overlap


def clean_config(config_path: Union[str, Path], spe_specs: Dict[str, str], inject_specs: Dict[str, str]) -> None:

    config_path = Path(config_path)
    config: Dict[str, Dict[str, Any]] = load_json(config_path)

    spe_dicts, inject_dicts = {}, {}
    # merge SPE sections
    for k, d in config.items():
        if d["debugging"]["type"] == 120:  # find SPE
            spe_dicts[k] = d

        if d["debugging"]["type"] == 63:  # find INJECT
            inject_dicts[k] = d

    for k in [*list(spe_dicts.keys()), *list(inject_dicts.keys())]:
        config.pop(k)

    spe_new_name = _get_name_overlap(list(spe_dicts.keys())).strip("_")
    config[spe_new_name] = list(spe_dicts.values())[0]
    config[spe_new_name]["states"] = spe_specs

    inject_new_name = _get_name_overlap(list(inject_dicts.keys())).strip("_")
    config[inject_new_name] = list(inject_dicts.values())[0]
    config[inject_new_name]["states"] = inject_specs

    with open(config_path, "w+") as json_file:
        json.dump(config, json_file, indent=4)
