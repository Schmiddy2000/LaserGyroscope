# Imports
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from copy import copy


# Path to the test folder
folder_path_: str = "/Users/lucas1/Downloads/Gyroskop Drehrate 2024-08-20 21-51-53"


# Class to store the data and to provide the functionalities for access and visualization
class PhyPhoxData:
    def __init__(self, folder_path: str):
        # Safe the path to the folder in case the metadata is needed later on
        self.folder_path = folder_path

        # Store the raw data as a dataframe
        self.data = pd.read_csv(folder_path + "/Raw Data.csv")

    def experiment_duration(self):
        return np.max(self.data['Time (s)'].to_numpy())

    def data_points(self):
        return self.data.shape[0]

    def columns(self):
        return self.data.columns.tolist()

    def get_dataframe(self):
        return copy(self.data)

    def get_time_data(self):
        return self.data['Time (s)'].to_numpy()

    def get_x_data(self):
        return self.data['Gyroscope x (rad/s)'].to_numpy()

    def get_y_data(self):
        return self.data['Gyroscope y (rad/s)'].to_numpy()

    def get_z_data(self):
        return self.data['Gyroscope z (rad/s)'].to_numpy()

    def get_absolute_data(self):
        return self.data['Absolute (rad/s)'].to_numpy()

    def plot_data(self, axis: str):
        # Set up the plot here. Use subplots depending on the length of 'axis'.

        if 'x' in axis:
            plt.plot(self.get_time_data(), self.get_x_data())
            plt.show()

 
# Small demonstration
my_data = PhyPhoxData(folder_path_)

# print(my_data.plot_data('x'))
