# Imports
import numpy as np
from matplotlib import pyplot as plt
from data.day_2 import *
from data.equipment import turn_table_information
import data.day_1 as d


# Formula: \Delta \nu_rot = \beta * \omega


def get_beta(delta_nu: float, velocity: str, orientation: str) -> float:
    degrees_per_second = turn_table_information.get(velocity).get(orientation)

    return degrees_per_second


v1 = np.array(laser_velocities_2 + laser_velocities_3)
cw_h1 = np.array(cw_highest_2 + cw_highest_3)
ccw_h1 = np.array(ccw_highest_2 + ccw_highest_3)

plt.scatter(d.laser_velocities, d.cw_highest, label='cw')

# plt.scatter(v1, cw_h1 - 25000, label='cw')
# plt.scatter(-v1, -ccw_h1 + 25000, label='ccw')
# plt.scatter(v1, cw_h1 - ccw_h1, label='cw - ccw')
# plt.ylim(0, 35000)
plt.legend()
plt.show()
