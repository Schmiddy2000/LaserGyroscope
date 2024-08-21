# Imports
import numpy as np
from phyphox.raw_data_parser import PhyPhoxData
from typing import List


# Beat frequency measurements
laser_velocities = [1, 2, 3, 4, 6, 8, 10, 12, 14]

cw_highest = [15800, 8430, 2890, 20720, 15710, 20320, 12840, 31910, 27130]
ccw_highest = [9830, 8490, 5560, 15800, 23160, 36260, 15440, 33930, 36050]

cw_lowest = [10180, 3370, 90, 12780, 10160, 12220, 6350, 16860, 14940]
ccw_lowest = [7200, 5100, 90, 11240, 19320, 0, 9370, 27410, 0]


# Mobile phone gyroscope measurements
mobile_velocities = []

mobile_measurement_file_names = []

mobile_gyroscope_data: List[PhyPhoxData] = []
