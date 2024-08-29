# Imports
from phyphox.data_getter import get_phyphox_data
from data.equipment import turn_table_information
from dataclasses import dataclass
from matplotlib import pyplot as plt
import numpy as np
from copy import copy


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

    # Total error on the angular velocity
    total_error: float = 0

    def __post_init__(self):
        self.theoretical_speed = turn_table_information.get(str(self.speed_setting)).get(orientation)
        self.theoretical_speed_error = turn_table_information.get(str(self.speed_setting)).get('error')


my_data = get_phyphox_data("day_2")

# print(my_data[1].data_points() / my_data[1].duration())
# print(my_data[1].data_points(), my_data[1].duration())

plot_data = []

for i, data in enumerate(my_data):
    # Remove the first and last second from the gyroscope data
    data.set_time_window(1, data.duration() - 1)

    # Store 'metadata'
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

    # Create new plot data instance and do the regression
    new_plot_data = PlotData(orientation, speed)
    fit_data = data.linear_fit('z')

    new_plot_data.measured_speed = fit_data[0][1] * 180 / 3.141
    new_plot_data.slope = fit_data[0][0] * 180 / 3.141

    new_plot_data.measured_speed_error = fit_data[1][1] * 180 / 3.141
    new_plot_data.slope_error = fit_data[1][0] * 180 / 3.141

    # Compute the total error and set it on the plot data instance
    total_error = np.sqrt(new_plot_data.measured_speed_error ** 2 + (data.duration() * new_plot_data.slope_error ** 2))
    new_plot_data.total_error = total_error

    plot_data.append(new_plot_data)

    # print(i, data.name, new_plot_data.measured_speed_error, '-->', new_plot_data.total_error)


# plt.hist([pd.slope for pd in plot_data], bins=50)

# my_data[42].plot('z', True, False)
# plt.savefig('preliminary_fit_demo.jpg')
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


# reproduce_residuals_measured_minus_provided_plot()


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


# reproduce_initial_phyphox_plot()


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


# reproduce_zoomed_in_plot()


# Try to assess the impact of the earth's rotation using out mobile gyroscope data
# Idea:
# 1) Do a linear regression (technically we should use ODR-Regression for this) on the cw and ccw values
# separately (exclude 18 and start at 2 or 3 (more 'constant' values)
# 2) Compute the slope for both directions and compare them (take care of the signs)
# 3) Somehow (is there a useful formula?) compute the earths rotation from that


def assess_earths_rotation():
    # Split the data by orientation
    pd_ccw = [pd for pd in plot_data if pd.orientation == 'ccw']
    pd_cw = [pd for pd in plot_data if pd.orientation == 'cw']

    # Remove the values for 18 degrees and start at 3 degrees (the lower bound still has to be give more thought)
    # We use 2.5 here, since the velocities for setting three are lower than 3.
    speed_limit = 3.5
    pd_ccw = [pd for pd in pd_ccw if pd.theoretical_speed > speed_limit and pd.speed_setting != 18]
    pd_cw = [pd for pd in pd_cw if pd.theoretical_speed > speed_limit and pd.speed_setting != 18]

    # Create lists with the x and y values
    x_ccw = [val.theoretical_speed for val in pd_ccw]
    y_ccw = [val.measured_speed for val in pd_ccw]

    x_cw = [val.theoretical_speed for val in pd_cw]
    y_cw = [val.measured_speed for val in pd_cw]

    # Compute the slope
    # Perform linear regression using numpy's polyfit (1st degree polynomial)
    slope_ccw, intercept_ccw = np.polyfit(x_ccw, y_ccw, 1)
    slope_cw, intercept_cw = np.polyfit(x_cw, y_cw, 1)

    print(f"Slope for CCW: {slope_ccw}, Slope for CW: {slope_cw}")
    print(f"Intercept for CCW: {intercept_ccw}, Intercept for CW: {intercept_cw}")

    # print(slope_cw, slope_ccw)
    print(intercept_cw - intercept_ccw)

    plt.scatter(-1 * np.array(x_ccw), y_ccw)
    plt.plot(np.array([-21, 0]), slope_ccw * np.array([21, 0]) + np.array(intercept_ccw))

    plt.scatter(np.array(x_cw), y_cw)
    plt.plot(np.array([21, 0]), slope_cw * np.array([21, 0]) + np.array(intercept_cw))
    plt.grid()
    plt.show()

    return None


assess_earths_rotation()
