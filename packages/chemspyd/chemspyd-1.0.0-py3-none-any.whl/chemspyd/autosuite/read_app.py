from typing import Union

import subprocess
from pathlib import Path

from chemspyd.autosuite.utils import (
    vbscript, get_cscript,
    check_error, verify_config
)

HERE = Path(__file__).resolve().parent
vbs_path = HERE / "read_app.vbs"
utils_path = HERE / "utils.vbs"
default_config_path = HERE / "config.ini"


@vbscript
def get_config(
    output_json: Path,
    manager_path: Path,
    config_path: Union[str, Path] = "default",
    show_output: bool = False
) -> None:
    """ Writes the element config from the given manager app."""

    if config_path == "default":
        config_path = default_config_path
    else:
        config_path = Path(config_path)

    verify_config(config_path)

    cmd = [
        get_cscript(), f'"{vbs_path}"',
        f'/manager:"{manager_path}"',
        f'/json:"{output_json}"',
        f'/utils:"{utils_path}"',
        f'/config:"{config_path}"',
    ]
    # print(" ".join(cmd))

    vbs_output = subprocess.check_output(" ".join(cmd)).decode("utf-8")
    check_error(vbs_output)

    if show_output:
        print(vbs_output)
