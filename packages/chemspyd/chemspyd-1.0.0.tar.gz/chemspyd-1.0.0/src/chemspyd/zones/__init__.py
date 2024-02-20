from typing import List, Union

from chemspyd.zones.chemspeed_element import ChemspeedElement
from chemspyd.zones.chemspeed_well import Well
from chemspyd.zones.well_group import WellGroup
from chemspyd.zones.zone_utils import initialize_zones

# Definition of Zone type to unify string and well definition of zones (might be deprecated in the future)
Zone = Union[str, Well, List[str], List[Well]]

__all__ = ["ChemspeedElement", "WellGroup", "Well", "initialize_zones", "Zone"]
