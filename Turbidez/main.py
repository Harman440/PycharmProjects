import csv
import numpy as np
from matplotlib import pyplot as plt
import math


def Tss2Turbidez(Tss, a, b, dispersion, medidaTurbidez, Malas):
    turbidezCalculada = a * Tss + b
    difTurb = medidaTurbidez - turbidezCalculada
    if difTurb < 0:
        difTurb = -1 * difTurb
    if difTurb < dispersion:
        return medidaTurbidez
    else:
        Malas[0] += 1
        return turbidezCalculada


def minimosCuadrados(x, y):
    i = 0
    sumXY = 0
    sumX = 0
    sumY = 0
    sumX2 = 0
    sumY2 = 0
    for xV in x:
        sumXY += xV * y[i]
        sumX += xV
        sumY += y[i]
        sumX2 += xV * xV
        sumY2 += y[i] * y[i]
        i += 1
    a = ((i * sumXY) - (sumY * sumX))/((i * sumX2) - (sumX * sumX))
    b = (sumY - a * sumX)/i
    r = ((i * sumXY) - (sumY * sumX))/math.sqrt((((i * sumX2) - (sumX * sumX))) * (((i * sumY2) - (sumY * sumY))))
    return a, b, r



# guardar Datos en arrays
csv_file = open('venv/ysi_salida_onzonilla.csv')
csv_reader = csv.reader(csv_file, delimiter=',')
line_count = 0
dataTodo = list(csv_reader)
numDatos = 4831
turbidez = np.zeros(numDatos)
TSS = np.zeros(numDatos)
turbidezNueva = np.zeros(numDatos)
for row in dataTodo:
    if line_count == 0:
        # print(f'columns names are {",".join(row)}')
        line_count += 1
    else:
        # print(f'\t valor de turbidez {line_count} es {row[2]}')
        # print(f'\t valor de TSS {line_count} es {row[3]}')
        turbidez[line_count - 1] = int(row[2])
        TSS[line_count - 1] = int(row[3])
        line_count += 1
# print(f'number of lines processed = {line_count}')


i = 0
medidasMalas = [0]

# Para hayar la media de turbidez para un valor de TSS, tmbn tengo codigo para un rango de TSS
numRangosdeTss = 60  # para TSSlog # 70 si quiero entre 200 y 270 TSS # 68  si quiero todos los valores de TSS
contador = np.zeros(numRangosdeTss)
media = np.zeros(numRangosdeTss)
TssValueGraph = np.zeros(numRangosdeTss)

# igual es util el logaritmo de los valores de TSS y turbidez (una correlación logaritmica se supone que se ajusta mas)
# aun asi los datos estan muy dispersos
turbidezLog = np.zeros(numDatos)
TssLog = np.zeros(numDatos)

aCalc, bCalc, r = minimosCuadrados(TSS, turbidez)

for TssValue in TSS:

    # hayar logaritmos
    TssLog[i] = math.log(TssValue, 10)
    if turbidez[i] != 0:
        turbidezLog[i] = math.log(turbidez[i], 10)

    # esta funcion te pasa de TSS a Turbidez si la relación es conocida y proporcional
    # los valores de a y b fueron calculados en un run del código anterior usando la func. minimosCuadrados.
    turbidezNueva[i] = Tss2Turbidez(TssValue, 0.2149, -5.966, 20, turbidez[i], medidasMalas)

    # -------10/03/2021-----
    # usando los logaritmos


    # agrupar turbidez si el valor de TSS asociado es el mismo (rango) y luego hayar la media de todos los valores
    for j in range(numRangosdeTss):
        # TssValueGraph[j] = j*5
        # TssValueGraph[j] = j + 200
        TssValueGraph[j] = j*0.005 + 2.2
        # Si la turbidez es menor que 15 o mayor de 95 es ruido seguro
        if 0.19 < turbidezLog[i] < 1.9:  # he añadido Log y antes era entre 10 y 95
            if TssLog[i] == TssValueGraph[j]:  # j * 5 < TssValue < j * 5 + 5:
                contador[j] += 1
                media[j] = (turbidezLog[i] + media[j] * (contador[j] - 1)) / contador[j]
    i += 1

for j in range(numRangosdeTss):
    print(f'la media de {contador[j]} medidas de un TSS de {j*0.005 + 2.2} es {media[j]}')

# aCalc2, bCalc2, r2 = minimosCuadrados(TssValueGraph, media)
aCalcL, bCalcL, rL = minimosCuadrados(TssLog, turbidezLog)
# Las datos de turbidez considerados ruido por la funcion de proporcionalidad
print(medidasMalas)
print(aCalc, bCalc, r)
# print(aCalc2, bCalc2, r2)
print(aCalcL, bCalcL, rL)

plt.figure(1)
plt.scatter(TssValueGraph, media)
# plt.plot(TSS, turbidezNueva)

plt.figure(2)
# plt.scatter(TssLog, turbidezLog)
plt.xlim(1190, 1500)
plt.plot(turbidezNueva)
plt.plot(turbidez)
plt.plot(TSS)

plt.figure(3)
plt.plot(turbidezLog)
# plt.plot(turbidez)
plt.plot(TssLog)

plt.show()
