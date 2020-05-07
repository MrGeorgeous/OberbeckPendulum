from array import *
import matplotlib.pyplot as plt
import numpy as np


# Константы
mass_karetka = 0.047
mass_shaiba = 0.220
mass_gruz = 0.408
l_1 = 5.7
l_0 = 2.5
b = 4.0
d = 4.6
h_0 = 70.0
g = 9.81908
humanDelayTime = 0.13
I_0 = 0.011541518
M_tr_a = 0.003179657
M_tr_b = 0.000950262
moments_tr = [-0.00228920, 0.00998837, 0.00906186, 0.01317346, 0.01499408, 0.01614266]


def getDataFromArduino():
    arduinoData = []

    # TODO Получение данных с платы

    # Пример:
    arduinoData = [70.00, 69.99, 69.97, 69.93, 69.88, 69.81, 69.72, 69.62, 69.50, 69.37, 69.23, 69.06, 68.89, 68.69,
                   68.48, 68.26, 68.02, 67.76, 67.49, 67.21, 66.91, 66.59, 66.26, 65.91, 65.54, 65.16, 64.77, 64.36,
                   63.93, 63.49, 63.04, 62.57, 62.08, 61.57, 61.06, 60.52, 59.97, 59.41, 58.83, 58.23, 57.62, 56.99,
                   56.35, 55.69, 55.02, 54.33, 53.63, 52.91, 52.17, 51.42, 50.66, 49.88, 49.08, 48.27, 47.44, 46.60,
                   45.74, 44.86, 43.97, 43.07, 42.15, 41.21, 40.26, 39.29, 38.31, 37.31, 36.30, 35.27, 34.22, 33.16,
                   32.09, 31.00, 29.89, 28.77, 27.63, 26.48, 25.31, 24.13, 22.93, 21.71, 20.48, 19.24, 17.98, 16.70,
                   15.41, 14.10, 12.78, 11.44, 10.09, 8.72, 7.33, 5.93, 4.52, 3.09, 1.64, 0.18]

    return arduinoData


def showPlot(x_, y_):
    plt.figure()
    plt.plot(x_, y_)
    plt.show()


# =======================================================================================================================

def M_tr(n_):
    return moments_tr[n_ - 1]


def R(n_):
    return l_1 + (n_ - 1) * l_0 + b / 2

def I(n_):
    return I_0 + 4 * mass_gruz * R(n_) * R(n_) / 10000

def m(q_):
    return mass_karetka + q_ * mass_shaiba

def a(q_, n_):
    return (m(q_) * (d / 100) * g / 2 - M_tr(n_)) / (2 * I(n_) / (d / 100) + m(q_) * (d / 100) / 2)


def x(t_, q_, n_):
    return 100.0 * max(0, h_0 / 100 - a(q_, n_) * t_ * t_ / 2)


def takeMeasurements(q, n):
    measurements = []
    r = 70.0
    experimentTime = 0.0
    while r > 0.0:
        measurements.append(r)
        r = x(experimentTime, q, n)
        experimentTime += 0.01

    return measurements


def make_calculations():
    # TODO Результаты
    ttt = 0


print("======================================================")
print("Добро пожаловать!")

print("Желаете ли внести изменить данные об установке?\n 1 - Да, 2 - Нет")
changeInstallationData = int(input())
if changeInstallationData == 1:
    print("Введите массу каретки: ", end="")
    caretcaMass = float(input())
    print("Введите массу шайбы: ", end="")
    m = float(input())
    print("Введите массу груза-утяжелителя на крестовине: ", end="")
    mUt = float(input())
    print("Введите расстояние первой риски от оси: ", end="")
    l1 = float(input())
    print("Введите расстояние между рисками: ", end="")
    l0 = float(input())
    print("Введите диаметр ступицы: ", end="")
    d = float(input())
    print("Введите размер утяжелителя вдоль спицы: ", end="")
    b = float(input())

print("======================================================")
print("Выберите конфигурацию:\nГрузы: 1, 2, 3, 4\nРейка: 1, 2, 3, 4, 5, 6");

print("Введите колличество грузов: ", end="")
q = int(input())
print("Введите номер риски: ", end="")
n = int(input())
print("======================================================")

# !Данные можно получить с установки!
# arduinoData = getDataFromArduino()
# t = 0.1 * len(arduinoData)
# R = l1 + (n - 1) * l0 + b / 2
# a = (2 * h_0) / (t ** 2)  # Ускорение
# eps = 2 * a / d  # Угловое ускорение крестовины
# T = m * (g - a)  # Сила натяжения
# M = m * d * (g - a) / 2  # Момент силы натяжения


measurements = takeMeasurements(q, n)
t = 0.01 * len(measurements)
print("Время падаения равно ", end="")
print(t)
