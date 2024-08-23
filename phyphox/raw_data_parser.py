# Imports
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from copy import copy
from pathlib import Path
from scipy.optimize import curve_fit


# Class to store the data and to provide the functionalities for access and visualization
# Possible improvements:
# - Add a fit function, which can then also be used in the plot function
class PhyPhoxData:
    def __init__(self, folder_path: str | Path):
        # Save the path to the folder in case the metadata is needed later on
        self.folder_path = folder_path

        # Store the name of the file and check the data type
        if isinstance(folder_path, str):
            self.name = folder_path.split("/")[-1]
        elif isinstance(folder_path, Path):
            self.name = folder_path.parts[-1]
        else:
            print("folder_name has to be of type string or Path")
            exit(1)

        # Store the raw data as a dataframe
        if isinstance(folder_path, str):
            self.data = pd.read_csv(folder_path + "/Raw Data.csv")
        elif isinstance(folder_path, Path):
            self.data = pd.read_csv(folder_path / "Raw Data.csv")

    def duration(self):
        return np.max(self.data['Time (s)'].to_numpy())

    def data_points(self):
        return self.data.shape[0]

    def columns(self):
        return self.data.columns.tolist()

    def get_dataframe(self):
        return copy(self.data)

    def time_data(self):
        return self.data['Time (s)'].to_numpy()

    def x_data(self):
        return self.data['Gyroscope x (rad/s)'].to_numpy()

    def y_data(self):
        return self.data['Gyroscope y (rad/s)'].to_numpy()

    def z_data(self):
        return self.data['Gyroscope z (rad/s)'].to_numpy()

    def absolute_data(self):
        return self.data['Absolute (rad/s)'].to_numpy()

    def axis_data(self, axis: str) -> np.array:
        if axis == 't':
            return self.time_data()
        elif axis == 'x':
            return self.x_data()
        elif axis == 'y':
            return self.y_data()
        elif axis == 'z':
            return self.z_data()
        elif axis == 'a':
            return self.absolute_data()
        else:
            raise ValueError(f"Parameter axis is {axis}, but should be one of 't', 'x', 'y', 'z' or 'a'.")

    def set_time_window(self, start_time: float, end_time: float, reset_time: bool = True):
        """
        Set the data to only a portion of the initial duration.

        Parameters:
        - start_time: float, the beginning of the time window (in seconds).
        - end_time: float, the end of the time window (in seconds).
        - return: bool, if True, resets the time to start from 0 within the window.
        """

        # Filter the data based on the time window
        mask = (self.data['Time (s)'] >= start_time) & (self.data['Time (s)'] <= end_time)
        self.data = self.data.loc[mask].reset_index(drop=True)

        # Optionally reset the time to start from 0
        if reset_time:
            self.data['Time (s)'] -= start_time

        # Optional: You could return the filtered DataFrame if needed
        return self.data

    def linear_fit(self, x_column: str, y_column: str):
        """
        Perform a linear fit to the specified data columns using SciPy.

        Parameters:
        - x_column: str, the name of the column to use as the independent variable (x-axis).
        - y_column: str, the name of the column to use as the dependent variable (y-axis).

        Returns:
        - popt: tuple, the slope and intercept of the linear fit.
        - pcov: 2x2 array, the estimated covariance of popt.
        """
        x_data = self.axis_data(x_column)
        y_data = self.axis_data(y_column)

        # Define a linear function
        def linear_model(x, m, b):
            return m * x + b

        # Perform the curve fitting
        popt, pcov = curve_fit(linear_model, x_data, y_data)

        # popt contains [slope, intercept], pcov is the covariance matrix
        return popt, pcov

    # Enhance the automatic layout for less than 4 plots
    # Enhance the fitting functions
    def plot(self, axis: str, fit: bool = False):
        if axis == 'all':
            axis = 'xyza'

        valid_axes = {'x', 'y', 'z', 'a'}
        if any(char not in valid_axes for char in axis):
            raise ValueError("Invalid character in axis. Allowed characters are 'x', 'y', 'z', and 'a'.")
        if len(set(axis)) != len(axis):
            raise ValueError("Duplicate characters in axis. Each axis should only be specified once.")

        num_plots = len(axis)
        fig = plt.figure(figsize=(12, 8))

        for i, ax in enumerate(axis):
            if num_plots == 3 and i == 2:
                ax_idx = plt.subplot2grid((2, 2), (1, 0), colspan=2)
            else:
                ax_idx = plt.subplot2grid((2, 2), divmod(i, 2))

            # Get the data to be plotted
            time_data = self.time_data()
            y_data = self.axis_data(ax)

            # Create the actual plot
            ax_idx.plot(time_data, y_data, label='Data')
            ax_idx.set_title(f'Gyroscope {ax.upper()} Data')
            ax_idx.set_xlabel('Time (s)')
            ax_idx.set_ylabel(f'{ax.upper()} (rad/s)')

            if fit:
                # Perform the linear fit
                popt, pcov = self.linear_fit('t', ax)
                slope, intercept = popt

                # Calculate the fit line
                fit_line = slope * time_data + intercept

                # Calculate uncertainty bounds
                perr = np.sqrt(np.diag(pcov))
                lower_bound = fit_line - perr[0] * time_data - perr[1]
                upper_bound = fit_line + perr[0] * time_data + perr[1]

                # Plot the fit line
                ax_idx.plot(time_data, fit_line, color='red', label=f'Fit: y={slope:.3f}x + {intercept:.3f}')
                ax_idx.fill_between(time_data, lower_bound, upper_bound, color='red', alpha=0.3, label='Uncertainty')

            ax_idx.legend()

        plt.tight_layout()
        plt.show()
