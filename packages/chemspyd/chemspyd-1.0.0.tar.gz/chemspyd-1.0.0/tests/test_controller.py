from typing import Tuple, List, Dict, Any

import pytest
import json
import logging
from pathlib import Path

from chemspyd import Controller
from chemspyd.executor import ChemspeedExecutor
from chemspyd.zones import WellGroup, initialize_zones

from .utils import autosuite_handling, autosuite_assertion

element_config = Path("configuration/element_config.json")
system_liquids = Path("configuration/system_liquids.json")
statuses = Path("configuration/statuses.json")


@autosuite_handling
def test_controller_initialization(tmpdir: Path):
    # Create test JSON files with minimal content
    logfile = tmpdir / "test.log"

    # Initialize the Controller
    controller = Controller(
        cmd_folder=tmpdir / "commands",
        element_config=element_config,
        system_liquids=system_liquids,
        statuses=statuses,
        stdout=False,
        logfile=logfile,
    )

    # Assert that the Controller and ChemspeedExecutor are properly initialized
    assert isinstance(controller, Controller)
    assert isinstance(controller.executor, ChemspeedExecutor)

    expected_elements, expected_wells = initialize_zones(json.loads(element_config.read_text()))

    # Assert that system_liquids, elements, and statuses are loaded correctly
    assert controller.system_liquids == json.loads(system_liquids.read_text())
    assert controller.elements == expected_elements
    assert controller.wells == expected_wells
    assert controller.statuses == json.loads(statuses.read_text())

    # Assert that the logger is properly configured
    assert controller.logger.handlers
    assert any(isinstance(handler, logging.FileHandler) for handler in controller.logger.handlers)


@pytest.mark.timeout(45.0)
@autosuite_assertion
def test_transfer_liquid(tmpdir: Path) -> Tuple[str, str]:
    source = "SOURCE:1"
    destination = "DEST:1"
    volume = 2.0
    needle = 0
    src_flow = 0.4
    src_bu = True
    src_distance = 3.0
    dst_flow = 40.0
    dst_bu = False
    dst_distance = 5.0
    rinse_volume = 2.0
    rinse_stn = 1
    airgap = 0.01
    post_airgap = 0.0
    airgap_dst = "WASTE1"
    extra_volume = 0.0
    extra_dst = "WASTE1"
    equib_src = 0.0
    equib_dst = 0.0
    multi_aspiration = False

    source = "ISYNTH:1"
    destination = "RACKL:1"
    volume = 2
    needle = 0
    src_flow = 0.4

    controller = Controller(
        cmd_folder=tmpdir,
        element_config=element_config,
        system_liquids=system_liquids,
        statuses=statuses,
        stdout=False,
        logfile=(tmpdir / "log.txt"),
        verbosity=0,
        simulation=False,
        track_quantities=False,
    )
    controller.transfer_liquid(
        source=source,
        destination=destination,
        volume=volume,
        needle=needle,
        src_flow=src_flow,
        src_bu=src_bu,
        src_distance=src_distance,
        dst_flow=dst_flow,
        dst_bu=dst_bu,
        dst_distance=dst_distance,
        rinse_volume=rinse_volume,
        rinse_stn=rinse_stn,
        airgap=airgap,
        post_airgap=post_airgap,
        airgap_dst=airgap_dst,
        extra_volume=extra_volume,
        extra_dst=extra_dst,
        equib_src=equib_src,
        equib_dst=equib_dst,
        multi_aspiration=multi_aspiration
    )

    source: WellGroup = WellGroup(
        source, well_configuration=controller.wells, logger=controller.logger
    )
    destination: WellGroup = WellGroup(
        destination, well_configuration=controller.wells, logger=controller.logger
    )
    airgap_dst: WellGroup = WellGroup(
        airgap_dst, well_configuration=controller.wells, logger=controller.logger
    )
    extra_dst: WellGroup = WellGroup(
        extra_dst, well_configuration=controller.wells, logger=controller.logger
    )

    expected_kwargs: Dict[str, Dict[str, Any]] = {
        "Source Zone": {"value": str(source), "unit": None},
        "Destination Zone": {"value": str(destination), "unit": None},
        "Volume": {"value": volume, "unit": "mL"},
        "Needle No.": {"value": needle, "unit": None},
        "Flow Rate (Source)": {"value": src_flow, "unit": "mL/min"},
        "Bottom-Up (Source)": {"value": int(src_bu), "unit": None},
        "Distance (Source)": {"value": src_distance, "unit": "mm"},
        "Flow Rate (Destination)": {"value": dst_flow, "unit": "mL/min"},
        "Bottom-Up (Destination)": {"value": int(dst_bu), "unit": None},
        "Distance (Destination)": {"value": dst_distance, "unit": "mm"},
        "Rinse Volume": {"value": rinse_volume, "unit": "mL"},
        "Rinse Station No.": {"value": rinse_stn, "unit": None},
        "Airgap Volume": {"value": airgap, "unit": "mL"},
        "Post-Airgap Volume": {"value": post_airgap, "unit": "mL"},
        "Airgap Destination": {"value": airgap_dst, "unit": None},
        "Extra Volume": {"value": extra_volume, "unit": "mL"},
        "Extra Volume Destination": {"value": extra_dst, "unit": None},
        "Equilib. Time (Source)": {"value": equib_src, "unit": "s"},
        "Equilib. Time (Destination)": {"value": equib_dst, "unit": "s"},
        "Multi. Aspiration Allowed": {
            "value": int(multi_aspiration),
            "unit": None,
        },
    }

    expected_command = "transfer_liquid"
    expected_values = ",".join([str(expected_kwargs[kwarg]["value"]) for kwarg in expected_kwargs]) + ",end"

    return expected_command, expected_values


@pytest.mark.timeout(45.0)
@autosuite_assertion
def test_inject_liquid(tmpdir: Path) -> Tuple[str, str]:
    source = "SOURCE:1"
    destination = "DEST:1"
    volume = 2.0
    needle = 0
    src_flow = 0.4
    src_bu = True
    src_distance = 3.0
    dst_flow = 40.0
    dst_bu = True
    dst_distance = 5.0
    rinse_volume = 2.0
    rinse_stn = 1
    airgap = 0.01
    post_airgap = 0.0
    airgap_dst = "WASTE1"
    extra_volume = 0.0
    extra_dst = "WASTE1"
    equib_src = 0.0
    equib_dst = 0.0
    multi_aspiration = False

    source = "ISYNTH:1"
    destination = "RACKL:1"
    volume = 2
    needle = 0
    src_flow = 0.4

    controller = Controller(
        cmd_folder=tmpdir,
        element_config=element_config,
        system_liquids=system_liquids,
        statuses=statuses,
        stdout=False,
        logfile=(tmpdir / "log.txt"),
        verbosity=0,
        simulation=False,
        track_quantities=False,
    )

    with pytest.deprecated_call():
        controller.inject_liquid(
            source=source,
            destination=destination,
            volume=volume,
            needle=needle,
            src_flow=src_flow,
            src_bu=src_distance,
            dst_flow=dst_flow,
            dst_bu=dst_distance,
            rinse_volume=rinse_volume,
        )

    source: WellGroup = WellGroup(
        source, well_configuration=controller.wells, logger=controller.logger
    )
    destination: WellGroup = WellGroup(
        destination, well_configuration=controller.wells, logger=controller.logger
    )
    airgap_dst: WellGroup = WellGroup(
        airgap_dst, well_configuration=controller.wells, logger=controller.logger
    )
    extra_dst: WellGroup = WellGroup(
        extra_dst, well_configuration=controller.wells, logger=controller.logger
    )

    expected_kwargs: Dict[str, Dict[str, Any]] = {
        "Source Zone": {"value": str(source), "unit": None},
        "Destination Zone": {"value": str(destination), "unit": None},
        "Volume": {"value": volume, "unit": "mL"},
        "Needle No.": {"value": needle, "unit": None},
        "Flow Rate (Source)": {"value": src_flow, "unit": "mL/min"},
        "Bottom-Up (Source)": {"value": int(src_bu), "unit": None},
        "Distance (Source)": {"value": src_distance, "unit": "mm"},
        "Flow Rate (Destination)": {"value": dst_flow, "unit": "mL/min"},
        "Bottom-Up (Destination)": {"value": int(dst_bu), "unit": None},
        "Distance (Destination)": {"value": dst_distance, "unit": "mm"},
        "Rinse Volume": {"value": rinse_volume, "unit": "mL"},
        "Rinse Station No.": {"value": rinse_stn, "unit": None},
        "Airgap Volume": {"value": airgap, "unit": "mL"},
        "Post-Airgap Volume": {"value": post_airgap, "unit": "mL"},
        "Airgap Destination": {"value": airgap_dst, "unit": None},
        "Extra Volume": {"value": extra_volume, "unit": "mL"},
        "Extra Volume Destination": {"value": extra_dst, "unit": None},
        "Equilib. Time (Source)": {"value": equib_src, "unit": "s"},
        "Equilib. Time (Destination)": {"value": equib_dst, "unit": "s"},
        "Multi. Aspiration Allowed": {
            "value": int(multi_aspiration),
            "unit": None,
        },
    }

    expected_command = "transfer_liquid"
    expected_values = ",".join([str(expected_kwargs[kwarg]["value"]) for kwarg in expected_kwargs]) + ",end"

    return expected_command, expected_values


@pytest.mark.timeout(45.0)
@autosuite_assertion
def test_transfer_solid(tmpdir: Path) -> Tuple[str, str]:
    source = "SOLID:1"
    destination = "ISYNTH:2"
    weight = 2.0
    height = 0.0
    chunk = 0.1
    equilib = 5.0
    auto_dispense = False
    rd_speed = 30.0
    rd_acc = 20.0
    rd_amp = 100.0
    fd_amount = 1.0
    fd_speed = 30.0
    fd_acc = 20.0
    fd_amp = 40.0
    fd_num = 360.0

    controller = Controller(
        cmd_folder=tmpdir,
        element_config=element_config,
        system_liquids=system_liquids,
        statuses=statuses,
        stdout=False,
        logfile=(tmpdir / "log.txt"),
        verbosity=0,
        simulation=False,
        track_quantities=False,
    )
    controller.transfer_solid(
        source=source,
        destination=destination,
        weight=weight,
        height=height,
        chunk=chunk,
        equilib=equilib,
        auto_dispense=auto_dispense,
        rd_speed=rd_speed,
        rd_acc=rd_acc,
        rd_amp=rd_amp,
        fd_amount=fd_amount,
        fd_speed=fd_speed,
        fd_acc=fd_acc,
        fd_amp=fd_amp,
        fd_num=fd_num,
    )

    source: WellGroup = WellGroup(
        source, well_configuration=controller.wells, logger=controller.logger
    )
    destination: WellGroup = WellGroup(
        destination, well_configuration=controller.wells, logger=controller.logger
    )

    expected_kwargs: Dict[str, Dict[str, Any]] = {
        "Source Zone": {"value": str(source), "unit": None},
        "Destination Zone": {"value": str(destination), "unit": None},
        "Mass": {"value": weight, "unit": "mg"},
        "Dispensing Height": {"value": height, "unit": "mm"},
        "Chunk Size": {"value": chunk, "unit": "mg"},
        "Equilibration Time": {"value": equilib, "unit": "s"},
        "Rough Dispensing Speed": {
            "value": rd_speed,
            "unit": "rpm",
        },
        "Rough Dispensing Acceleration": {"value": rd_acc, "unit": "deg s^-2"},
        "Rough Dispensing Amplitude": {"value": rd_amp, "unit": None},
        "Fine Dispensing Amount": {"value": fd_amount, "unit": "mg"},
        "Fine Dispensing Speed": {
            "value": fd_speed,
            "unit": "rpm",
        },
        "Fine Dispensing Acceleration": {"value": fd_acc, "unit": "deg s^-2"},
        "Fine Dispensing Amplitude": {"value": fd_amp, "unit": None},
        "Fine Dispensing Angle": {"value": fd_num, "unit": "°"},
        "Auto Dispense Activated": {"value": int(auto_dispense), "unit": None},
    }

    expected_command = "transfer_solid"
    expected_values = ",".join([str(expected_kwargs[kwarg]["value"]) for kwarg in expected_kwargs]) + ",end"

    return expected_command, expected_values


@pytest.mark.xfail(raises=NotImplementedError)
def test_transfer_solid_swile(tmpdir: Path) -> Tuple[str, str]:
    raise NotImplementedError()


@pytest.mark.timeout(45.0)
@autosuite_assertion
def test_set_drawer(tmpdir: Path) -> Tuple[str, str]:
    zone = "ISYNTH:1"
    state = "open"
    env = "inert"

    controller = Controller(
        cmd_folder=tmpdir,
        element_config=element_config,
        system_liquids=system_liquids,
        statuses=statuses,
        stdout=False,
        logfile=(tmpdir / "log.txt"),
        verbosity=0,
        simulation=False,
        track_quantities=False,
    )
    controller.set_drawer(
        zone=zone,
        state=state,
        environment=env,
    )

    zone: WellGroup = WellGroup(
        zone, well_configuration=controller.wells, logger=controller.logger
    )

    expected_kwargs = {
        "Zone": {"value": str(zone), "unit": None},
        "Target State": {"value": state, "unit": None},
        "Environment": {"value": env, "unit": None},
    }

    expected_command = "set_drawer"
    expected_values = ",".join([str(expected_kwargs[kwarg]["value"]) for kwarg in expected_kwargs]) + ",end"

    return expected_command, expected_values


@pytest.mark.timeout(45.0)
@autosuite_assertion
def test_set_isynth_reflux(tmpdir: Path) -> Tuple[str, str]:
    reflux_zone = "ISYNTH:1"
    state = "on"
    temperature = 20.0  # Example temperature value

    controller = Controller(
        cmd_folder=tmpdir,
        element_config=element_config,
        system_liquids=system_liquids,
        statuses=statuses,
        stdout=False,
        logfile=(tmpdir / "log.txt"),
        verbosity=0,
        simulation=False,
        track_quantities=False,
    )

    with pytest.deprecated_call():
        controller.set_isynth_reflux(state, temperature)

    _reflux_zone: WellGroup = WellGroup(
        reflux_zone, well_configuration=controller.wells, logger=controller.logger
    )

    expected_kwargs: Dict[str, Dict[str, Any]] = {
        "Zone": {"value": _reflux_zone.get_element_string(), "unit": None},
        "Target State": {"value": state, "unit": None},
        "Chiller Temperature": {"value": temperature, "unit": "°C"},
    }

    expected_command = "set_reflux"
    expected_values = ",".join([str(expected_kwargs[kwarg]["value"]) for kwarg in expected_kwargs]) + ",end"

    return expected_command, expected_values


@pytest.mark.timeout(45.0)
@autosuite_assertion
def test_set_reflux(tmpdir: Path) -> Tuple[str, str]:
    reflux_zone = "ISYNTH:1"
    state = "on"
    temperature = 20.0  # Example temperature value

    controller = Controller(
        cmd_folder=tmpdir,
        element_config=element_config,
        system_liquids=system_liquids,
        statuses=statuses,
        stdout=False,
        logfile=(tmpdir / "log.txt"),
        verbosity=0,
        simulation=False,
        track_quantities=False,
    )

    controller.set_reflux(reflux_zone, state, temperature)

    _reflux_zone: WellGroup = WellGroup(
        reflux_zone, well_configuration=controller.wells, logger=controller.logger
    )

    expected_kwargs: Dict[str, Dict[str, Any]] = {
        "Zone": {"value": _reflux_zone.get_element_string(), "unit": None},
        "Target State": {"value": state, "unit": None},
        "Chiller Temperature": {"value": temperature, "unit": "°C"},
    }

    expected_command = "set_reflux"
    expected_values = ",".join([str(expected_kwargs[kwarg]["value"]) for kwarg in expected_kwargs]) + ",end"

    return expected_command, expected_values


@pytest.mark.timeout(45.0)
@autosuite_assertion
def test_set_isynth_temperature(tmpdir: Path) -> Tuple[str, str]:
    temp_zone = "ISYNTH:1"
    state = "on"
    temperature = 25.0  # Example temperature value
    ramp = 2.0  # Example ramp value

    controller = Controller(
        cmd_folder=tmpdir,
        element_config=element_config,
        system_liquids=system_liquids,
        statuses=statuses,
        stdout=False,
        logfile=(tmpdir / "log.txt"),
        verbosity=0,
        simulation=False,
        track_quantities=False,
    )

    with pytest.deprecated_call():
        controller.set_isynth_temperature(state, temperature, ramp)

    _temp_zone: WellGroup = WellGroup(
        temp_zone, well_configuration=controller.wells, logger=controller.logger
    )

    expected_kwargs: Dict[str, Dict[str, Any]] = {
        "Zone": {"value": _temp_zone.get_element_string(), "unit": None},
        "Target State": {"value": state, "unit": None},
        "Temperature": {"value": temperature, "unit": "°C"},
        "Ramp Speed": {"value": ramp, "unit": "°C/min"},
    }

    expected_command = "set_temperature"
    expected_values = ",".join([str(expected_kwargs[kwarg]["value"]) for kwarg in expected_kwargs]) + ",end"

    return expected_command, expected_values


@pytest.mark.timeout(45.0)
@autosuite_assertion
def test_set_temperature(tmpdir: Path) -> Tuple[str, str]:
    temp_zone = "ISYNTH:1"
    state = "on"
    temperature = 25.0  # Example temperature value
    ramp = 2.0  # Example ramp value

    controller = Controller(
        cmd_folder=tmpdir,
        element_config=element_config,
        system_liquids=system_liquids,
        statuses=statuses,
        stdout=False,
        logfile=(tmpdir / "log.txt"),
        verbosity=0,
        simulation=False,
        track_quantities=False,
    )

    controller.set_temperature(temp_zone, state, temperature, ramp)

    _temp_zone: WellGroup = WellGroup(
        temp_zone, well_configuration=controller.wells, logger=controller.logger
    )

    expected_kwargs: Dict[str, Dict[str, Any]] = {
        "Zone": {"value": _temp_zone.get_element_string(), "unit": None},
        "Target State": {"value": state, "unit": None},
        "Temperature": {"value": temperature, "unit": "°C"},
        "Ramp Speed": {"value": ramp, "unit": "°C/min"},
    }

    expected_command = "set_temperature"
    expected_values = ",".join([str(expected_kwargs[kwarg]["value"]) for kwarg in expected_kwargs]) + ",end"

    return expected_command, expected_values


@pytest.mark.timeout(45.0)
@autosuite_assertion
def test_set_isynth_stir(tmpdir: Path) -> List[List[str]]:
    stir_zone = "ISYNTH:1"
    state = "on"
    rpm = 200.0  # Example RPM value

    controller = Controller(
        cmd_folder=tmpdir,
        element_config=element_config,
        system_liquids=system_liquids,
        statuses=statuses,
        stdout=False,
        logfile=(tmpdir / "log.txt"),
        verbosity=0,
        simulation=False,
        track_quantities=False,
    )

    with pytest.deprecated_call():
        controller.set_isynth_stir(state, rpm)

    _stir_zone: WellGroup = WellGroup(
        stir_zone, well_configuration=controller.wells, logger=controller.logger
    )

    expected_kwargs: Dict[str, Dict[str, Any]] = {
        "Zone": {"value": _stir_zone.get_element_string(), "unit": None},
        "Target State": {"value": state, "unit": None},
        "Stir Rate": {"value": rpm, "unit": "rpm"},
    }

    expected_command = "set_stir"
    expected_values = ",".join([str(expected_kwargs[kwarg]["value"]) for kwarg in expected_kwargs]) + ",end"

    return [["unmount_all", expected_command], [",end", expected_values]]


@pytest.mark.timeout(45.0)
@autosuite_assertion
def test_set_stir(tmpdir: Path) -> List[List[str]]:
    stir_zone = "ISYNTH:1"
    state = "on"
    rpm = 200.0  # Example RPM value

    controller = Controller(
        cmd_folder=tmpdir,
        element_config=element_config,
        system_liquids=system_liquids,
        statuses=statuses,
        stdout=False,
        logfile=(tmpdir / "log.txt"),
        verbosity=0,
        simulation=False,
        track_quantities=False,
    )

    controller.set_stir(stir_zone, state, rpm)

    _stir_zone: WellGroup = WellGroup(
        stir_zone, well_configuration=controller.wells, logger=controller.logger
    )

    expected_kwargs: Dict[str, Dict[str, Any]] = {
        "Zone": {"value": _stir_zone.get_element_string(), "unit": None},
        "Target State": {"value": state, "unit": None},
        "Stir Rate": {"value": rpm, "unit": "rpm"},
    }

    expected_command = "set_stir"
    expected_values = ",".join([str(expected_kwargs[kwarg]["value"]) for kwarg in expected_kwargs]) + ",end"

    return [["unmount_all", expected_command], [",end", expected_values]]


@pytest.mark.timeout(45.0)
@autosuite_assertion
def test_set_isynth_vacuum(tmpdir: Path) -> Tuple[str, str]:
    vac_zone = "ISYNTH:1"
    state = "on"
    vacuum = 800.0  # Example vacuum pressure value

    controller = Controller(
        cmd_folder=tmpdir,
        element_config=element_config,
        system_liquids=system_liquids,
        statuses=statuses,
        stdout=False,
        logfile=(tmpdir / "log.txt"),
        verbosity=0,
        simulation=False,
        track_quantities=False,
    )

    with pytest.deprecated_call():
        controller.set_isynth_vacuum(state, vacuum)

    _vac_zone: WellGroup = WellGroup(
        vac_zone, well_configuration=controller.wells, logger=controller.logger
    )

    expected_kwargs: Dict[str, Dict[str, Any]] = {
        "Zone": {"value": _vac_zone.get_element_string(), "unit": None},
        "Target State": {"value": state, "unit": None},
        "Pressure": {"value": vacuum, "unit": "mbar"},
    }

    expected_command = "set_vacuum"
    expected_values = ",".join([str(expected_kwargs[kwarg]["value"]) for kwarg in expected_kwargs]) + ",end"

    return expected_command, expected_values


@pytest.mark.timeout(45.0)
@autosuite_assertion
def test_set_vacuum(tmpdir: Path) -> Tuple[str, str]:
    vac_zone = "ISYNTH:1"
    state = "on"
    vacuum = 800.0  # Example vacuum pressure value

    controller = Controller(
        cmd_folder=tmpdir,
        element_config=element_config,
        system_liquids=system_liquids,
        statuses=statuses,
        stdout=False,
        logfile=(tmpdir / "log.txt"),
        verbosity=0,
        simulation=False,
        track_quantities=False,
    )

    controller.set_vacuum(vac_zone, state, vacuum)

    _vac_zone: WellGroup = WellGroup(
        vac_zone, well_configuration=controller.wells, logger=controller.logger
    )

    expected_kwargs: Dict[str, Dict[str, Any]] = {
        "Zone": {"value": _vac_zone.get_element_string(), "unit": None},
        "Target State": {"value": state, "unit": None},
        "Pressure": {"value": vacuum, "unit": "mbar"},
    }

    expected_command = "set_vacuum"
    expected_values = ",".join([str(expected_kwargs[kwarg]["value"]) for kwarg in expected_kwargs]) + ",end"

    return expected_command, expected_values


@pytest.mark.timeout(45.0)
@autosuite_assertion
def test_vial_transport(tmpdir: Path) -> Tuple[str, str]:
    source = "ISYNTH:1"
    destination = "ISYNTH:2"
    gripping_force = 15.0  # Example gripping force value
    gripping_depth = 8.0  # Example gripping depth value
    push_in = True
    grip_inside = False

    controller = Controller(
        cmd_folder=tmpdir,
        element_config=element_config,
        system_liquids=system_liquids,
        statuses=statuses,
        stdout=False,
        logfile=(tmpdir / "log.txt"),
        verbosity=0,
        simulation=False,
        track_quantities=False,
    )

    controller.vial_transport(
        source=source,
        destination=destination,
        gripping_force=gripping_force,
        gripping_depth=gripping_depth,
        push_in=push_in,
        grip_inside=grip_inside,
    )

    _source: WellGroup = WellGroup(
        source, well_configuration=controller.wells, logger=controller.logger
    )
    _destination: WellGroup = WellGroup(
        destination, well_configuration=controller.wells, logger=controller.logger
    )

    expected_kwargs: Dict[str, Dict[str, Any]] = {
        "Source Zone": {"value": str(_source), "unit": None},
        "Destination Zone": {"value": str(_destination), "unit": None},
        "Gripping Force": {"value": gripping_force, "unit": "N"},
        "Gripping Depth": {"value": gripping_depth, "unit": "mm"},
        "Push Vial In": {"value": int(push_in), "unit": None},
        "Grip Vial from Inside": {"value": int(grip_inside), "unit": None},
    }

    expected_command = "vial_transport"
    expected_values = ",".join([str(expected_kwargs[kwarg]["value"]) for kwarg in expected_kwargs]) + ",end"

    return expected_command, expected_values


@pytest.mark.timeout(45.0)
@autosuite_assertion
def test_set_zone_state(tmpdir: Path) -> Tuple[str, str]:
    zone = "ISYNTH:1"
    state = True  # Example state value

    controller = Controller(
        cmd_folder=tmpdir,
        element_config=element_config,
        system_liquids=system_liquids,
        statuses=statuses,
        stdout=False,
        logfile=(tmpdir / "log.txt"),
        verbosity=0,
        simulation=False,
        track_quantities=False,
    )

    controller.set_zone_state(zone=zone, state=state)

    _zone: WellGroup = WellGroup(
        zone, well_configuration=controller.wells, logger=controller.logger
    )

    expected_kwargs: Dict[str, Dict[str, Any]] = {
        "Zone": {"value": str(_zone), "unit": None},
        "Target State": {"value": int(state), "unit": None},
    }

    expected_command = "set_zone_state"
    expected_values = ",".join([str(expected_kwargs[kwarg]["value"]) for kwarg in expected_kwargs]) + ",end"

    return expected_command, expected_values


@pytest.mark.timeout(45.0)
@autosuite_assertion
def test_measure_level(tmpdir: Path) -> Tuple[str, str]:
    zone = "ISYNTH:1"

    controller = Controller(
        cmd_folder=tmpdir,
        element_config=element_config,
        system_liquids=system_liquids,
        statuses=statuses,
        stdout=False,
        logfile=(tmpdir / "log.txt"),
        verbosity=0,
        simulation=False,
        track_quantities=False,
    )

    controller.measure_level(zone=zone)

    _zone: WellGroup = WellGroup(
        zone, well_configuration=controller.wells, logger=controller.logger
    )

    expected_kwargs = {"Zone": {"value": str(_zone), "unit": None}}

    expected_command = "measure_level"
    expected_values = ",".join([str(expected_kwargs[kwarg]["value"]) for kwarg in expected_kwargs]) + ",end"

    return expected_command, expected_values


@pytest.mark.timeout(45.0)
@autosuite_assertion
def test_unmount_all(tmpdir: Path) -> Tuple[str, str]:
    controller = Controller(
        cmd_folder=tmpdir,
        element_config=element_config,
        system_liquids=system_liquids,
        statuses=statuses,
        stdout=False,
        logfile=(tmpdir / "log.txt"),
        verbosity=0,
        simulation=False,
        track_quantities=False,
    )

    controller.unmount_all()

    expected_command = "unmount_all"
    expected_values = ",end"

    return expected_command, expected_values


@pytest.mark.timeout(45.0)
@autosuite_assertion
def test_stop_manager(tmpdir: Path) -> Tuple[str, str]:
    controller = Controller(
        cmd_folder=tmpdir,
        element_config=element_config,
        system_liquids=system_liquids,
        statuses=statuses,
        stdout=False,
        logfile=(tmpdir / "log.txt"),
        verbosity=0,
        simulation=False,
        track_quantities=False,
    )

    controller.stop_manager()

    expected_command = "stop_manager"
    expected_values = ",end"

    return expected_command, expected_values


@pytest.mark.timeout(45.0)
@autosuite_assertion
def test_wait(tmpdir: Path) -> Tuple[str, str]:
    controller = Controller(
        cmd_folder=tmpdir,
        element_config=element_config,
        system_liquids=system_liquids,
        statuses=statuses,
        stdout=False,
        logfile=(tmpdir / "log.txt"),
        verbosity=0,
        simulation=False,
        track_quantities=False,
    )

    duration = 10  # duration
    controller.wait(duration)

    expected_command = "wait"
    expected_values = f"{duration},end"

    return expected_command, expected_values
