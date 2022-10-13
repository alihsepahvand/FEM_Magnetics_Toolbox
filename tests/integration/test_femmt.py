import pytest
import os
import json
import femmt as fmt

def compare_result_logs(first_log, second_log):
    first_content = None
    second_content = None

    with open(first_log, "r") as fd:
        first_content = json.loads(fd.read())
        if "date" in first_content["simulation_settings"]:
            del first_content["simulation_settings"]["date"]
        if "working_directory" in first_content["simulation_settings"]:
            del first_content["simulation_settings"]["working_directory"]

    with open(second_log, "r") as fd:
        second_content = json.loads(fd.read())
        if "date" in second_content["simulation_settings"]:
            del second_content["simulation_settings"]["date"]
        if "working_directory" in second_content["simulation_settings"]:
            del second_content["simulation_settings"]["working_directory"]

    print(first_content)
    print(second_content)
    return first_content == second_content

@pytest.fixture
def temp_folder():
    # Setup temp folder
    temp_folder_path = os.path.join(os.path.dirname(__file__), "temp")

    if not os.path.exists(temp_folder_path):
        os.mkdir(temp_folder_path)

    # Get onelab path
    onelab_path = os.path.join(os.path.dirname(__file__), "..", "..", "onelab")

    # Test
    yield temp_folder_path, onelab_path

@pytest.fixture
def femmt_simulation(temp_folder):
    temp_folder_path, onelab_folder = temp_folder
    
    # Create new temp folder, build model and simulate
    try:
        working_directory = temp_folder_path
        if not os.path.exists(working_directory):
            os.mkdir(working_directory)

        # Set is_gui = True so FEMMt won't ask for the onelab path if no config is found.
        geo = fmt.MagneticComponent(component_type=fmt.ComponentType.Inductor, working_directory=working_directory, silent=True, is_gui=True)

        # Set onelab path manually
        geo.file_data.onelab_folder_path = onelab_folder
        
        core_db = fmt.core_database()["PQ 40/40"]

        core = fmt.Core(core_inner_diameter=core_db["core_inner_diameter"], window_w=core_db["window_w"], window_h=core_db["window_h"],
                        material="95_100")
        geo.set_core(core)

        air_gaps = fmt.AirGaps(fmt.AirGapMethod.Percent, core)
        air_gaps.add_air_gap(fmt.AirGapLegPosition.CenterLeg, 0.0005, 10)
        air_gaps.add_air_gap(fmt.AirGapLegPosition.CenterLeg, 0.0005, 90)
        geo.set_air_gaps(air_gaps)

        insulation = fmt.Insulation()
        insulation.add_core_insulations(0.001, 0.001, 0.004, 0.001)
        insulation.add_winding_insulations([0.0005], 0.0001)
        geo.set_insulation(insulation)

        winding_window = fmt.WindingWindow(core, insulation)
        vww = winding_window.split_window(fmt.WindingWindowSplit.NoSplit)

        winding = fmt.Conductor(0, fmt.Conductivity.Copper)
        winding.set_solid_round_conductor(conductor_radius=0.0013, conductor_arrangement=fmt.ConductorArrangement.Square)

        vww.set_winding(winding, 9, None)
        geo.set_winding_window(winding_window)

        geo.create_model(freq=100000, visualize_before=False, save_png=False)

        geo.single_simulation(freq=100000, current=[4.5], show_results=False)

        """
        Currently only the magnetics simulation is tested

        thermal_conductivity_dict = {
                "air": 0.0263,
                "case": 0.3,
                "core": 5,
                "winding": 400,
                "air_gaps": 180
        }
        case_gap_top = 0.0015
        case_gap_right = 0.0025
        case_gap_bot = 0.002
        boundary_temperatures = {
            "value_boundary_top": 293,
            "value_boundary_top_right": 293,
            "value_boundary_right_top": 293,
            "value_boundary_right": 293,
            "value_boundary_right_bottom": 293,
            "value_boundary_bottom_right": 293,
            "value_boundary_bottom": 293
        }
        boundary_flags = {
            "flag_boundary_top": 1,
            "flag_boundary_top_right": 1,
            "flag_boundary_right_top": 1,
            "flag_boundary_right": 1,
            "flag_boundary_right_bottom": 1,
            "flag_boundary_bottom_right": 1,
            "flag_boundary_bottom": 1
        }

        geo.thermal_simulation(thermal_conductivity_dict, boundary_temperatures, boundary_flags, case_gap_top, case_gap_right, case_gap_bot, show_results=False)
        """
    except Exception as e:
        print("An error occurred while creating the femmt mesh files:", e)
    except KeyboardInterrupt:
        print("Keyboard interrupt..")

    return os.path.join(temp_folder_path, "results", "log_electro_magnetic.json")

def test_femmt(femmt_simulation):
    """
    The first idea was to compare the simulated meshes with test meshes simulated manually.
    It turns out that the meshes cannot be compared because even slightly differences in the mesh,
    can cause to a test failure, because the meshes are binary files.
    Those differences could even occur when running the simulation on different machines
    -> This was observed when creating a docker image and running the tests.

    Now as an example only the result log will be checked.
    """
    test_result_log = femmt_simulation

    assert os.path.exists(test_result_log), "Electro magnetic simulation did not work!"

    # e_m mesh
    fixture_result_log = os.path.join(os.path.dirname(__file__), "fixtures", "results", "log_electro_magnetic.json")
    assert compare_result_logs(test_result_log, fixture_result_log), "Electro magnetic results file is wrong."
