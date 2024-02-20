import time
from typing import List, Union

from chemspyd import Controller
from chemspyd.exceptions import ChemspydZoneError
from chemspyd.utils import UnitConverter
from chemspyd.zones import WellGroup, Zone


def prime_pumps(chmspd: Controller, pump: int, volume: Union[int, float]) -> None:
    """
    Primes the ChemSpeed pumps.

    Args:
        chmspd: Chemspeed controller object
        pump: pump being primed
        volume: volume with which to prime pumps

    Returns:
        None
    """
    try:
        src = str(chmspd.system_liquids[str(pump)]["liquid_zone"])
        dst = str(chmspd.system_liquids[str(pump)]["waste_zone"])
    except KeyError:
        raise ChemspydZoneError("The specified zone does not exist.")

    chmspd.transfer_liquid(
        source=src,
        destination=dst,
        needle=pump,
        volume=volume,
        src_flow=20.0,
        dst_flow=40.0,
        rinse_volume=0.0,
    )


def inject_to_hplc(
    chmspd: Controller,
    source: Zone,
    destination: Zone,
    volume: float,
    needle: int,
    src_flow: float = 10,
    src_bu: bool = True,
    src_distance: float = 3,
    dst_flow: float = 0.5,
    equib_dst: float = 30,
    rinse_volume: float = 2,
    rinse_after_valve_switch: bool = True,
) -> None:
    """
    Inject liquid to the injection ports. This will use volume + 0.1ml of liquid.

    Args:
        chmspd: Controller object
        source (Zone): Zone for transfer source
        destination (Zone): Injection zone
        volume: volume to transfer (mL)
        needle: Number of the needle to be used for injection.
        src_flow: draw speed at source (mL/min)
        src_bu: True if liquid should be drawn bottom-up at the source.
        src_distance: Needle bottom-up / top-down distance at source (mm)
        dst_flow: Dispense speed at destination (mL/min)
        equib_dst: Equilibration time at destination (sec)
        rinse_volume: needle rinsing volume after action (mL)
        rinse_after_valve_switch: True if needle should only be rinsed after switching the HPLC valve.
    """
    # source = WellGroup(source, well_configuration=chmspd.wells)
    # destination = WellGroup(destination, well_configuration=chmspd.wells, state="load")  # ATTN: What is load?

    if rinse_after_valve_switch:
        rinse_volume_init: float = 0.0  # type: ignore[no-redef]
    else:
        rinse_volume_init: float = rinse_volume  # type: ignore[no-redef]

    chmspd.transfer_liquid(
        source=source,  # TODO: Add WellGroup to acceptable types?
        destination=destination,
        volume=volume,
        needle=needle,
        src_flow=src_flow,
        src_bu=src_bu,
        src_distance=src_distance,
        dst_flow=dst_flow,
        dst_bu=True,
        dst_distance=0.0,
        airgap=0.0,
        rinse_volume=rinse_volume_init,
        equib_dst=equib_dst,
    )

    if rinse_after_valve_switch:
        chmspd.transfer_liquid(
            source=str(chmspd.system_liquids[str(needle)][
                "liquid_zone"
            ]),  # BUG: If needle == 0, raises KeyError
            destination=str(chmspd.system_liquids[str(needle)]["waste_zone"]),
            volume=rinse_volume,
            needle=needle,
            rinse_volume=rinse_volume,
        )


def do_schlenk_cycles(
    chmspd: Controller,
    wells: Zone,
    evac_time: int = 60,
    backfill_time: int = 30,
    vacuum_pressure: float = 1,
    num_cycles: int = 3,
) -> None:
    """
    Performs Schlenk Cycles (evacuate-refill cycles) on the specified wells.
    Requires the wells to be in an element that supports vacuum/inert gas handling.

    ATTN: Might also influence neighboring wells (e.g. if they are in the same ISYNTH drawer).

    Args:
        chmspd: Chemspeed controller object
        wells: Zones to be set to inert gas.
        evac_time: Time (in sec) for evacuation. Default: 60 sec.
        backfill_time: Time (in sec) for backfilling with inert gas. Default: 30 sec.
        vacuum_pressure: Pressure (in mbar) that should be targeted for evacuation. Default: 1 mbar (minimum).
        num_cycles: Number of Schlenk cycles. Default: 3.
    """
    for _ in range(num_cycles):
        # Evacuation
        chmspd.set_drawer(zone=wells, state="close", environment="vacuum")
        time.sleep(
            0.5
        )  # ATTN: Implemented because of random communication delays. Test if it is necessary.
        chmspd.set_vacuum(vac_zone=wells, state="on", vacuum=vacuum_pressure)
        chmspd.wait(evac_time)

        # Backfilling
        chmspd.set_drawer(zone=wells, state="close", environment="inert")
        time.sleep(
            0.5
        )  # ATTN: Implemented because of random communication delays. Test if it is necessary.
        chmspd.set_vacuum(vac_zone=wells, state="on", vacuum=1000)
        chmspd.wait(backfill_time)

    chmspd.set_vacuum(vac_zone="ISYNTH:1", state="off")
    chmspd.set_drawer(zone=wells, state="close", environment="none")


def heat_under_reflux(
    chmspd: Controller,
    wells: Zone,
    stir_rate: float,
    temperature: float,
    heating_hours: int,
    cooling_hours: int,
    condenser_temperature: float = 0,
    ramp: float = 0,
) -> None:
    """
    Sets up the heating and the reflux condenser for a specified time period.
    Cools the system back to room temperature for a specified cooling period.

    ATTN: Might also influence neighboring vials (e.g. it can only heat the entire element).
          Maybe this should be taken into account somehow.

    Args:
        chmspd: Controller object.
        wells: Wells to be heated under reflux.
        stir_rate: Stir rate (in rpm).
        temperature: Heating temperature (in °C)
        heating_hours: Heating time (in h).
        cooling_hours: Cooling time (in h).
        condenser_temperature: Temperature (in °C) of the reflux condenser.
        ramp: Ramping speed (in °C / min) for the cryostat.
    """
    chmspd.set_reflux(wells, state="on", temperature=condenser_temperature)
    chmspd.set_temperature(wells, state="on", temperature=temperature, ramp=ramp)
    chmspd.set_stir(wells, state="on", rpm=stir_rate)
    chmspd.wait(UnitConverter()("time", heating_hours, "hour", "second"))
    chmspd.set_temperature(wells, state="on", temperature=20, ramp=ramp)
    chmspd.wait(UnitConverter()("time", cooling_hours, "hour", "second"))
    chmspd.set_temperature(wells, state="off")
    chmspd.set_reflux(wells, state="off")
    chmspd.set_stir(wells, state="off")


def filter_liquid(
    chmspd: Controller,
    source: Zone,
    needle: int,
    filtration_zone: Zone,
    filtration_volume: float,
    collect_filtrate: bool = True,
    wash_liquid: Zone = "",
    wash_volume: float = 0,
    collect_wash: bool = False,
    eluent: Zone = "",
    eluent_volume: float = 0,
) -> None:
    """
    Filters a liquid sample on a filtration rack. Allows for collecting the filtrate, washing and eluting the filter.

    Args:
        chmspd: Controller object.
        source_well: Source well of the sample to be filtered.
        filtration_zone: Zone on the filtration rack to be used. All "sub-zones" (SPE_D, SPE_C, SPE_W can be used).
        filtration_volume: Volume (in mL) of liquid to be filtered.
        collect_filtrate: Whether to collect or dispose the filtrate
        wash_liquid: Source zone of the wash liquid.
        wash_volume: Volume (in mL) of wash liquid.
        collect_wash: Whether to collect or dispose the wash liquid.
        eluent: Source zone of the eluent.
        eluent_volume: Volume of eluent to be used.
    """
    _filtration_zone = WellGroup(filtration_zone, chmspd.wells)
    filtrate_state: str = "collect" if collect_filtrate else "waste"
    wash_state: str = "collect" if collect_wash else "waste"

    # Transfer liquid to filtration zone and collect or dispose the filtrate
    _filtration_zone.set_state(filtrate_state)
    chmspd.transfer_liquid(
        source=source,
        destination=_filtration_zone.well_list,
        volume=filtration_volume,
        needle=needle,
    )

    # Wash the filter and collect or dispose the wash liquid
    if wash_volume > 0:
        _filtration_zone.set_state(wash_state)
        chmspd.transfer_liquid(
            source=wash_liquid,
            destination=_filtration_zone.well_list,
            volume=wash_volume,
            needle=needle,
        )

    # Elute from the filter and collect the eluent.
    if eluent_volume > 0:
        _filtration_zone.set_state("collect")
        chmspd.transfer_liquid(
            source=eluent,
            destination=_filtration_zone.well_list,
            volume=eluent_volume,
            needle=needle,
        )


def set_isynth_drawers(
    chmspd: Controller,
    state: str,
    environment: str = "none",
) -> None:
    # BUG: This is only needed because we can't apply operations to entire elements.
    """
    Sets ALL the ISYNTH drawers to the specified state.

    Args:
        chmspd: Controller object.
        state: State to be set ("open" or "close").
        environment: Environment to be set ("vacuum", "inert" or "none").
    """
    isynth_drawers: List[str] = [
        "ISYNTH:1",
        "ISYNTH:9",
        "ISYNTH:17",
        "ISYNTH:25",
        "ISYNTH:33",
        "ISYNTH:41",
    ]
    for drawer in isynth_drawers:
        chmspd.set_drawer(zone=drawer, state=state, environment=environment)
        time.sleep(0.1)  # ATTN: Stupid fix for a communication latency bug...
