from array import *

from prettytable import PrettyTable
import matplotlib.pyplot as plt
import io
import numpy as np
import serial



# Константы
EPS = 2
m0 = 0.047
delta_m0 = 0.0005
m_shaiba = 0.220
delta_m_shaiba = 0.0005
m_gruz = 0.408
delta_m_gruz = 0.0005
l_1 = 5.7
l_0 = 2.5
b = 4.0
d = 0.046
delta_d = 0.0005
h = 0.7
delta_h = 0.0
g = 9.81908
humanDelayTime = 0.13
I_0 = 0.011541518
M_tr_a = 0.003179657
M_tr_b = 0.000950262
moments_tr = [-0.00228920, 0.00998837, 0.00906186, 0.01317346, 0.01499408, 0.01614266]
mass_gruz_array = [0.267, 0.487, 0.707, 0.927]
R_arr = [0.08, 0.1, 0.13, 0.15, 0.18, 0.2]

# Глобальные
data_from_arduino = [[[]]]
data_a_e_M = [[]]
data_delta_t_a_e_M = [[]]

a_plot_2 = 0
b_plot_2 = 0

a_plot_1 = [0, 0, 0, 0, 0, 0]
b_plot_1 = [0, 0, 0, 0, 0, 0]

def plots(data_in):
    global data_from_arduino
    global data_a_e_M

    graphs = [io.BytesIO(), io.BytesIO()]

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

    # ========================================= График 1 =========================================

    M_x = [[0.0 for x in range(mass)] for x in range(reika)]
    eps_y = [[0.0 for x in range(mass)] for x in range(reika)]
    count = 1

    for i in range(reika):
        for j in range(mass):
            M_x[i][j] = data_a_e_M[j][i][1]
            eps_y[i][j] = data_a_e_M[j][i][2]

    def add_plot1(x, y, count):
        global a_plot_1
        global b_plot_1

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

        # =====
        I_y.append(b)
        # =====

        y_out1 = []
        for xi in x:
            y_out1.append(a + b * xi)

        plt.plot(x, y_out1)
        plt.text(x[-1] + 0.1, y_out1[-1], str(count), fontsize=11)
        a_plot_1[count - 1] = a
        b_plot_1[count - 1] = b

    plt.cla()
    for i in range(reika):
        add_plot1(M_x[i], eps_y[i], count)
        count = count + 1
        plt.scatter(M_x[i], eps_y[i], color='orange', s=20, marker='o')

    plt.xlabel('ε, рад/с^2 ')
    plt.ylabel('M(ε), Н*м')
    plt.title('График 1    M(ε)', fontsize=15)
    plt.grid(True)

    # plt.show()
    plt.savefig(graphs[0], format='png')

    plt.cla()
    print()

    # ========================================= График 2 ========================================


    def add_plot2(x, y):
        global a_plot_2
        global b_plot_2

        x_ = 0.0
        y_ = 0.0
        for xi in x:
            x_ = x_ + xi
        for yi in y:
            y_ = y_ + yi

        x_ = x_ / len(x)
        y_ = y_ / len(y)

        t1 = 0.0
        b_plot_2 = 0.0
        for i in range(len(x)):
            t1 = t1 + (x[i] - x_) ** 2

        for i in range(len(x)):
            b_plot_2 = b_plot_2 + (x[i] - x_) * (y[i] - y_) / t1

        a_plot_2 = y_ - b_plot_2 * x_

        y_out1 = []
        for xi in x:
            y_out1.append(a_plot_2 + b_plot_2 * xi)

        plt.plot(x, y_out1)

    R_x = []

    for i in range(len(R_arr)):
        R_x.append(R_arr[i] ** 2)

    print()

    plt.cla()
    add_plot2(R_x, I_y)
    plt.scatter(R_x, I_y, color='orange', s=20, marker='o')

    plt.xlabel('R^2, м^2')
    plt.ylabel('I(R^2), кг*м^2')

    plt.title('График 2    I(R^2)', fontsize=15)
    plt.grid(True)
    #plt.show()

    plt.savefig(graphs[1], format='png')

    return graphs


import datetime
import io
from array import *
from prettytable import PrettyTable
import matplotlib.pyplot as plt
import numpy as np

import serial

import logging
import threading
import time

physics_height = 0.7;
physics_Karetka = 0.047;
physics_Shaiba = 0.220;
physics_Gruz = 0.408;
physics_g = 9.81908;

COM_PORT = 4
arduino_speed = 9600
arduino_time = 0.1

stop_arduino = True
arduino_tmp_msg = ""
throw_result_time = 0.0

delta_measurement = 0.5
EMULATOR_MODE_ON = True

import pprint

n_masses = 4
n_lengths = 6
n_measurements = 3
data_from_arduino = [[[0.0 for k in range(n_measurements)] for j in range(n_lengths)] for i in range(n_masses)]

n_masses_delta = 4
n_lengths_delta = 6
n_delta = 4
data_delta_t_a_e_M = [[[0.0 for k in range(n_delta)] for j in range(n_lengths_delta)] for i in range(n_masses_delta)]

# TODO Пример!
data_from_arduino = [
    [[4.41, 4.46, 4.44], [5.84, 5.84, 5.97], [7.07, 7.00, 7.06], [7.97, 8.06, 8.07], [9.50, 9.22, 9.31],
     [10.28, 10.13, 10.37]],
    [[3.16, 3.28, 3.25], [4.09, 4.16, 4.18], [4.04, 5.00, 5.28], [5.72, 5.69, 5.64], [6.40, 6.31, 6.28],
     [7.25, 7.13, 7.28]],
    [[2.81, 2.72, 2.72], [3.39, 3.46, 3.35], [4.06, 4.13, 4.06], [4.56, 4.69, 4.63], [5.15, 5.19, 5.19],
     [5.81, 5.81, 5.81]],
    [[2.40, 2.34, 2.47], [3.00, 2.91, 2.97], [3.56, 3.59, 3.64], [3.93, 4.03, 3.98], [4.53, 4.47, 4.43],
     [5.03, 4.97, 4.94]]
]

print(data_from_arduino)

from PIL import Image

import PySimpleGUI as sg

sg.theme('SystemDefaultForReal')

measurementFrame = [
    [sg.Text('Установка: не подключена.', key="comport", size=(25, 1)),
     sg.Checkbox('Режим эмулятора', key='emulatormode', size=(20, 1), default=EMULATOR_MODE_ON, enable_events=True)],
    [
        sg.Text('Количество грузов'),
        sg.Slider(range=(1, 4), orientation='h', size=(8, 10), change_submits=True, key='sliderMass',
                  font=('Helvetica 12')),
        sg.Text('Положение утяжелителей'),
        sg.Slider(range=(1, 6), orientation='h', size=(12, 10), change_submits=True, key='sliderLength',
                  font=('Helvetica 12'))
    ],
    [
        sg.Text('1: '), sg.Text(key="r1", text=str(data_from_arduino[0][0][0])), sg.Button('Измерить', key='m1'),
        sg.Text('2: '), sg.Text(key="r2", text=str(data_from_arduino[0][0][1])), sg.Button('Измерить', key='m2'),
        sg.Text('3: '), sg.Text(key="r3", text=str(data_from_arduino[0][0][2])), sg.Button('Измерить', key='m3')
    ],
]

resultsFrame = [[sg.Button('Таблицы и графики', key='showGraphs'),
                 sg.Button('Экспортировать таблицы и графики', key='exportGraphs', enable_events=True)]]

layout = [
    [sg.Frame('Измерения', measurementFrame, font='Any 12', title_color='blue')],
    [sg.Frame('Обработка данных', resultsFrame, font='Any 12', title_color='blue')],
    [sg.Button('Ok'), sg.Button('Cancel')]
]

window = sg.Window('Маятник Обербека', layout)
measuringNow = False


def noArduinoScenario():
    print("No Arduino")


import serial.tools.list_ports


def resultWindow(data_from_arduino):
    global a_plot_1, b_plot_1, a_plot_2, b_plot_2

    graphs = plots(data_from_arduino)

    sg.theme('SystemDefaultForReal')

    layout1 = [[sg.Image(filename='', key='image1')]] \
              + [[sg.Text('1(n2 = 1):  M(ε) = (' + str(round(b_plot_1[0], 4)) + ')ε + (' + str(round(a_plot_1[0], 4)) + ')', size=(33, 1), font=("Helvetica", 13))] + [sg.Text('4(n2 = 4):  M(ε) = (' + str(round(b_plot_1[3], 4)) + ')ε + (' + str(round(a_plot_1[3], 4)) + ')', font=("Helvetica", 13))]] \
              + [[sg.Text('2(n2 = 2):  M(ε) = (' + str(round(b_plot_1[1], 4)) + ')ε + (' + str(round(a_plot_1[1], 4)) + ')', size=(33, 1), font=("Helvetica", 13))] + [sg.Text('5(n2 = 5):  M(ε) = (' + str(round(b_plot_1[4], 4)) + ')ε + (' + str(round(a_plot_1[4], 4)) + ')', font=("Helvetica", 13))]] \
              + [[sg.Text('3(n2 = 3):  M(ε) = (' + str(round(b_plot_1[2], 4)) + ')ε + (' + str(round(a_plot_1[2], 4)) + ')', size=(33, 1), font=("Helvetica", 13))] + [sg.Text('6(n2 = 6):  M(ε) = (' + str(round(b_plot_1[5], 4)) + ')ε + (' + str(round(a_plot_1[5], 4)) + ')', font=("Helvetica", 13))]] \
              # [[sg.Text('1(n2 = 4):  M(ε) = ' + str(round(b_plot_1[3], 4)) + 'ε + (' + str(round(a_plot_1[3], 4)) + ')', font=("Helvetica", 10))]] \
              #+ [[sg.Text('1(n2 = 5):  M(ε) = ' + str(round(b_plot_1[4], 4)) + 'ε + (' + str(round(a_plot_1[4], 4)) + ')', font=("Helvetica", 10))]] \
              #+ [[sg.Text('1(n2 = 6):  M(ε) = ' + str(round(b_plot_1[5], 4)) + 'ε + (' + str(round(a_plot_1[5], 4)) + ')', font=("Helvetica", 10))]] \

    layout2 = [[sg.Image(filename='', key='image2')]] + [[sg.Text('I(R^2) = (' + str(round(b_plot_2, 4)) + ')R^2 + (' + str(round(a_plot_2, 4)) + ')', font=("Helvetica", 13))]]

    # ======================= Таблица 1  =======================
    headings = ['t, c', 'n2 = 1', 'n2 = 2', 'n2 = 3', 'n2 = 4', 'n2 = 5', 'n2 = 6']
    header = [[sg.Text(h, size=(6, 1), font=("Helvetica", 14)) for h in headings]]

    # input_rows = [[sg.Text(' 1 ') for col in range(4)] for row in range(10)]
    row1_str = []
    for i in range(6):
        row1_str.append('    ' + str(data_from_arduino[0][i][0]))

    input_row1 = [[sg.Text('n1 = 1', size=(6, 1), font=("Helvetica", 14))] + [sg.Text(r, size=(7, 1), font=14) for r in row1_str]]

    row2_str = []
    for i in range(6):
        row2_str.append('    ' + str(data_from_arduino[0][i][1]))

    input_row2 = [[sg.Text(' ', size=(6, 1), font=("Helvetica", 14))] + [sg.Text(r, size=(7, 1), font=14) for r in row2_str]]

    row3_str = []
    for i in range(6):
        row3_str.append('    ' + str(data_from_arduino[0][i][2]))

    input_row3 = [[sg.Text(' ', size=(6, 1), font=("Helvetica", 14))] + [sg.Text(r, size=(7, 1), font=14) for r in row3_str]]

    # ===================================================================
    row4_str = []
    for i in range(6):
        row4_str.append('    ' + str(data_from_arduino[1][i][0]))

    input_row4 = [[sg.Text('n1 = 2', size=(6, 1), font=("Helvetica", 14))] + [sg.Text(r, size=(7, 1), font=14) for r in row4_str]]

    row5_str = []
    for i in range(6):
        row5_str.append('    ' + str(data_from_arduino[1][i][1]))

    input_row5 = [[sg.Text(' ', size=(6, 1), font=("Helvetica", 14))] + [sg.Text(r, size=(7, 1), font=14) for r in row5_str]]

    row6_str = []
    for i in range(6):
        row6_str.append('    ' + str(data_from_arduino[1][i][2]))

    input_row6 = [[sg.Text(' ', size=(6, 1), font=("Helvetica", 14))] + [sg.Text(r, size=(7, 1), font=14) for r in row6_str]]
    # ===================================================================
    row7_str = []
    for i in range(6):
        row7_str.append('    ' + str(data_from_arduino[2][i][0]))

    input_row7 = [[sg.Text('n1 = 3', size=(6, 1), font=("Helvetica", 14))] + [sg.Text(r, size=(7, 1), font=14) for r in row7_str]]

    row8_str = []
    for i in range(6):
        row8_str.append('    ' + str(data_from_arduino[2][i][1]))

    input_row8 = [[sg.Text(' ', size=(6, 1), font=("Helvetica", 14))] + [sg.Text(r, size=(7, 1), font=14) for r in row8_str]]

    row9_str = []
    for i in range(6):
        row9_str.append('    ' + str(data_from_arduino[2][i][2]))

    input_row9 = [[sg.Text(' ', size=(6, 1), font=("Helvetica", 14))] + [sg.Text(r, size=(7, 1), font=14) for r in row9_str]]

    # ===================================================================
    row10_str = []
    for i in range(6):
        row10_str.append('    ' + str(data_from_arduino[3][i][0]))

    input_row10 = [[sg.Text('n1 = 4', size=(6, 1), font=("Helvetica", 14))] + [sg.Text(r, size=(7, 1), font=14) for r in row10_str]]

    row11_str = []
    for i in range(6):
        row11_str.append('    ' + str(data_from_arduino[3][i][1]))

    input_row11 = [[sg.Text(' ', size=(6, 1), font=("Helvetica", 14))] + [sg.Text(r, size=(7, 1), font=14) for r in row11_str]]

    row12_str = []
    for i in range(6):
        row12_str.append('    ' + str(data_from_arduino[3][i][2]))

    input_row12 = [[sg.Text(' ', size=(6, 1), font=("Helvetica", 14))] + [sg.Text(r, size=(7, 1), font=14) for r in row12_str]]
    # ===================================================================

    layoutTable1 = header + input_row1 + input_row2 + input_row3 + input_row4 + input_row5 + input_row6 + input_row7 + input_row8 + input_row9 + input_row10 + input_row11 + input_row12
    # layoutTable1 = []

    # ======================= Таблица 2  =======================
    global data_a_e_M

    headings = ['a,ε,M', ' n2 = 1', ' n2 = 2', ' n2 = 3', '  n2 = 4', '   n2 = 5', '    n2 = 6']
    header = [[sg.Text(h, size=(7, 1), font=("Helvetica", 14)) for h in headings]]

    # input_rows = [[sg.Text(' 1 ') for col in range(4)] for row in range(10)]
    row1_str = []
    for i in range(6):
        row1_str.append('   ' + str(round(data_a_e_M[0][i][0], 4)))

    input_row1 = [[sg.Text('n1 = 1', size=(6, 1), font=("Helvetica", 14))] + [sg.Text(r, size=(9, 1), font=14) for r in row1_str]]

    row2_str = []
    for i in range(6):
        row2_str.append('   ' + str(round(data_a_e_M[0][i][1], 4)))

    input_row2 = [[sg.Text('  ', size=(6, 1), font=("Helvetica", 14))] + [sg.Text(r, size=(9, 1), font=14) for r in row2_str]]

    row3_str = []
    for i in range(6):
        row3_str.append('   ' + str(round(data_a_e_M[0][i][2], 4)))

    input_row3 = [[sg.Text('', size=(6, 1), font=("Helvetica", 14))] + [sg.Text(r, size=(9, 1), font=14) for r in row3_str]]

    # ===================================================================
    row4_str = []
    for i in range(6):
        row4_str.append('   ' + str(round(data_a_e_M[1][i][0], 4)))

    input_row4 = [[sg.Text('n1 = 2', size=(6, 1), font=("Helvetica", 14))] + [sg.Text(r, size=(9, 1), font=14) for r in row4_str]]

    row5_str = []
    for i in range(6):
        row5_str.append('   ' + str(round(data_a_e_M[1][i][1], 4)))

    input_row5 = [[sg.Text('', size=(6, 1), font=("Helvetica", 14))] + [sg.Text(r, size=(9, 1), font=14) for r in row5_str]]

    row6_str = []
    for i in range(6):
        row6_str.append('   ' + str(round(data_a_e_M[1][i][2], 4)))

    input_row6 = [[sg.Text('', size=(6, 1), font=("Helvetica", 14))] + [sg.Text(r, size=(9, 1), font=14) for r in row6_str]]
    # ===================================================================
    row7_str = []
    for i in range(6):
        row7_str.append('   ' + str(round(data_a_e_M[2][i][0], 4)))

    input_row7 = [[sg.Text('n1 = 3', size=(6, 1), font=("Helvetica", 14))] + [sg.Text(r, size=(9, 1), font=14) for r in row7_str]]

    row8_str = []
    for i in range(6):
        row8_str.append('   ' + str(round(data_a_e_M[2][i][1], 4)))

    input_row8 = [[sg.Text('', size=(6, 1), font=("Helvetica", 14))] + [sg.Text(r, size=(9, 1), font=14) for r in row8_str]]

    row9_str = []
    for i in range(6):
        row9_str.append('   ' + str(round(data_a_e_M[2][i][2], 4)))

    input_row9 = [[sg.Text('', size=(6, 1), font=("Helvetica", 14))] + [sg.Text(r, size=(9, 1), font=14) for r in row9_str]]

    # ===================================================================
    row10_str = []
    for i in range(6):
        row10_str.append('   ' + str(round(data_a_e_M[3][i][0], 4)))

    input_row10 = [[sg.Text('n1 = 4', size=(6, 1), font=("Helvetica", 14))] + [sg.Text(r, size=(9, 1), font=14) for r in row10_str]]

    row11_str = []
    for i in range(6):
        row11_str.append('   ' + str(round(data_a_e_M[3][i][1], 4)))

    input_row11 = [[sg.Text('', size=(6, 1), font=("Helvetica", 14))] + [sg.Text(r, size=(9, 1), font=14) for r in row11_str]]

    row12_str = []
    for i in range(6):
        row12_str.append('   ' + str(round(data_a_e_M[3][i][2], 4)))

    input_row12 = [[sg.Text('', size=(6, 1), font=("Helvetica", 14))] + [sg.Text(r, size=(9, 1), font=14) for r in row12_str]]
    # ===================================================================

    layoutTable2 = header + input_row1 + input_row2 + input_row3 + [[sg.Text('')]]  \
                   + input_row4 + input_row5 + input_row6 + [[sg.Text('')]] \
                   + input_row7 + input_row8 + input_row9 + [[sg.Text('')]] \
                   + input_row10 + input_row11 + input_row12 + [[sg.Text('')]]


    # ======================= Погрешности  =======================








    # ===================================================================
    count_all_delta()

    headings = ['∆(t,a,ε,M)', ' n2 = 1', ' n2 = 2', ' n2 = 3', '  n2 = 4', '   n2 = 5', '    n2 = 6']
    header = [[sg.Text(h, size=(7, 1), font=("Helvetica", 14)) for h in headings]]


    row1_str = []
    for i in range(6):
        row1_str.append('   ' + str(round(data_delta_t_a_e_M[0][i][0], 4)))

    input_row1 = [
        [sg.Text('n1 = 1', size=(6, 1), font=("Helvetica", 14))] + [sg.Text(r, size=(9, 1), font=10) for r in row1_str]]

    row2_str = []
    for i in range(6):
        row2_str.append('   ' + str(round(data_delta_t_a_e_M[0][i][1], 4)))

    input_row2 = [
        [sg.Text('  ', size=(6, 1), font=("Helvetica", 14))] + [sg.Text(r, size=(9, 1), font=14) for r in row2_str]]

    row3_str = []
    for i in range(6):
        row3_str.append('   ' + str(round(data_delta_t_a_e_M[0][i][2], 4)))

    input_row3 = [
        [sg.Text('', size=(6, 1), font=("Helvetica", 14))] + [sg.Text(r, size=(9, 1), font=14) for r in row3_str]]

    row3t_str = []
    for i in range(6):
        row3t_str.append('   ' + str(round(data_delta_t_a_e_M[0][i][3], 4)))

    input_row3t = [
        [sg.Text('', size=(6, 1), font=("Helvetica", 14))] + [sg.Text(r, size=(9, 1), font=14) for r in row3t_str]]

    # ===================================================================
    row4_str = []
    for i in range(6):
        row4_str.append('   ' + str(round(data_delta_t_a_e_M[1][i][0], 4)))

    input_row4 = [
        [sg.Text('n1 = 2', size=(6, 1), font=("Helvetica", 14))] + [sg.Text(r, size=(9, 1), font=14) for r in row4_str]]

    row5_str = []
    for i in range(6):
        row5_str.append('   ' + str(round(data_delta_t_a_e_M[1][i][1], 4)))

    input_row5 = [
        [sg.Text('', size=(6, 1), font=("Helvetica", 14))] + [sg.Text(r, size=(9, 1), font=14) for r in row5_str]]

    row6_str = []
    for i in range(6):
        row6_str.append('   ' + str(round(data_delta_t_a_e_M[1][i][2], 4)))

    input_row6 = [
        [sg.Text('', size=(6, 1), font=("Helvetica", 14))] + [sg.Text(r, size=(9, 1), font=14) for r in row6_str]]

    row6t_str = []
    for i in range(6):
        row6t_str.append('   ' + str(round(data_delta_t_a_e_M[0][i][2], 4)))

    input_row6t = [
        [sg.Text('', size=(6, 1), font=("Helvetica", 14))] + [sg.Text(r, size=(9, 1), font=14) for r in row6t_str]]
    # ===================================================================
    row7_str = []
    for i in range(6):
        row7_str.append('   ' + str(round(data_delta_t_a_e_M[2][i][0], 4)))

    input_row7 = [
        [sg.Text('n1 = 3', size=(6, 1), font=("Helvetica", 14))] + [sg.Text(r, size=(9, 1), font=14) for r in row7_str]]

    row8_str = []
    for i in range(6):
        row8_str.append('   ' + str(round(data_delta_t_a_e_M[2][i][1], 4)))

    input_row8 = [
        [sg.Text('', size=(6, 1), font=("Helvetica", 14))] + [sg.Text(r, size=(9, 1), font=14) for r in row8_str]]

    row9_str = []
    for i in range(6):
        row9_str.append('   ' + str(round(data_delta_t_a_e_M[2][i][2], 4)))

    input_row9 = [
        [sg.Text('', size=(6, 1), font=("Helvetica", 14))] + [sg.Text(r, size=(9, 1), font=14) for r in row9_str]]

    row9t_str = []
    for i in range(6):
        row9t_str.append('   ' + str(round(data_delta_t_a_e_M[0][i][2], 4)))

    input_row9t = [
        [sg.Text('', size=(6, 1), font=("Helvetica", 14))] + [sg.Text(r, size=(9, 1), font=14) for r in row9t_str]]

    # ===================================================================
    row10_str = []
    for i in range(6):
        row10_str.append('   ' + str(round(data_delta_t_a_e_M[3][i][0], 4)))

    input_row10 = [[sg.Text('n1 = 4', size=(6, 1), font=("Helvetica", 14))] + [sg.Text(r, size=(9, 1), font=14) for r in
                                                                               row10_str]]

    row11_str = []
    for i in range(6):
        row11_str.append('   ' + str(round(data_delta_t_a_e_M[3][i][1], 4)))

    input_row11 = [
        [sg.Text('', size=(6, 1), font=("Helvetica", 14))] + [sg.Text(r, size=(9, 1), font=14) for r in row11_str]]

    row12_str = []
    for i in range(6):
        row12_str.append('   ' + str(round(data_delta_t_a_e_M[3][i][2], 4)))

    input_row12 = [
        [sg.Text('', size=(6, 1), font=("Helvetica", 14))] + [sg.Text(r, size=(9, 1), font=14) for r in row12_str]]

    row12t_str = []
    for i in range(6):
        row12t_str.append('   ' + str(round(data_delta_t_a_e_M[0][i][3], 4)))

    input_row12t = [
        [sg.Text('', size=(6, 1), font=("Helvetica", 14))] + [sg.Text(r, size=(9, 1), font=14) for r in row12t_str]]
    # ===================================================================

    layout_delta = header + input_row1 + input_row2 + input_row3 + input_row3t + [[sg.Text('')]] \
                   + input_row4 + input_row5 + input_row6 + input_row6t + [[sg.Text('')]] \
                   + input_row7 + input_row8 + input_row9 + input_row9t + [[sg.Text('')]] \
                   + input_row10 + input_row11 + input_row12 + input_row12t


















    # ======================= Layout =======================


    layout = [[sg.TabGroup([[
        sg.Tab('Таблица 1 (T)', layoutTable1),
        sg.Tab('Таблица 2 (A, E, Mтр)', layoutTable2),
        sg.Tab('График 1 (M(E))', layout1),
        sg.Tab('График 2 (I(R^2))', layout2),
        sg.Tab('Погрешности', layout_delta)
    ]])]]

    window = sg.Window('Таблицы и графики', layout)
    window.finalize()

    img1 = Image.open(graphs[0])
    imgByteArr = io.BytesIO()
    img1.save(imgByteArr, format='PNG')
    # imgByteArr = imgByteArr.getvalue()
    window['image1'](data=imgByteArr.getvalue())

    img1 = Image.open(graphs[1])
    imgByteArr = io.BytesIO()
    img1.save(imgByteArr, format='PNG')
    # imgByteArr = imgByteArr.getvalue()
    window['image2'](data=imgByteArr.getvalue())


# ============================= Погрешности =============================
def find_delta(n1, n2):
    global data_from_arduino
    global data_a_e_M

    t1 = data_from_arduino[n1][n2][0]
    t2 = data_from_arduino[n1][n2][1]
    t3 = data_from_arduino[n1][n2][2]
    t_avrg = (t1 + t2 + t3) / 3
    # Погрешность t
    delta_t = 2.353 * (((t_avrg - t1) ** 2 + (t_avrg - t2) ** 2 + (t_avrg - t3) ** 2) / 6) ** 0.5

    a = data_a_e_M[n1][n2][0]
    eps = data_a_e_M[n1][n2][1]
    M = data_a_e_M[n1][n2][2]
    t = t_avrg

    delta_a = 1.0 * ((-4 * h * delta_t / t ** 3) ** 2 + (2 * delta_h / t ** 2) ** 2) ** (0.5)
    e_a = 1.0 * delta_a / a

    delta_eps = 1.0 * ((-8 * h * delta_t / d / t ** 3) ** 2 + (4 * delta_h / d / t ** 2) ** 2 + (
                -4 * h * delta_d / d ** 2 / t ** 2) ** 2) ** (0.5)
    e_eps = 1.0 * delta_eps / eps

    delta_M = 1.0 * ((d / 2 * m0 * (m0 + m_shaiba * n1) * (g - 2 * h / t ** 2) * delta_m0) ** 2 + (
                d / 2 * m_shaiba * (m0 + m_shaiba * n1) * (g - 2 * h / t ** 2) * delta_m_shaiba) ** 2 + (
                                 2 * d * h * (m0 + m_shaiba * n1) * delta_t / t ** 3) ** 2 + (
                                 1 / 2 * (m0 + m_shaiba * n1) * (g - 2 * h / t ** 2) * delta_d) ** 2) ** (0.5)
    e_M = 1.0 * delta_M / M

    return delta_t, delta_a, delta_eps, delta_M


def count_all_delta():
    global data_delta_t_a_e_M
    global n_masses_delta
    global n_lengths_delta
    global n_delta

    for i in range(n_masses_delta):
        for j in range(n_lengths_delta):
            data_delta_t_a_e_M[i][j] = find_delta(i, j)




def exportGraphs(data_from_arduino):
    graphs = plots(data_from_arduino)
    count_all_delta()
    print(data_delta_t_a_e_M)

    Image.open(graphs[0]).save("graph1.png")
    Image.open(graphs[1]).save("graph2.png")

    # ========= Таблица 1 =========
    x = PrettyTable()

    x.field_names = ["n2 = 1", "n2 = 2", "n2 = 3", "n2 = 4", "n2 = 5", "n2 = 6"]

    for i in range(4):
        for j in range(3):
            row = []
            for k in range(6):
                row.append(data_from_arduino[i][k][j])
            x.add_row(row)

        avg_values = []

        for k in range(6):
            avg_value = data_from_arduino[i][k][0] + data_from_arduino[i][k][1] + data_from_arduino[i][k][2]
            avg_values.append(round(avg_value / 3, 2))

        #x.add_row(avg_values)

    with open('table1.html', 'wb') as f:
        f.write(x.get_html_string().encode('utf-8'))

    # ========= Таблица 2 =========
    x = PrettyTable()

    x.field_names = ["n2 = 1", "n2 = 2", "n2 = 3", "n2 = 4", "n2 = 5", "n2 = 6"]

    physics_h = 0.7;
    physics_d = 0.046;
    physics_m_0 = 0.047;
    physics_m_sh = 0.220;
    physics_g = 9.81908;

    for i in range(4):

        row1 = []
        row2 = []
        row3 = []

        for k in range(6):
            #print(i)
            avg_value = (data_from_arduino[i][k][0] + data_from_arduino[i][k][1] + data_from_arduino[i][k][2]) / 3
            a = 2 * physics_h / (avg_value * avg_value)
            eps = 2 * a / physics_d
            m = (physics_m_0 + physics_m_sh * (i + 1.0))
            #print(m)
            row1.append(a)
            row2.append(eps)

            row3.append((physics_g - a) * (m * physics_d / 2.0))

        x.add_row(row1)
        x.add_row(row2)
        x.add_row(row3)

    with open('table2.html', 'wb') as f:
        f.write(x.get_html_string().encode('utf-8'))


    # ========= Погрешности =========
    x = PrettyTable()

    x.field_names = ["n2 = 1", "n2 = 2", "n2 = 3", "n2 = 4", "n2 = 5", "n2 = 6"]

    for i in range(4):
        for j in range(4):
            row = []
            for k in range(6):
                row.append(data_delta_t_a_e_M[i][k][j])
            x.add_row(row)

    with open('delta.html', 'wb') as f:
        f.write(x.get_html_string().encode('utf-8'))



    print("Export successful")


def detectArduino():
    ports = list(serial.tools.list_ports.comports())
    Arduino_ports = []
    for p in ports:
        # print(p.description)
        # if 'Arduino' in p.description:
        Arduino_ports.append(p)
    global window
    if (len(Arduino_ports) == 0):
        window['comport'].Update(value='Установка: не подключена.')
        return "-1"
    window['comport'].Update(value='Установка: подключена на ' + str(Arduino_ports[0]) + '.')
    return Arduino_ports[0].device


def arduinoAdapter(com_port, m):
    throw_now = False
    throw_start_time = 0.0
    throw_end_time = 0.0

    previous_measurement = 100.0

    try:
        with serial.Serial(str(com_port), arduino_speed, timeout=0) as ser:
            global stop_arduino
            while not stop_arduino:
                a = str(ser.readline().decode()).replace("\\r\\n", "")

                try:
                    s = float(a)

                    global delta_measurement
                    global throw_result_time

                    throw_result_time = float(time.time()) - float(throw_start_time)
                    global window
                    window[str('r' + str(m))].Update(value='%.2f' % throw_result_time)

                    if (throw_now):
                        if (previous_measurement - s < 0.01):
                            throw_now = False
                        if (time.time() - throw_start_time > 20.0):
                            throw_now = False

                        if (s < 0.5):
                            stop_arduino = True
                            throw_now = False
                            throw_end_time = time.time()
                            throw_result_time = throw_end_time - throw_start_time

                    else:
                        if (s >= 69.9):
                            throw_start_time = time.time()
                            throw_now = True

                    previous_measurement = s

                    # print(str(datetime.datetime.now().time()) + " " + str(s))
                    time.sleep(arduino_time)
                except ValueError:
                    pass

                global arduino_tmp_msg
                if (arduino_tmp_msg):
                    ser.write(arduino_tmp_msg)
                    arduino_tmp_msg = ""
    except:
        noArduinoScenario()


def getSingleThrow(m):
    global stop_arduino
    if (stop_arduino):
        stop_arduino = False
        com_port = detectArduino()
        if (com_port == str(-1)):
            noArduinoScenario()
            return 0.0
        arduinoAdapter(com_port, m)
        return throw_result_time
    else:
        return 0.0


def awaitSingleThrow(m, r, s):
    global throw_result_time
    throw_result_time = 0.0
    x = threading.Thread(target=getSingleThrow, args=(s,))
    x.start()

    if EMULATOR_MODE_ON:
        time.sleep(3)
        commandy = "throw " + str(m) + " " + str(r)
        global arduino_tmp_msg
        arduino_tmp_msg = bytes(commandy, 'utf-8')
        # print(arduino_tmp_msg)

    x.join(60.0)
    global stop_arduino
    stop_arduino = True

    global window
    global data_from_arduino

    try:
        print(throw_result_time)
        data_from_arduino[m - 1][r - 1][s - 1] = throw_result_time
        window[str('r' + str(s))].Update(value='%.2f' % throw_result_time)

        if EMULATOR_MODE_ON:
            window[str('r' + str(1))].Update(value='%.2f' % throw_result_time)
            window[str('r' + str(2))].Update(value='%.2f' % throw_result_time)
            window[str('r' + str(3))].Update(value='%.2f' % throw_result_time)
            data_from_arduino[m - 1][r - 1][0] = throw_result_time
            data_from_arduino[m - 1][r - 1][1] = throw_result_time
            data_from_arduino[m - 1][r - 1][2] = throw_result_time

        # print()
    except:
        print("danna why but something is wrong")

    global measuringNow
    measuringNow = False
    disableUIForMeasurement(False, s)

    return throw_result_time


def disableUIForMeasurement(t, n):
    global window
    window['sliderMass'].Update(disabled=t)
    window['sliderLength'].Update(disabled=t)

    window['emulatormode'].Update(disabled=t)

    if t:
        if (n == 1):
            # print(dir( window['m1']))
            window['m1'].Update(text="Стоп")
            window['m2'].Update(disabled=t)
            window['m3'].Update(disabled=t)
        if (n == 2):
            window['m2'].Update(text="Стоп")
            window['m1'].Update(disabled=t)
            window['m3'].Update(disabled=t)
        if (n == 3):
            window['m3'].Update(text="Стоп")
            window['m2'].Update(disabled=t)
            window['m1'].Update(disabled=t)
    else:
        if (n == 1):
            window['m1'].Update(text="Измерить")
            window['m2'].Update(disabled=t)
            window['m3'].Update(disabled=t)
        if (n == 2):
            window['m2'].Update(text="Измерить")
            window['m1'].Update(disabled=t)
            window['m3'].Update(disabled=t)
        if (n == 3):
            window['m3'].Update(text="Измерить")
            window['m2'].Update(disabled=t)
            window['m1'].Update(disabled=t)


def read_from_file():
    # layout_reading_from_file = [
    #    [sg.T('Выберите файл')],
    #    [sg.In(key='input')],
    #    [sg.FileSaveAs(target='input'), sg.OK()],
    # ]

    data_from_file = [[]]

    file_name_in = str(sg.popup_get_file('Выбор файла с измерениями'))

    if file_name_in == 'None':
        return data_from_file

    with open(file_name_in) as f:
        for line in f:
            data_from_arduino.append([float(x) for x in line.split()])
    # sg.popup('1', 'Будет считан указанный ниже файл', file_name_in)

    # window = sg.Window('Считывание из файла', layout_reading_from_file)
    # event, values = window.read()
    # sg.popup(values[0])
    # window.close()

    return data_from_file


# ================ MAIN PROGRAM ================
window.finalize()
detectArduino()

# Считывание из файла!
# data_from_file = read_from_file()


while True:
    event, values = window.read()

    mass = int(values['sliderMass'])
    length = int(values['sliderLength'])

    if event in (None, 'Cancel'):
        break

    if event == 'sliderMass' or event == 'sliderLength':
        window['r1'].Update(value=str(data_from_arduino[int(mass) - 1][int(length) - 1][0]))
        window['r2'].Update(value=str(data_from_arduino[int(mass) - 1][int(length) - 1][1]))
        window['r3'].Update(value=str(data_from_arduino[int(mass) - 1][int(length) - 1][2]))

    if event == 'showGraphs':
        resultWindow(data_from_arduino)

    if event == 'exportGraphs':
        exportGraphs(data_from_arduino)

    if (event == 'emulatormode'):
        EMULATOR_MODE_ON = values['emulatormode']
        if EMULATOR_MODE_ON:
            print('Emulator enabled')
        else:
            print('Emulator disabled')

    if (event == 'm1') or (event == 'm2') or (event == 'm3'):
        if (measuringNow):
            stop_arduino = True
            measuringNow = False
            if (event == 'm1'):
                disableUIForMeasurement(measuringNow, 1)
            if (event == 'm2'):
                disableUIForMeasurement(measuringNow, 2)
            if (event == 'm3'):
                disableUIForMeasurement(measuringNow, 3)
        else:
            measuringNow = True
            if (event == 'm1'):
                disableUIForMeasurement(measuringNow, 1)
            if (event == 'm2'):
                disableUIForMeasurement(measuringNow, 2)
            if (event == 'm3'):
                disableUIForMeasurement(measuringNow, 3)

            x = threading.Thread(target=awaitSingleThrow, args=(mass, length, int(event[1])))
            x.start()

    # print(str(mass) + " " + str(length))

window.close()

if False:
    print("l1: " + str(awaitSingleThrow(2, 3)))
    print("l2: " + str(awaitSingleThrow(4, 2)))

exit(0)
