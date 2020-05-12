from array import *

from prettytable import PrettyTable
import matplotlib.pyplot as plt
import numpy as np
import serial



# Константы
EPS = 2
mass_karetka = 0.047
mass_shaiba = 0.220
mass_gruz = 0.408
l_1 = 5.7
l_0 = 2.5
b = 4.0
d = 0.046
h = 0.7
g = 9.81908
humanDelayTime = 0.13
I_0 = 0.011541518
M_tr_a = 0.003179657
M_tr_b = 0.000950262
moments_tr = [-0.00228920, 0.00998837, 0.00906186, 0.01317346, 0.01499408, 0.01614266]
mass_gruz_array = [0.69, 0.91, 1.13, 1.35]
R_arr = [0.08, 0.1, 0.13, 0.15, 0.18, 0.2]

# =====================================================================================================================

def showPlot(x_, y_):
    plt.figure()
    plt.plot(x_, y_)
    plt.show()


def a(t):
    global h
    return (2.0 * h) / (t * t)


def e(t):
    global h
    global d
    return (4.0 * h) / (d * t * t)


def M(m, t):
    global g
    global d
    global h
    return (m * g * d) / 2.0 - (m * d * h) / (t * t)


# =======================================================================================================================


mass = 4
reika = 6
num = 3



data_in = [
    [[4.41, 4.46, 4.44], [5.84, 5.84, 5.97], [7.07, 7.00, 7.06], [7.97, 8.06, 8.07], [9.50, 9.22, 9.31], [10.28, 10.13, 10.37]],
    [[3.16, 3.28, 3.25], [4.09, 4.16, 4.18], [4.04, 5.00, 5.28], [5.72, 5.69, 5.64], [6.40, 6.31, 6.28], [7.25, 7.13, 7.28]],
    [[2.81, 2.72, 2.72], [3.39, 3.46, 3.35], [4.06, 4.13, 4.06], [4.56, 4.69, 4.63], [5.15, 5.19, 5.19], [5.81, 5.81, 5.81]],
    [[2.40, 2.34, 2.47], [3.00, 2.91, 2.97], [3.56, 3.59, 3.64], [3.93, 4.03, 3.98], [4.53, 4.47, 4.43], [5.03, 4.97, 4.94]]
]

data_average_time = [[0.0 for x in range(reika)] for x in range(mass)]
I_y = []

t = 0.0
for i in range(len(data_in)):
    for j in range(len(data_in[i])):
        t = 0.0
        for k in range(len(data_in[i][j])):
            t = t + data_in[i][j][k]

        data_average_time[i][j] = t / 3


data_a_e_M = [[[0.0 for x in range(3)] for x in range(reika)] for x in range(mass)]

for i in range(len(data_a_e_M)):
    for j in range(len(data_a_e_M[i])):
        data_a_e_M[i][j][0] = a(data_average_time[i][j])
        data_a_e_M[i][j][1] = e(data_average_time[i][j])
        data_a_e_M[i][j][2] = M(mass_gruz_array[i], data_average_time[i][j])


# =====================================================================================================================
# График 1

M_x = [[0.0 for x in range(mass)] for x in range(reika)]
eps_y = [[0.0 for x in range(mass)] for x in range(reika)]

for i in range(reika):
    for j in range(mass):
        M_x[i][j] = data_a_e_M[j][i][1]
        eps_y[i][j] = data_a_e_M[j][i][2]




def add_plot1(x, y):
    x_ = 0.0
    y_ = 0.0
    for xi in x:
        x_ = x_ + xi
    for yi in y:
        y_ = y_ + yi

    x_ = x_ / len(x)
    y_ = y_ / len(y)


    t1 = 0.0
    b = 0.0
    for i in range(len(x)):
        t1 = t1 + (x[i] - x_) ** 2

    for i in range(len(x)):
        b = b + (x[i] - x_) * (y[i] - y_) / t1

    a = y_ - b * x_

    #=====
    I_y.append(b)
    # =====

    y_out1 = []
    for xi in x:
        y_out1.append(a + b * xi)

    # !!! Раскоментировать, чтобы показать 1 график
    plt.plot(x, y_out1)


for i in range(reika):
   add_plot1(M_x[i], eps_y[i])

plt.xlabel('eps')
plt.ylabel('M(eps)')
plt.grid()
# !!! Раскоментировать, чтобы показать 1 график
plt.show()

# =====================================================================================================================
# График 2


def add_plot2(x, y):
    x_ = 0.0
    y_ = 0.0
    for xi in x:
        x_ = x_ + xi
    for yi in y:
        y_ = y_ + yi

    x_ = x_ / len(x)
    y_ = y_ / len(y)


    t1 = 0.0
    b = 0.0
    for i in range(len(x)):
        t1 = t1 + (x[i] - x_) ** 2

    for i in range(len(x)):
        b = b + (x[i] - x_) * (y[i] - y_) / t1

    a = y_ - b * x_


    y_out1 = []
    for xi in x:
        y_out1.append(a + b * xi)

    plt.plot(x, y_out1)


R_x = []

for i in range(len(R_arr)):
    R_x.append(R_arr[i] ** 2)


print()

add_plot2(R_x, I_y)

plt.xlabel('R^2')
plt.ylabel('I')
plt.grid()
plt.show()