from femmt import MagneticComponent as fmc
from femmt import Functions as ff
from femmt import Model as model
from femmt.Enumerations import *
import os

# Working directory can be set arbitrarily
working_directory = os.path.join(os.path.dirname(__file__), "inductor")
if not os.path.exists(working_directory):
    os.mkdir(working_directory)

geo = fmc.MagneticComponent(component_type=ComponentType.Transformer, working_directory=working_directory)
#geo = fmc.MagneticComponent(component_type=ComponentType.Inductor, working_directory=working_directory)

core_db = ff.core_database()["PQ 40/40"]

core = model.Core(core_inner_diameter=core_db["core_w"], window_w=core_db["window_w"], window_h=core_db["window_h"],
                material="95_100")

geo.set_core(core)

air_gaps = model.AirGaps(AirGapMethod.Percent, core)
air_gaps.add_air_gap(AirGapLegPosition.CenterLeg, 10, 0.0005)
air_gaps.add_air_gap(AirGapLegPosition.CenterLeg, 90, 0.0005)
geo.set_air_gaps(air_gaps)

insulation = model.Insulation()
insulation.add_core_insulations(0.001, 0.001, 0.001, 0.001)
insulation.add_winding_insulations([0.0001, 0.0001], 0.0001)
geo.set_insulation(insulation)

winding_window = model.WindingWindow(core, insulation)
conductor1 = model.Conductor(0, Conductivity.Copper)
conductor1.set_solid_round_conductor(0.0005, ConductorArrangement.Square)

conductor2 = model.Conductor(1, Conductivity.Copper)
conductor2.set_solid_round_conductor(0.0005, ConductorArrangement.Square)

left, right = winding_window.split_window(WindingWindowSplit.HorizontalSplit)
left.set_winding(conductor1, 5, None)
right.set_winding(conductor2, 5, None)

#top_left, top_right, bot_left, bot_right = winding_window.split_window(WindingWindowSplit.HorizontalAndVerticalSplit, 0.5, 0.5)
#top_left.set_winding(conductor1, 5, WindingScheme.FoilHorizontal, WrapParaType.FixedThickness)
#bot_left.set_winding(conductor2, 5, None, None)

#right = winding_window.combine_vww(top_right, bot_right)
#right.set_interleaved_winding(conductor1, 5, conductor2, 5, InterleavedWindingScheme.HorizontalAlternating)

#complete = winding_window.split_window(WindingWindowSplit.NoSplit)
#complete.set_winding(conductor1, 9, None, None)


geo.set_winding_window(winding_window)

geo.create_model(freq=100000, visualize_before=True, save_png=False)
#geo.single_simulation(freq=100000, current=[4.5], show_results=True)
geo.single_simulation(freq=100000, current=[4.5, 4.5], phi_deg=[0, 180], show_results=True)
