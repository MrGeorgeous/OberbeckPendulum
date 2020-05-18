

from array import *

from prettytable import PrettyTable
import matplotlib.pyplot as plt
import io
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


def plots(data_in):

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

    #plt.show()
    plt.savefig(graphs[0], format='png')

    plt.cla()
    print()

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
data = [[[0.0 for k in range(n_measurements)] for j in range(n_lengths)] for i in range(n_masses)]

data = [
    [[4.41, 4.46, 4.44], [5.84, 5.84, 5.97], [7.07, 7.00, 7.06], [7.97, 8.06, 8.07], [9.50, 9.22, 9.31], [10.28, 10.13, 10.37]],
    [[3.16, 3.28, 3.25], [4.09, 4.16, 4.18], [4.04, 5.00, 5.28], [5.72, 5.69, 5.64], [6.40, 6.31, 6.28], [7.25, 7.13, 7.28]],
    [[2.81, 2.72, 2.72], [3.39, 3.46, 3.35], [4.06, 4.13, 4.06], [4.56, 4.69, 4.63], [5.15, 5.19, 5.19], [5.81, 5.81, 5.81]],
    [[2.40, 2.34, 2.47], [3.00, 2.91, 2.97], [3.56, 3.59, 3.64], [3.93, 4.03, 3.98], [4.53, 4.47, 4.43], [5.03, 4.97, 4.94]]
]

print(data)

from PIL import Image

import PySimpleGUI as sg

sg.theme('SystemDefaultForReal')

measurementFrame = [
                [sg.Text('Установка: не подключена.', key="comport", size=(25,1)),
                 sg.Checkbox('Режим эмулятора', key='emulatormode', size=(20,1), default=EMULATOR_MODE_ON, enable_events=True)],
                [
                    sg.Text('Количество грузов'),
                    sg.Slider(range=(1, 4), orientation='h', size=(8,10), change_submits=True, key='sliderMass', font=('Helvetica 12')),
                    sg.Text('Положение утяжелителей'),
                    sg.Slider(range=(1, 6), orientation='h', size=(12, 10), change_submits=True, key='sliderLength', font=('Helvetica 12'))
                ],
                [
                     sg.Text('1: '), sg.Text(key="r1", text=str(data[0][0][0])), sg.Button('Измерить', key='m1'),
                     sg.Text('2: '), sg.Text(key="r2", text=str(data[0][0][1])), sg.Button('Измерить', key='m2'),
                     sg.Text('3: '), sg.Text(key="r3", text=str(data[0][0][2])), sg.Button('Измерить', key='m3')
                ],
            ]

resultsFrame = [[sg.Button('Таблицы и графики', key='showGraphs')]]

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

def resultWindow(data):

    graphs = plots(data)

    sg.theme('SystemDefaultForReal')

    layout1 = [ [sg.Image(filename='', key='image1')] ]
    layout2 = [ [sg.Image(filename='', key='image2')] ]


    # ЗДЕСЬ СДЕЛАТЬ ТАБЛИЦЫ И ВСТАВИТЬ

    layoutTable1 = []
    layoutTable2 = []

    layout = [[sg.TabGroup([[
        sg.Tab('Таблица 1 (T)', layoutTable1),
        sg.Tab('Таблица 2 (A, E, Mтр)', layoutTable2),
        sg.Tab('График 1 (M(E))', layout1),
        sg.Tab('График 2 (I(R^2))', layout2)
    ]]) ]]

    window = sg.Window('Таблицы и графики', layout)
    window.finalize()

    img1 = Image.open(graphs[0])
    imgByteArr = io.BytesIO()
    img1.save(imgByteArr, format='PNG')
    #imgByteArr = imgByteArr.getvalue()
    window['image1'](data=imgByteArr.getvalue())

    img1 = Image.open(graphs[1])
    imgByteArr = io.BytesIO()
    img1.save(imgByteArr, format='PNG')
    #imgByteArr = imgByteArr.getvalue()
    window['image2'](data=imgByteArr.getvalue())



def detectArduino():
    ports = list(serial.tools.list_ports.comports())
    Arduino_ports = []
    for p in ports:
        #print(p.description)
        #if 'Arduino' in p.description:
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
                    window[str('r' + str(m))].Update(value= '%.2f'%throw_result_time )

                    if (throw_now):
                        if (previous_measurement - s < 0.01) :
                            throw_now = False
                        if (time.time() - throw_start_time > 20.0):
                            throw_now = False

                        if (s < 0.5) :
                            stop_arduino = True
                            throw_now = False
                            throw_end_time = time.time()
                            throw_result_time = throw_end_time - throw_start_time

                    else:
                        if (s >= 69.9) :
                            throw_start_time = time.time()
                            throw_now = True

                    previous_measurement = s

                    #print(str(datetime.datetime.now().time()) + " " + str(s))
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
        #print(arduino_tmp_msg)

    x.join(60.0)
    global stop_arduino
    stop_arduino = True

    global window
    global data

    try:
        print(throw_result_time)
        data[m - 1][r - 1][s - 1] = throw_result_time
        window[str('r' + str(s))].Update(value='%.2f' % throw_result_time)

        if EMULATOR_MODE_ON:
            window[str('r' + str(1))].Update(value='%.2f' % throw_result_time)
            window[str('r' + str(2))].Update(value='%.2f' % throw_result_time)
            window[str('r' + str(3))].Update(value='%.2f' % throw_result_time)
            data[m - 1][r - 1][0] = throw_result_time
            data[m - 1][r - 1][1] = throw_result_time
            data[m - 1][r - 1][2] = throw_result_time

        #print()
    except:
        print("dunna why but something is wrong")

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
            #print(dir( window['m1']))
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


window.finalize()
detectArduino()

while True:
    event, values = window.read()

    mass = int(values['sliderMass'])
    length = int(values['sliderLength'])

    if event in (None, 'Cancel'):
        break

    if event == 'sliderMass' or event == 'sliderLength':
        window['r1'].Update(value=str(data[int(mass) - 1][int(length) - 1][0]))
        window['r2'].Update(value=str(data[int(mass) - 1][int(length) - 1][1]))
        window['r3'].Update(value=str(data[int(mass) - 1][int(length) - 1][2]))

    if event == 'showGraphs':
        resultWindow(data)


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

exit(0);






