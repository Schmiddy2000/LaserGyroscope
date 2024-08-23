# Imports
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from copy import copy
from pathlib import Path


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

    # Possible improvements:
    # - Add lists for titles, axis descriptions, etc. to make the code less repetitive
    def plot(self, axis: str):
        # Check if 'axis' is 'all'
        if axis == 'all':
            axis = 'xyza'

        # Validate the 'axis' input
        valid_axes = {'x', 'y', 'z', 'a'}
        if any(char not in valid_axes for char in axis):
            raise ValueError("Invalid character in axis. Allowed characters are 'x', 'y', 'z', and 'a'.")
        if len(set(axis)) != len(axis):
            raise ValueError("Duplicate characters in axis. Each axis should only be specified once.")

        # Compute the number of plots that need to be drawn
        num_plots = len(axis)

        # Create a 2x2 grid for plotting
        fig = plt.figure(figsize=(12, 8))

        for i, ax in enumerate(axis):
            if num_plots == 3 and i == 2:  # Special case: third plot spans entire bottom row
                ax_idx = plt.subplot2grid((2, 2), (1, 0), colspan=2)
            else:
                ax_idx = plt.subplot2grid((2, 2), divmod(i, 2))

            if ax == 'x':
                ax_idx.plot(self.time_data(), self.x_data())
                ax_idx.set_title('Gyroscope X Data')
                ax_idx.set_xlabel('Time (s)')
                ax_idx.set_ylabel('X (rad/s)')
            elif ax == 'y':
                ax_idx.plot(self.time_data(), self.y_data())
                ax_idx.set_title('Gyroscope Y Data')
                ax_idx.set_xlabel('Time (s)')
                ax_idx.set_ylabel('Y (rad/s)')
            elif ax == 'z':
                ax_idx.plot(self.time_data(), self.z_data())
                ax_idx.set_title('Gyroscope Z Data')
                ax_idx.set_xlabel('Time (s)')
                ax_idx.set_ylabel('Z (rad/s)')
            elif ax == 'a':
                ax_idx.plot(self.time_data(), self.absolute_data())
                ax_idx.set_title('Absolute Gyroscope Data')
                ax_idx.set_xlabel('Time (s)')
                ax_idx.set_ylabel('Absolute (rad/s)')

        plt.tight_layout()
        plt.show()
