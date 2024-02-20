import random
from typing import Dict, List, Optional, Tuple, Union

from chemspyd.utils.precision import decimal_precision


class CapacityError(Exception):
    pass


class UnavailableError(Exception):
    pass


class Vial:
    @decimal_precision
    def __init__(
        self,
        min_volume: float,
        max_volume: float,
        current_volume: Optional[float] = None,
    ) -> None:
        """

        Args:
            min_volume: Minimum volume of the vial
            max_volume: Maximum volume of the vial
            current_volume: Current volume of the vial
        """
        self.min_volume: float = min_volume
        self.max_volume: float = max_volume
        # Case for balance vial
        if current_volume is None:
            self.current_volume: float = min_volume
        else:
            self.current_volume: float = current_volume  # type: ignore [no-redef]

    @property
    @decimal_precision
    def usable_volume(self) -> float:
        """Volume of the vial that can be used to remove liquid."""
        return self.current_volume - self.min_volume

    @property
    @decimal_precision
    def capacity(self) -> float:
        """Volume of the vial that can be used to add liquid."""
        return self.max_volume - self.current_volume

    @decimal_precision
    def available(self, volume_to_check: float) -> bool:
        """
        Check if the vial has enough capacity to hold the volume to check.

        Args:
            volume_to_check: Volume to check
        """
        return (
            self.min_volume <= self.current_volume + volume_to_check <= self.max_volume
        )

    @decimal_precision
    def add(self, volume_added: float) -> float:
        """
        Add volume to the vial.

        Args:
            volume_added: Volume to add
        """
        self.current_volume += volume_added
        return volume_added

    @decimal_precision
    def remove(self, volume_removed: float) -> float:
        self.current_volume -= volume_removed
        return volume_removed


class WellUnion:
    def __init__(
        self,
        source_wells: List[str],
        min_volume: float,
        max_volume: float,
        init_volume: float,
        randomize: bool = True,
    ) -> None:
        """

        Args:
            source_wells: List of well names to be used as source wells
            min_volume: Minimum volume of each well
            max_volume: Maximum volume of each well
            randomize: Whether to randomize the choice of source wells. Defaults to True.
        """
        # TODO: How to access the underlying Well objects?
        unsorted_wells: Dict[str, Vial] = {
            well: Vial(min_volume, max_volume, current_volume=init_volume)
            for well in source_wells
        }
        self.vials: Dict[str, Vial] = dict(sorted(unsorted_wells.items()))
        self.randomize: bool = randomize

    @property
    @decimal_precision
    def total_capacity(self) -> float:
        return float(sum([v.capacity for v in self.vials.values()]))

    @property
    @decimal_precision
    def total_usable(self) -> float:
        return float(sum([v.usable_volume for v in self.vials.values()]))

    @decimal_precision
    def possible_transfers(self, volume: float) -> int:
        return sum([int(v.usable_volume // volume) for v in self.vials.values()])

    @decimal_precision
    def get_available_vials(self, volume: float) -> List[str]:
        return [vial for vial in self.vials if self.vials[vial].available(volume)]

    @decimal_precision
    def get_vial(self, volume: float) -> Union[str, List[str]]:
        """
        Raises IndexError if no available wells.

        Args:
            volume: Volume to be transferred. Positive for adding, negative for removing.

        Returns:
            Location of the vial to be used.
        """
        try:
            if self.randomize:
                vial: str = random.choice(self.get_available_vials(volume))
            else:
                vial: str = self.get_available_vials(volume)[0]  # type: ignore [no-redef]

        except IndexError:
            raise UnavailableError("No available wells!")

        self.vials[vial].add(volume)
        return vial

    @decimal_precision
    def add_to_all(self, volume: float) -> List[str]:
        """
        Raises IndexError if no available wells.

        Args:
            volume: Volume to be added.

        Returns:
            List of locations of the vials to be used.
        """
        try:
            vials: List[str] = self.get_available_vials(volume)
        except IndexError:
            raise UnavailableError("No available wells!")

        for vial in vials:
            self.vials[vial].add(volume)

        return vials

    @decimal_precision
    def get_max_capacity(self) -> Tuple[str, float]:
        max_vial: str = max(self.vials, key=lambda x: self.vials[x].capacity)  # type: ignore [no-any-return]
        max_capacity: float = self.vials[max_vial].capacity
        wells: List[str] = [
            k for k, v in self.vials.items() if v.capacity == max_capacity
        ]

        if self.randomize:
            well: str = random.choice(wells)
        else:
            well: str = wells[0]  # type: ignore [no-redef]

        capacity: float = self.vials[well].capacity
        if capacity == 0:
            raise CapacityError("No available wells!")
        return well, capacity
