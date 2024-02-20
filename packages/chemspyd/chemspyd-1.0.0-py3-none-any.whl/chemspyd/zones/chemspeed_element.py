from __future__ import annotations
from logging import Logger
from typing import Optional, Union, List, Dict

from chemspyd.exceptions import (
    ChemspydElementError,
    ChemspydPropertyError,
    ChemspydRangeError,
)


class ChemspeedElement:
    """
    Class for describing an element of the Chemspeed (e.g. ISynth, Filtration Rack, Vial Rack, ...) as a Python object.
    For consistent naming of wells, each element must be represented as a single zone in the Manager app.
    """

    _required_keys: set[str] = {
        "no_wells",
        "max_volume",
        "default_quantity",
        "addable_liquid",
        "removable_liquid",
        "addable_solid",
        "removable_solid",
        "thermostat",
        "stir",
        "reflux",
        "vacuum_pump",
        "drawer",
        "environment",
        "states",
    }

    def __init__(
        self, name: str, properties: dict, logger: Optional[Logger] = None
    ) -> None:
        """
        Instantiates the ChemspeedElement object by setting all properties as attributes.

        Args:
            name: Name of the element (must match the zone name in the Manager app).
            properties: Dictionary of all specific properties of the element. Must contain the keys specified in the
                        class variable _required_keys.
            logger (optional): Logger object

        Raises:
            ChemspeedConfigurationError: if any of the required keys are missing.
        """
        self.logger: Optional[Logger] = logger
        self.name = name

        if not self._required_keys.issubset(properties):
            raise ChemspydPropertyError(
                f"Configuration of {name} failed. "
                f"Missing keys {self._required_keys - properties.keys()} for element {name}.",
                logger=self.logger,
            )

        for key in properties:
            setattr(self, key, properties[key])

    def __str__(self) -> str:
        return self.name

    def __eq__(self, other: object):
        if not isinstance(other, ChemspeedElement):
            raise NotImplementedError(f"cannot perform __eq__ between ChemspeedElement and {type(other)}")
        else:
            for prop in self._required_keys:
                if getattr(self, prop) != getattr(other, prop):
                    return False
            return True

    def validate_parameter(
        self, parameter_name: str, parameter_value: Union[int, float, str, bool]
    ) -> None:
        """
        Validates a specific setting / target status (e.g. temperature, stir rate, ...) that the element should be
        set to.

        Args:
            parameter_name: Key of the parameter (must be in self._required_keys).
            parameter_value: Value of the parameter.

        Raises:
            ChemspeedValueError: If the parameter value is not within the specified boundaries.
            ChemspeedConfigurationError: If the parameter cannot be set for the given element.
        """
        validation_methods: dict = {
            str: self._validate_discrete_parameter,
            bool: self._validate_discrete_parameter,
            int: self._validate_continuous_parameter,
            float: self._validate_continuous_parameter,
        }

        try:
            validation_methods[type(parameter_value)](parameter_name, parameter_value)

        except (KeyError, AttributeError, TypeError):
            raise ChemspydElementError(
                f"The parameter {parameter_name} cannot be set for {self.name}",
                logger=self.logger,
            )

    def _validate_continuous_parameter(
        self, parameter_name: str, parameter_value: Union[int, float]
    ) -> None:
        """
        Validates if a continuous parameter is in the specified boundaries,
        given as [lower, upper] in the configuration.

        Args:
            parameter_name: Key of the parameter
            parameter_value: Value of the parameter.
        """
        boundaries: list = getattr(self, parameter_name)

        if not boundaries[0] <= parameter_value <= boundaries[1]:
            raise ChemspydRangeError(
                f"The set value of {parameter_name} ({parameter_value}) exceeds the limit of {self.name}.",
                logger=self.logger,
            )

    def _validate_discrete_parameter(
        self, parameter_name: str, parameter_value: Union[str, bool]
    ) -> None:
        """
        Validates if a discrete parameter is in the specified set of options.

        Args:
            parameter_name: Key of the parameter
            parameter_value: Value of the parameter.
        """
        options: list = getattr(self, parameter_name)

        if parameter_value not in options:
            raise ChemspydRangeError(
                f"The set value of {parameter_name} ({parameter_value}) is not a feasible option for {self.name}.",
                logger=self.logger,
            )

    @property
    def no_wells(self) -> int:
        """ Number of wells in the element."""
        return self._no_wells

    @no_wells.setter
    def no_wells(self, value: int) -> None:
        self._no_wells = value

    @property
    def max_volume(self) -> float:
        """ Maximum volume of the element."""
        return self._max_volume

    @max_volume.setter
    def max_volume(self, value: float) -> None:
        self._max_volume = value

    @property
    def default_quantity(self) -> float:
        """ Default quantity of the element."""
        return self._default_quantity

    @default_quantity.setter
    def default_quantity(self, value: float) -> None:
        self._default_quantity = value

    @property
    def addable_liquid(self) -> bool:
        """ Whether liquid can be added to the element."""
        return self._addable_liquid

    @addable_liquid.setter
    def addable_liquid(self, value: bool) -> None:
        self._addable_liquid = value

    @property
    def removable_liquid(self) -> bool:
        """ Whether liquid can be removed from the element."""
        return self._removable_liquid

    @removable_liquid.setter
    def removable_liquid(self, value: bool) -> None:
        self._removable_liquid = value

    @property
    def addable_solid(self) -> bool:
        """ Whether solid can be added to the element."""
        return self._addable_solid

    @addable_solid.setter
    def addable_solid(self, value: bool) -> None:
        self._addable_solid = value

    @property
    def removable_solid(self) -> bool:
        """ Whether solid can be removed from the element."""
        return self._removable_solid

    @removable_solid.setter
    def removable_solid(self, value: bool) -> None:
        self._removable_solid = value

    @property
    def thermostat(self) -> Optional[List[str]]:
        """ Thermostat config of the element."""
        return self._thermostat

    @thermostat.setter
    def thermostat(self, value: Optional[List[str]]) -> None:
        self._thermostat = value

    @property
    def stir(self) -> Optional[List[str]]:
        """ stir config of the element."""
        return self._stir

    @stir.setter
    def stir(self, value: Optional[List[str]]) -> None:
        self._stir = value

    @property
    def reflux(self) -> Optional[List[str]]:
        """ reflux config of the element."""
        return self._reflux

    @reflux.setter
    def reflux(self, value: Optional[List[str]]) -> None:
        self._reflux = value

    @property
    def vacuum_pump(self) -> Optional[List[str]]:
        """ vacuum pump config of the element."""
        return self._vacuum_pump

    @vacuum_pump.setter
    def vacuum_pump(self, value: Optional[List[str]]) -> None:
        self._vacuum_pump = value

    @property
    def drawer(self) -> Optional[List[str]]:
        """ drawer config of the element."""
        return self._drawer

    @drawer.setter
    def drawer(self, value: Optional[List[str]]) -> None:
        self._drawer = value

    @property
    def environment(self) -> Optional[List[str]]:
        """ environment config of the element."""
        return self._env

    @environment.setter
    def environment(self, value: Optional[List[str]]) -> None:
        self._env = value

    @property
    def states(self) -> Dict[str, str]:
        """ states of the element."""
        return self._states

    @states.setter
    def states(self, value: Dict[str, str]) -> None:
        self._states = value
