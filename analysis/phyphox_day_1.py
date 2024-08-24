# Imports
from phyphox.data_getter import get_phyphox_data
from data.equipment import turn_table_information
from dataclasses import dataclass
from matplotlib import pyplot as plt
import numpy as np


# Maybe add a speed_setting for 0.1, 0.2, ... Then theoretical speed would be 'independent'
@dataclass
class PlotData:
    # This represents the 'metadata' of the measurement
    orientation: str
    speed_setting: float | int
    theoretical_speed: float | int = 0
    theoretical_speed_error: float = 0

    # Stores the linear regression parameters
    slope: float = 0
    measured_speed: float = 0

    # Errors on the linear regression parameters
    slope_error: float = 0
    measured_speed_error: float = 0

    def __post_init__(self):
        self.theoretical_speed = turn_table_information.get(str(self.speed_setting)).get(orientation)
        self.theoretical_speed_error = turn_table_information.get(str(self.speed_setting)).get('error')


my_data = get_phyphox_data("day_2")

print(my_data[1].data_points() / my_data[1].duration())
print(my_data[1].data_points(), my_data[1].duration())

plot_data = []

for i, data in enumerate(my_data):
    data.set_time_window(1, data.duration() - 1)
    name = data.name
    orientation = name.split('_')[-2]
    speed = name.split('_')[-1]

    if speed[0] == '0':
        speed = float(speed) / 10
    else:
        # Handle the case where speed is 1 or 2 differently due to how the turn table information is defined
        if speed == '1' or speed == '2':
            speed = float(speed)
        else:
            speed = int(speed)

    new_plot_data = PlotData(orientation, speed)
    fit_data = data.linear_fit('z')

    new_plot_data.measured_speed = fit_data[0][1] * 180 / 3.141
    new_plot_data.slope = fit_data[0][0] * 180 / 3.141

    new_plot_data.measured_speed_error = fit_data[1][1] * 180 / 3.141
    new_plot_data.slope_error = fit_data[1][0] * 180 / 3.141

    plot_data.append(new_plot_data)

    print(i, data.name, new_plot_data.slope)


# plt.hist([pd.slope for pd in plot_data], bins=50)

my_data[42].plot('z', True, False)
plt.savefig('preliminary_fit_demo.jpg')
# plt.show()


x_data = [pd.theoretical_speed if pd.orientation == 'cw' else -pd.theoretical_speed for pd in plot_data]
speed_setting_data = [pd.speed_setting if pd.orientation == 'cw' else -pd.speed_setting for pd in plot_data]
y_data = [pd.measured_speed for pd in plot_data]
y_err = [pd.measured_speed_error for pd in plot_data]
x_err = [pd.theoretical_speed_error for pd in plot_data]


def reproduce_residuals_measured_minus_provided_plot():
    plt.figure(figsize=(12, 6), dpi=200)
    plt.title('Residuals of the measured speeds (Measured minus Provided)')
    plt.ylabel("Measured - Provided speeds [°/s]")
    plt.xlabel("Speed setting [no units]")

    plt.scatter(speed_setting_data, np.array(y_data) - np.array(x_data), s=15, label='Residuals')

    # What would the real errors look like for this plot?
    # plt.errorbar(x_data, y_data, y_err, x_err, fmt='none', capsize=7, elinewidth=0.75, capthick=0.75, label='Errors')

    plt.grid()
    # plt.xlim(-5, 5)
    plt.ylim(-3, 3)
    plt.legend()
    plt.subplots_adjust(top=0.95, bottom=0.1, left=0.1, right=0.95)

    plt.savefig('phyphox_residuals_measured_minus_provided.jpg')
    # plt.show()

    return None


reproduce_residuals_measured_minus_provided_plot()


def reproduce_initial_phyphox_plot():
    plt.figure(figsize=(12, 6), dpi=200)
    plt.title('Provided against measured angular speeds')
    plt.xlabel("Provided angular speeds in [°/s]")
    plt.ylabel("Measured angular speeds in [°/s]")

    plt.scatter(x_data, y_data, s=5, label='Data points')
    plt.errorbar(x_data, y_data, y_err, x_err, fmt='none', capsize=5, elinewidth=0.5, capthick=0.5, label='Errors')
    plt.grid()
    plt.legend()
    plt.subplots_adjust(top=0.95, bottom=0.1, left=0.1, right=0.95)

    plt.savefig('phyphox_measure_vs_provided_angular_speeds.jpg')
    # plt.show()

    return None


reproduce_initial_phyphox_plot()


# Plot that zooms in on the central area to see the possible lock-in effect.
def reproduce_zoomed_in_plot():
    plt.figure(figsize=(12, 6), dpi=200)
    plt.title('Enlarged center of provided against measured angular speeds')
    plt.xlabel("Provided angular speeds in [°/s]")
    plt.ylabel("Measured angular speeds in [°/s]")

    plt.scatter(x_data, y_data, s=15, label='Data points')
    plt.errorbar(x_data, y_data, y_err, x_err, fmt='none', capsize=7, elinewidth=0.75, capthick=0.75, label='Errors')
    plt.grid()
    plt.xlim(-5, 5)
    plt.ylim(-5, 5)
    plt.legend()
    plt.subplots_adjust(top=0.95, bottom=0.1, left=0.1, right=0.95)

    plt.savefig('phyphox_measure_vs_provided_angular_speeds_zoomed_in.jpg')
    # plt.show()

    return None


reproduce_zoomed_in_plot()
