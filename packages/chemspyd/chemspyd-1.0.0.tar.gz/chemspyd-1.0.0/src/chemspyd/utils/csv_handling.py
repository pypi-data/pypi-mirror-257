from pathlib import Path
from typing import Union, Literal, overload


@overload
def read_csv(file_name: Union[str, Path], single_line: Literal[True], delimiter: str = ",") -> list[str]: ...


@overload
def read_csv(file_name: Union[str, Path], single_line: Literal[False], delimiter: str = ",") -> list[list[str]]: ...


def read_csv(
    file_name: Union[str, Path], single_line: bool = False, delimiter: str = ","
) -> Union[list[str], list[list[str]]]:
    """
    Reads in a csv file and returns each line as a list of entries.

    Args:
        file_name: Path to the csv file
        single_line: True if only a single line from the file should be read. Else returns a list of lists.
        delimiter: CSV column delimiter.

    Returns:
         List or List[List]: Each line as a list of entries.
    """
    with open(file_name, "r") as input_file:
        lines: list[str] = input_file.readlines()

    if not lines:
        lines = [""]  # in case the file is empty

    if single_line:
        return lines[0].strip().split(sep=delimiter)
    else:
        return [line.strip().split(sep=delimiter) for line in lines]


def write_csv(
    lines: list[Union[str, list[str]]],
    file_name: Union[str, Path],
    single_line: bool = False,
    delimiter: str = ",",
) -> None:
    """
    Writes a list of rows into a csv file.

    Args:
        lines: List[list] of rows (each row as a list). If single_line is given, lines is a simple list.
        file_name: Path to the csv file
        single_line: True if only a single line should be written to the file.
        delimiter: CSV column delimiter.
    """
    if single_line:
        lines = [lines]  # type: ignore[no-redef, list-item]

    with open(file_name, "w") as output_file:
        for line in lines:
            line = [str(entry) for entry in line]
            output_file.write(f"{delimiter.join(line)}\n")
