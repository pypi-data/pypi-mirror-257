from typing import Callable, Dict

from scipy.constants import convert_temperature
from scipy.constants import (
    # SI Units
    kilo, milli,
    micro, nano, pico,
    # Time
    minute, hour, day,
    # Pressure
    atm, bar, mmHg, psi,
    # Mass
    gram,
)


class UnitConverter:
    def __init__(self) -> None:
        """
        Constructor for a unit converter, sets up a factory pattern for matching the variable types to convert with
        the corresponding converter methods.
        """
        self.converter_factory: Dict[str, Callable[[float, str, str, int], float]] = {
            "temperature": self._convert_temperature,
            "pressure": self._convert_pressure,
            "mass": self._convert_mass,
            "time": self._convert_time,
            "float": self._no_conversion,
        }

        self.units: Dict[str, Dict[str, float]] = {
            "si": {
                "1": 1.0,  # this is for when there is no prefix
                "kilo": kilo,
                "milli": milli,
                "micro": micro,
                "nano": nano,
                "pico": pico,
                "k": kilo,
                "m": milli,
                "μ": micro,
                "n": nano,
                "p": pico,
            },
            "pressure": {
                "Pa": 1.0,
                "atm": atm,
                "atmosphere": atm,
                "bar": bar,
                "torr": mmHg,
                "mmHg": mmHg,
                "psi": psi,
            },
            "mass": {
                "gram": gram,
                "g": gram,
            },
            "time": {
                "second": 1.0,
                "minute": minute,
                "hour": hour,
                "day": day,
                "sec": 1.0,
                "min": minute,
                "d": day,
                "s": 1.0,
                "m": minute,
                "h": hour,
                "d": day
            },
        }

    def __call__(
        self,
        parameter_type: str,
        value: float,
        source_unit: str,
        target_unit: str,
        precision: int = 1,
    ) -> float:
        """
        Uses the converter factory pattern to call the converter function depending on the parameter type.

        Args:
            parameter_type: Name of the parameter type.
            value: Value of the parameter to convert.
            source_unit: Name of the source unit.
            target_unit: Name of the target unit.

        Returns:
            float: Converted value
        """
        return self.converter_factory[parameter_type](
            value, source_unit, target_unit, precision
        )

    @staticmethod
    def _convert_temperature(
        value: float, source_unit: str, target_unit: str, precision: int = 1
    ) -> float:
        """
        Converts temperatures using scipy's convert_temperature method.

        Args:
            value: Temperature value to convert
            source_unit: Name of the source unit (e.g. K, C, F)
            target_unit: Name of the target unit
            precision: Number of digits after the comma

        Returns:
            float: Converted temperature, rounded.
        """
        return round(
            float(convert_temperature(value, source_unit, target_unit)), precision
        )

    def _convert_time(
        self, value: float, source_unit: str, target_unit: str, precision: int = 1
    ) -> float:
        """
        Converts times using scipy's internal constants

        Args:
            value: Time value to convert
            source_unit: Name of the source unit (e.g. second, minute, hour, milli, micro, ...)
            target_unit: Name of the target unit
            precision: Number of digits after the comma

        Returns:
            float: Converted time, rounded.
        """
        _source_unit = ("1", source_unit)
        _target_unit = ("1", target_unit)

        for prefix in self.units["si"].keys():
            if prefix in ["1", "m"]:
                continue
            if _source_unit[1].startswith(prefix):
                _source_unit = (prefix, _source_unit[1].replace(prefix, ""))

            if _target_unit[1].startswith(prefix):
                _target_unit = (prefix, _target_unit[1].replace(prefix, ""))

        source_unit_value = self.units["time"][_source_unit[1]] * self.units["si"][_source_unit[0]]
        target_unit_value = self.units["time"][_target_unit[1]] * self.units["si"][_target_unit[0]]

        return round(value * (source_unit_value) / (target_unit_value), precision)

    def _convert_mass(
        self, value: float, source_unit: str, target_unit: str, precision: int = 2
    ) -> float:
        """
        Converts masses using scipy's internal constants

        Args:
            value: Time value to convert
            source_unit: Name of the source unit (e.g. milli, micro, kilo)
            target_unit: Name of the target unit
            precision: Number of digits after the comma.

        Returns:
            float: Converted mass, rounded
        """
        _source_unit = ("1", source_unit)
        _target_unit = ("1", target_unit)

        for prefix in self.units["si"].keys():
            if prefix == "1":
                continue
            if _source_unit[1].startswith(prefix):
                _source_unit = (prefix, _source_unit[1].replace(prefix, ""))

            if _target_unit[1].startswith(prefix):
                _target_unit = (prefix, _target_unit[1].replace(prefix, ""))

        source_unit_value = self.units["mass"][_source_unit[1]] * self.units["si"][_source_unit[0]]
        target_unit_value = self.units["mass"][_target_unit[1]] * self.units["si"][_target_unit[0]]

        return round(value * (source_unit_value) / (target_unit_value), precision)

    def _convert_pressure(
        self, value: float, source_unit: str, target_unit: str, precision: int = 2
    ) -> float:
        """
        Converts pressures using scipy's internal constants

        Args:
            value: Pressure value to convert
            source_unit: Name of the source unit (e.g. Pa, mbar, milli, micro, kilo)
            target_unit: Name of the target unit
            precision: Number of digits after the comma.

        Returns:
            float: Converted mass, rounded
        """
        _source_unit = ("1", source_unit)
        _target_unit = ("1", target_unit)

        for prefix in self.units["si"].keys():
            if prefix == "1":
                continue
            if _source_unit[1].startswith(prefix) and _source_unit[1] not in ["mmHg", "psi"]:
                _source_unit = (prefix, _source_unit[1].replace(prefix, ""))

            if _target_unit[1].startswith(prefix) and _target_unit[1] not in ["mmHg", "psi"]:
                _target_unit = (prefix, _target_unit[1].replace(prefix, ""))

        source_unit_value = self.units["pressure"][_source_unit[1]] * self.units["si"][_source_unit[0]]
        target_unit_value = self.units["pressure"][_target_unit[1]] * self.units["si"][_target_unit[0]]

        return round(value * (source_unit_value) / (target_unit_value), precision)

    @staticmethod
    def _no_conversion(value: float, source_unit: str, target_unit: str, precision: int) -> float:
        """
        Leave value unchanged. Here to allow convenient mapping of values to converter functions.

        Args:
            value: Value to return unchanged.
            kwargs: Unused, only for similar API across all converter functions.

        Returns:
            float: Unchanged value
        """
        return round(value, precision)
