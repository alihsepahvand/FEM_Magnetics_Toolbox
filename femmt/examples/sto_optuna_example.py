# python libraries
import os

# 3rd party libraries
import numpy as np
import datetime

#femmt libraries
import femmt as fmt



core_database = fmt.core_database()
pq3230 = core_database["PQ 32/30"]
pq4040 = core_database["PQ 40/40"]
pq5050 = core_database["PQ 50/50"]
pq6560 = core_database["PQ 65/60"]


i_1 = [[0.0, 3.265248131976911e-07, 2.5e-06, 2.8265248131976912e-06, 5e-06], [-0.9996115022426437, 4.975792579275104, 0.9996115022426446, -4.975792579275103, -0.9996115022426437]]
i_2 = [[0.0, 3.265248131976911e-07, 2.5e-06, 2.8265248131976912e-06, 5e-06], [-0.9196195846583147, -19.598444313231134, 0.9196195846583122, 19.59844431323113, -0.9196195846583147]]

sto_insulations = fmt.StoInsulation(
    iso_top_core=0.001,
    iso_bot_core=0.001,
    iso_left_core=0.002,
    iso_right_core=0.001,
    iso_primary_to_primary=2e-4,
    iso_secondary_to_secondary=2e-4,
    iso_primary_to_secondary=4e-4,
    iso_primary_additional=1e-3
)

dab_transformer_config = fmt.StoSingleInputConfig(
    # target parameters
    l_s12_target = 5.8e-6,
    l_h_target= 90e-6,
    n_target= 15,

    # operating point parameters
    time_current_1_vec = np.array(i_1),
    time_current_2_vec = np.array(i_2),
    temperature=100,

    # sweep parameters: geometry and material
    material_list = ["N95"],
    core_inner_diameter_min_max_list= [18e-3, 22e-3],
    window_w_min_max_list= [10e-3, 14e-3],
    window_h_bot_min_max_list= [13e-3, 15e-3],
    max_transformer_total_height=40e-3,
    primary_litz_wire_list= ["1.71x140x0.1"],
    metal_sheet_thickness_list= [0.0005, 0.0015],
    primary_coil_turns_min_max_list = [1,5],

    # fix parameters
    insulations=sto_insulations,

    # misc
    working_directory=os.path.join(os.path.dirname(__file__), "example_results", "optuna_stacked_transformer_optimization")
)

study_name = "2023-07-05"

if __name__ == '__main__':
    time_start = datetime.datetime.now()


    fmt.StackedTransformerOptimization.FemSimulation.NSGAII.start_proceed_study(study_name, dab_transformer_config, 2)
    #fmt.StackedTransformerOptimization.FemSimulation.NSGAII.show_study_results(study_name, dab_transformer_config)