# Imports
import numpy as np

# Mirror distances
l_1 = 417
l_2 = 416
l_3 = 419
L = l_1 + l_2 + l_3
s = L / 2

# Errors on the parameters above
delta_l = 2.48
delta_L = 4.3
delta_s = delta_L / 2

# Wave length
_lambda = 0.6328 / 1000

# Area of the triangle
F = np.sqrt(s * (s - l_1) * (s - l_2) * (s - l_3))

print('F (mm^2):', F)


# Derivatives of the formula for the area
def dF_ds():
    derivative = (F ** 2 / s + F ** 2 / (s - l_3) + F ** 2 / (s - l_2) + F ** 2 / (s - l_1)) / (2 * F)
    return derivative


def dF_dl1():
    derivative = -(s * (s - l_2) * (s - l_3)) / (2 * np.sqrt(s * (s - l_1) * (s - l_2) * (s - l_3)))
    return derivative


def dF_dl2():

    derivative = -(s * (s - l_1) * (s - l_3)) / (2 * np.sqrt(s * (s - l_1) * (s - l_2) * (s - l_3)))
    return derivative


def dF_dl3():
    derivative = -(s * (s - l_1) * (s - l_2)) / (2 * np.sqrt(s * (s - l_1) * (s - l_2) * (s - l_3)))
    return derivative


# Error on the area
delta_F = np.sqrt((dF_ds() * delta_s) ** 2 + (dF_dl1() * delta_l) ** 2 + (dF_dl2() * delta_l) ** 2 + (dF_dl2() * delta_l) ** 2)

print('delta_F (unit?):', delta_F / 100)


# Scaling factor beta
beta = 4 * F / (L * _lambda)

print('beta (Hz / grad):', beta * np.pi / 180)


# Derivatives of the scaling factor
def dBeta_dF():
    derivative = 4 / (L * _lambda)
    return derivative


def dBeta_dL():
    derivative = - 4 * F / (L ** 2 * _lambda)
    return derivative


# Error on the scaling factor
delta_beta = np.sqrt((dBeta_dF() * delta_F) ** 2 + (dBeta_dL() * delta_L) ** 2)

print('delta_beta (Hz / grad):', delta_beta * np.pi / 180)
