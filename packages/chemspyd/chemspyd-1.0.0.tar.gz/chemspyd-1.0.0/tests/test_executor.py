from pathlib import Path

from chemspyd.executor import ChemspeedExecutor
from chemspyd.utils.logging_utils import get_logger
from .utils import autosuite_assertion, commands_handling


@commands_handling
def test_idle(tmpdir: Path):
    executor = ChemspeedExecutor(cmd_folder=tmpdir, logger=get_logger(False))
    response_file = tmpdir / "response.csv"

    response_file.write_text("1")
    assert executor.idle is True

    response_file.write_text("0")
    assert executor.idle is False


@commands_handling
def test_newcmd(tmpdir: Path):
    executor = ChemspeedExecutor(cmd_folder=tmpdir, logger=get_logger(False))
    command_file = tmpdir / "command.csv"

    command_file.write_text("1")
    assert executor.newcmd is True

    command_file.write_text("0")
    assert executor.newcmd is False


@commands_handling
def test_blocked(tmpdir: Path):
    executor = ChemspeedExecutor(cmd_folder=tmpdir, logger=get_logger(False))
    response_file = tmpdir / "response.csv"
    command_file = tmpdir / "command.csv"

    response_file.write_text("1")
    command_file.write_text("1")
    assert executor.blocked is True

    response_file.write_text("0")
    command_file.write_text("0")
    assert executor.blocked is True

    response_file.write_text("0")
    command_file.write_text("1")
    assert executor.blocked is True

    response_file.write_text("1")
    command_file.write_text("0")
    assert executor.blocked is False


@commands_handling
def test_return_data(tmpdir: Path):
    executor = ChemspeedExecutor(cmd_folder=tmpdir, logger=get_logger(False))
    return_file = tmpdir / "return.csv"

    return_file.write_text("ReturnData,end")
    assert executor.return_data == ["ReturnData"]


@commands_handling
def test_status(tmpdir: Path):
    executor = ChemspeedExecutor(cmd_folder=tmpdir, logger=get_logger(False))
    status_file = tmpdir / "status.csv"

    status_file.write_text("Status")
    assert executor.status == ["Status"]


@autosuite_assertion
def test_execute(tmpdir: Path):
    executor = ChemspeedExecutor(cmd_folder=tmpdir, logger=get_logger(False))

    cmd = "placeholder_command"
    kwargs = {"k1": {"value": "v1", "unit": "u1"}, "k2": {"value": "v2", "unit": "u2"}}

    executor.execute(
        command=cmd,
        **kwargs,
    )

    expected_values = ",".join([str(kwargs[kwarg]["value"]) for kwarg in kwargs]) + ",end"

    return cmd, expected_values
