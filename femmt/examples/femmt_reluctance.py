# 2D-axis symmetric core reluctance calculations

import femmt as fmt
import numpy as np
import schemdraw
import schemdraw.elements as elm


def basic_example_func(f_height, f_position, f_n_turns, f_core_cond_iso, f_current):

    # 2. set core parameters
    core_db = fmt.core_database()["PQ 40/40"]

    core = fmt.Core(core_w=core_db["core_w"], window_w=core_db["window_w"], window_h=core_db["window_h"],
                    material="95_100")
    # mu_rel=3000, phi_mu_deg=10,
    # sigma=0.5)
    geo.set_core(core)

    # 3. set air gap parameters
    air_gaps = fmt.AirGaps(fmt.AirGapMethod.Percent, core)
    air_gaps.add_air_gap(fmt.AirGapLegPosition.CenterLeg, f_position[0], f_height)
    # air_gaps.add_air_gap(fmt.AirGapLegPosition.CenterLeg, f_position[1], f_height)
    # air_gaps.add_air_gap(fmt.AirGapLegPosition.CenterLeg, f_position[2], f_height)
    # air_gaps.add_air_gap(fmt.AirGapLegPosition.CenterLeg, f_position[3], f_height)
    # air_gaps.add_air_gap(fmt.AirGapLegPosition.CenterLeg, f_position[4], f_height)
    geo.set_air_gaps(air_gaps)

    # 4. set conductor parameters: use solid wires
    winding = fmt.Winding(f_n_turns, 0, fmt.Conductivity.Copper, fmt.WindingType.Primary, fmt.WindingScheme.Square)
    winding.set_solid_conductor(0.0013)
    # winding.set_litz_conductor(conductor_radius=0.0013, number_strands=150, strand_radius=100e-6, fill_factor=None)
    geo.set_windings([winding])

    # 5. set isolations
    isolation = fmt.Isolation()
    isolation.add_core_isolations(0.001, 0.001, f_core_cond_iso, 0.001)
    isolation.add_winding_isolations(0.0005)
    geo.set_isolation(isolation)

    # 5. create the model
    geo.create_model(freq=100000, visualize_before=False, save_png=False)

    # 6. start simulation
    geo.single_simulation(freq=100000, current=[f_current], show_results=False)


class MagneticCircuit:

    """This is a class for calculating the reluctance and inductance and visualising magnetic circuit"""

    # position_tag = 0 for 2D axis symmetric cores
    def __init__(self, core_w, window_h, window_w,
                 no_of_turns, current, method, n_air_gaps, air_gap_h, air_gap_position):

        self.core_h = window_h + core_w / 2
        self.core_w = core_w
        self.window_h = window_h
        self.window_w = window_w
        self.r_outer = None
        self.r_inner = None
        self.core_h_middle = None  # height of upper and lower part of the window in the core
        self.outer_w = None  # Outer leg width

        self.no_of_turns = no_of_turns
        self.current = current
        self.method = method
        self.n_air_gaps = n_air_gaps
        self.air_gap_h = air_gap_h
        self.air_gap_position = air_gap_position

        self.L = None          # Total inductance
        self.section = None
        self.orientation = None
        self.length = None
        self.area = None
        self.fringe_area = None
        self.fringe_dist = None
        self.reluctance = None
        self.mu_rel = 3000
        self.mu_0 = 4 * np.pi * 1e-7

        self.max_percent = None
        self.min_percent = None
        self.position = None

    def core_reluctance(self):
        self.core_h_middle = (self.core_h - self.window_h)/2
        self.r_inner = self.core_w/2 + self.window_w
        self.r_outer = np.sqrt((self.core_w / 2) ** 2 + self.r_inner ** 2)
        self.outer_w = self.r_outer - self.r_inner

        self.section = [0, 1, 2, 3, 4]
        self.length = np.zeros(len(self.section))
        self.area = np.zeros(len(self.section))
        self.reluctance = np.zeros(len(self.section))

        self.length[0] = self.window_h - sum(self.air_gap_h)
        self.area[0] = np.pi * ((self.core_w/2) ** 2)

        self.length[1] = (np.pi / 8) * (self.core_w / 2 + self.core_h_middle)
        self.area[1] = ((self.core_w / 2 + self.core_h_middle) / 2) * 2 * np.pi * (self.core_w / 2)

        self.length[2] = self.window_w
        self.area[2] = np.nan
        self.reluctance[2] = ((self.mu_0 * self.mu_rel * 2 * np.pi * self.core_h_middle) ** -1) * np.log((2 * self.r_inner) / self.core_w)

        self.length[3] = (np.pi / 8) * (self.outer_w + self.core_h_middle)
        self.area[3] = ((self.outer_w + self.core_h_middle) / 2) * 2 * np.pi * self.r_inner

        self.length[4] = self.window_h
        self.area[4] = np.pi * (self.r_outer ** 2 - self.r_inner ** 2)

        self.reluctance[~np.isnan(self.area)] = self.length[~np.isnan(self.area)] / (self.mu_0 * self.mu_rel * self.area[~np.isnan(self.area)])
        self.reluctance[1:3] = 2 * self.reluctance[1:3]

    def air_gap_reluctance(self):
        flag_0 = 0
        flag_1 = 0
        flag_2 = 0
        if self.method == 'center':
            self.section.append(6)  # round-round
            temp1 = fmt.r_basis(self.air_gap_h[0] / 2, self.core_w, (self.window_h - self.air_gap_h[0]) / 2)
            temp2 = fmt.sigma(self.air_gap_h[0], self.core_w / 2, 2 * temp1)
            temp3 = fmt.r_round_round(self.air_gap_h[0], temp2, self.core_w / 2)
            temp4 = self.air_gap_h[0] / (self.mu_0 * np.pi * (self.core_w / 2) ** 2)    # classical reluctance formula
            self.reluctance = np.append(self.reluctance, temp4)
            self.fringe_area = (np.pi * (self.core_w / 2) ** 2) * (1 / (temp2 * temp2))
            self.fringe_dist = np.sqrt(self.fringe_area / np.pi) - (self.core_w / 2)
        # Assuming only equally distributed airgaps
        elif self.method == 'percent':
            self.max_percent = ((self.window_h - self.air_gap_h[self.n_air_gaps - 1] / 2) / self.window_h) * 100
            self.min_percent = ((self.air_gap_h[0] / 2) / self.window_h) * 100
            self.position = np.array(self.air_gap_position) / 100 * self.window_h  # Convert percent position to absolute value position
            print(f"Max percent: {self.max_percent}")
            print(f"Min percent: {self.min_percent}")

            if self.air_gap_position[0] <= self.min_percent:
                flag_0 = 1
                self.section.append(8)
                if self.n_air_gaps == 1:
                    h = self.window_h - self.air_gap_h[0]
                else:
                    h = ((self.position[1] - self.air_gap_h[1] / 2) - self.air_gap_h[0]) / 2

                temp1 = fmt.r_basis(self.air_gap_h[0], self.core_w, h)
                temp2 = fmt.sigma(self.air_gap_h[0], self.core_w / 2, temp1)
                temp3 = fmt.r_round_inf(self.air_gap_h[0], temp2, self.core_w / 2)
                self.reluctance = np.append(self.reluctance, temp3)
                print('air gap is at lower corner')

            if self.air_gap_position[self.n_air_gaps - 1] >= self.max_percent:
                flag_1 = 1
                self.section.append(8)
                if self.n_air_gaps == 1:
                    h = self.window_h - self.air_gap_h[self.n_air_gaps - 1]
                else:
                    h = (self.position[self.n_air_gaps - 1] - self.position[self.n_air_gaps - 2] - self.air_gap_h[self.n_air_gaps - 1] / 2 - self.air_gap_h[self.n_air_gaps - 2] / 2) / 2

                temp1 = fmt.r_basis(self.air_gap_h[self.n_air_gaps - 1], self.core_w, h)
                temp2 = fmt.sigma(self.air_gap_h[self.n_air_gaps - 1], self.core_w / 2, temp1)
                temp3 = fmt.femmt_functions.r_round_inf(self.air_gap_h[self.n_air_gaps - 1], temp2, self.core_w / 2)
                self.reluctance = np.append(self.reluctance, temp3)
                print('air gap is at upper corner')

            for i in range(self.n_air_gaps):
                if self.min_percent < self.air_gap_position[i] < self.max_percent:
                    self.section.append(7)
                    if flag_2 == 0:

                        if flag_0 == 0 and flag_1 == 0:     # No corner air-gaps
                            self.position = np.append(self.position, self.window_h + (self.window_h - self.position[self.n_air_gaps - 1]))
                            self.position = np.insert(self.position, 0, -self.position[0])
                            self.air_gap_h = np.append(self.air_gap_h, self.air_gap_h[self.n_air_gaps - 1])
                            self.air_gap_h = np.insert(self.air_gap_h, 0, self.air_gap_h[0])
                        elif flag_0 == 1 and flag_1 == 0:   # Only lower air-gap is present
                            self.position = np.append(self.position, self.window_h + (self.window_h - self.position[self.n_air_gaps - 1]))
                            self.air_gap_h = np.append(self.air_gap_h, self.air_gap_h[self.n_air_gaps - 1])
                        elif flag_0 == 0 and flag_1 == 1:   # Only Upper air-gap is present
                            self.position = np.insert(self.position, 0, -self.position[0])
                            self.air_gap_h = np.insert(self.air_gap_h, 0, self.air_gap_h[0])
                        flag_2 = 1

                    if flag_0 == 0 and flag_1 == 0:
                        h1 = (self.position[i + 1] - self.position[i] - self.air_gap_h[i + 1] / 2 - self.air_gap_h[i] / 2) / 2
                        h2 = (self.position[i + 2] - self.position[i + 1] - self.air_gap_h[i + 2] / 2 - self.air_gap_h[i + 1] / 2) / 2
                        print('No corner air gap detected')
                    elif flag_0 == 1 and flag_1 == 0:
                        h1 = (self.position[i] - self.position[i - 1] - self.air_gap_h[i] / 2 - self.air_gap_h[i - 1] / 2) / 2
                        h2 = (self.position[i + 1] - self.position[i] - self.air_gap_h[i + 1] / 2 - self.air_gap_h[i] / 2) / 2
                        print('Lower air gap detected')
                    elif flag_0 == 0 and flag_1 == 1:
                        h1 = (self.position[i + 1] - self.position[i] - self.air_gap_h[i + 1] / 2 - self.air_gap_h[i] / 2) / 2
                        h2 = (self.position[i + 2] - self.position[i + 1] - self.air_gap_h[i + 2] / 2 - self.air_gap_h[i + 1] / 2) / 2
                        print('Upper air gap detected')
                    else:
                        h1 = (self.position[i] - self.position[i - 1] - self.air_gap_h[i] / 2 - self.air_gap_h[i - 1] / 2) / 2
                        h2 = (self.position[i + 1] - self.position[i] - self.air_gap_h[i + 1] / 2 - self.air_gap_h[i] / 2) / 2
                        print('Both air gap detected')

                    r_basis_1 = fmt.r_basis(self.air_gap_h[i] / 2, self.core_w, h1)
                    r_basis_2 = fmt.r_basis(self.air_gap_h[i] / 2, self.core_w, h2)
                    temp2 = fmt.sigma(self.air_gap_h[i], self.core_w / 2, r_basis_1 + r_basis_2)
                    temp3 = fmt.femmt_functions.r_round_round(self.air_gap_h[i], temp2, self.core_w / 2)
                    self.reluctance = np.append(self.reluctance, temp3)

        # self.section, self.orientation = set_orientation(self.section, len(self.section))
        self.L = (self.no_of_turns * self.no_of_turns) / sum(self.reluctance)


# Sweep of air-gap and winding position and compare it with FEM simulation
sweep_air_gap_h = np.linspace(0.0001, 0.0005, 3)
sweep_wndg_pos = np.linspace(0.001, 0.007, 5)
# sweep_current = np.linspace(0.1, 10, 5)
fem_ind = np.zeros((len(sweep_air_gap_h), len(sweep_wndg_pos)))
cal_ind = np.zeros((len(sweep_air_gap_h), len(sweep_wndg_pos)))
# cal_fringe_dist = np.zeros((len(sweep_air_gap_h), len(sweep_wndg_pos)))

# Working directory can be set arbitrarily
working_directory = fmt.os.path.join(fmt.os.path.dirname(__file__), '..')

# 1. chose simulation type
geo = fmt.MagneticComponent(component_type=fmt.ComponentType.Inductor, working_directory=working_directory)

for j in range(len(sweep_air_gap_h)):
    for k in range(len(sweep_wndg_pos)):
        mc1 = MagneticCircuit(0.0149, 0.0295, 0.01105, 9, 10, 'center', 1, [sweep_air_gap_h[j]], [50])  # 0.0149
        mc1.core_reluctance()
        mc1.air_gap_reluctance()
        cal_ind[j, k] = mc1.L #- (2.38295 * 1e-6 - 0.000326175 * sweep_wndg_pos[k])
        # cal_fringe_dist[j, k] = mc1.fringe_dist
        mc1.max_percent = ((mc1.window_h - (sweep_air_gap_h[j] / 2)) / mc1.window_h) * 100
        mc1.min_percent = ((sweep_air_gap_h[j] / 2) / mc1.window_h) * 100

        # basic_example_func(sweep_air_gap_h[j], [mc1.min_percent + 0.1, 25, 50, 75, mc1.max_percent - 0.1], 9, sweep_wndg_pos[k], 10)
        basic_example_func(sweep_air_gap_h[j], [50], 9, sweep_wndg_pos[k], 10)
        fem_ind[j, k] = geo.read_log()["single_sweeps"][0]["winding1"]["self_inductivity"][0]
        # fem_ind[j, k] = geo.read_log()["single_sweeps"][0]["winding1"]["Q"]

print(f"Air-gap length: {sweep_air_gap_h}")
print(f"Winding position: {sweep_wndg_pos}")
print(f"FEM inductance: {fem_ind}")
print(f"Calculated inductance: {cal_ind}")
# print(f"Calculated fringe dist: {cal_fringe_dist}")

h_by_l = ((0.0295 - sweep_air_gap_h) / 2) / sweep_air_gap_h
abs_error = cal_ind - fem_ind
error = (abs_error / fem_ind) * 100
avg_abs_error = np.sum(abs_error, axis=0) / 5

print(f"h_by_l: {h_by_l}")
print(f"abs_error: {abs_error}")
print(f"percent error: {error}")
print(f"average actual error: {avg_abs_error}")

np.savetxt('absolute_error.txt', abs_error)


# Plotting tools
fig, ax = fmt.plt.subplots()  # Create a figure containing a single axes.
fmt.plt.title("Inductance % error vs winding pos (3 conductors) (center airgaps)")
fmt.plt.xlabel("Winding position (in m)")
fmt.plt.ylabel("Percent error (in %)")
# ax.plot(Air_gap_length, FEM_inductance, 'o')
for j in range(len(sweep_air_gap_h)):
    # ax.plot(sweep_wndg_pos, fem_ind[j, :], sweep_wndg_pos, cal_ind[j, :], label=str(sweep_air_gap_h[j]))
    ax.plot(sweep_wndg_pos, error[j, :], label=str(sweep_air_gap_h[j]))
ax.legend(loc='best')
ax.grid()
fmt.plt.show()


# mc1 = MagneticCircuit(0.0398, 0.0149, 0.0295, 0.01105, 8, 3, 'center', 1, [0.0005], [50])
# mc1 = MagneticCircuit(0.0149, 0.0295, 0.01105, 8, 3, 'center', 1, [0.02], [50])
# mc1 = MagneticCircuit(0.0149, 0.0295, 0.01105, 8, 3, 'percent', 2, [0.0005, 0.0005], [20, 50])
# mc1.core_reluctance()
# mc1.air_gap_reluctance()
# mc1.draw_schematic()
# plot_error()


# def set_orientation(section: list, n: int) -> tuple:    # Function to dynamically define circuit component orientation: 'up', 'right', 'down', 'left'
#     temp1 = ['up', 'right', 'down', 'left']
#     temp2 = []
#     if n % 2 != 0:
#         section.append('l')
#         n += 1
#     if n % 2 == 0:
#         if n % 4 == 0:
#             for i in range(4):
#                 for j in range(n // 4):
#                     temp2.append(temp1[i])
#         else:
#             for i in range(4):
#                 for j in range((n-2) // 4):
#                     temp2.append(temp1[i])
#
#             temp2.insert((n-2) // 4, 'right')
#             temp2.append('left')
#     return section, temp2


# def plot_r_basis():
#     width = 1
#     length = 1
#     height = np.linspace(10, 0.1, 1000)
#     h_l = height / length
#
#     r_m = 1 / (mu0 * (width / 2 / length + 2 / np.pi * (
#                 1 + np.log(np.pi * height / 4 / length))))
#
#     combined = np.vstack((h_l, r_m)).T
#     print(combined)
#     fig, ax = plt.subplots()  # Create a figure containing a single axes.
#     plt.title("R_basic vs h/l")
#     plt.xlabel("h/l")
#     plt.ylabel("R_basic")
#     ax.plot(h_l, r_m)
#     ax.invert_xaxis()
#     ax.grid()
#     plt.show()


# def plot_error():
#     fem_ind = np.array([116.0773e-6, 32.1e-6, 18.71e-6, 6.08575e-6, 4.324969e-6,  3.81392e-6, 2.345389e-6])
#     cal_ind = np.array([116.518e-6, 32.12472e-6, 18.72275e-6, 6.25557e-6, 4.2895602e-6, 3.611239e-6, 0.71733329e-6])
#     air_gap_l = np.array([0.0001, 0.0005, 0.001, 0.005, 0.00833, 0.01, 0.02])
#     h_by_l = ((0.0295 - air_gap_l) / 2) / air_gap_l
#     error = ((fem_ind - cal_ind) / fem_ind) * 100
#     fig, ax = plt.subplots()  # Create a figure containing a single axes.
#     plt.title("inductance vs h/l")
#     plt.xlabel("h/l")
#     plt.ylabel("Error in %")
#     # ax.plot(h_by_l, fem_ind, h_by_l, cal_ind)
#     ax.plot(h_by_l, error)
#     # ax.invert_xaxis()
#     ax.grid()
#     plt.show()


# def draw_schematic(self):

# print('Section:', self.section)
# print('Orientation:', self.orientation)
# print('List of length:', self.length)
# print('List of cross-section area:', self.area)
# print('List of reluctance:', self.reluctance)
# print('Inductance:', self.L)

# schemdraw.theme('monokai')
# d = schemdraw.Drawing()
# for i in range(len(self.section)):
#     if self.section[i] == 9:
#         d += getattr(elm.SourceV().dot().label(str(round(self.reluctance[i], 2)) + ' AT'), self.orientation[i])
#     elif self.section[i] == 'l':
#         d += getattr(elm.Line().dot(), self.orientation[i])
#     elif self.section[i] == 6 or self.section[i] == 7 or self.section[i] == 8:
#         d += getattr(elm.ResistorIEC().dot().label(str(round(self.reluctance[i], 2)) + ' AT/Wb'), self.orientation[i])
#     else:
#         d += getattr(elm.Resistor().dot().label(str(round(self.reluctance[i], 2)) + ' AT/Wb'), self.orientation[i])
#
# d.draw()
# d.save('my_circuit.svg')

# Air_gap_length = [1.00000000e-07, 4.08261224e-04, 8.16422449e-04, 1.22458367e-03,
#  1.63274490e-03, 2.04090612e-03, 2.44906735e-03, 2.85722857e-03,
#  3.26538980e-03, 3.67355102e-03, 4.08171224e-03, 4.48987347e-03,
#  4.89803469e-03, 5.30619592e-03, 5.71435714e-03, 6.12251837e-03,
#  6.53067959e-03, 6.93884082e-03, 7.34700204e-03, 7.75516327e-03,
#  8.16332449e-03, 8.57148571e-03, 8.97964694e-03, 9.38780816e-03,
#  9.79596939e-03, 1.02041306e-02, 1.06122918e-02, 1.10204531e-02,
#  1.14286143e-02, 1.18367755e-02, 1.22449367e-02, 1.26530980e-02,
#  1.30612592e-02, 1.34694204e-02, 1.38775816e-02, 1.42857429e-02,
#  1.46939041e-02, 1.51020653e-02, 1.55102265e-02, 1.59183878e-02,
#  1.63265490e-02, 1.67347102e-02, 1.71428714e-02, 1.75510327e-02,
#  1.79591939e-02, 1.83673551e-02, 1.87755163e-02, 1.91836776e-02,
#  1.95918388e-02, 2.00000000e-02]
#
# FEM_inductance = [[5.25733873e-04],
#  [3.56509342e-05],
#  [1.96273371e-05],
#  [1.38607988e-05],
#  [1.08431919e-05],
#  [8.96908451e-06],
#  [7.68081665e-06],
#  [6.73635898e-06],
#  [6.00979154e-06],
#  [5.42909853e-06],
#  [4.95256678e-06],
#  [4.55325727e-06],
#  [4.21369509e-06],
#  [3.92151073e-06],
#  [3.66711744e-06],
#  [3.44366581e-06],
#  [3.24587203e-06],
#  [3.06932936e-06],
#  [2.91034587e-06],
#  [2.76613127e-06],
#  [2.63475469e-06],
#  [2.51460888e-06],
#  [2.40401003e-06],
#  [2.30159406e-06],
#  [2.20646338e-06],
#  [2.11756703e-06],
#  [2.03425524e-06],
#  [1.95578553e-06],
#  [1.88179771e-06],
#  [1.81227984e-06],
#  [1.74712510e-06],
#  [1.68603210e-06],
#  [1.62871517e-06],
#  [1.57488291e-06],
#  [1.52419216e-06],
#  [1.47629414e-06],
#  [1.43075069e-06],
#  [1.38734476e-06],
#  [1.34601111e-06],
#  [1.30665534e-06],
#  [1.26911897e-06],
#  [1.23328032e-06],
#  [1.19909825e-06],
#  [1.16647940e-06],
#  [1.13532254e-06],
#  [1.10558445e-06],
#  [1.07726437e-06],
#  [1.05039705e-06],
#  [1.02504119e-06],
#  [1.00107838e-06]]