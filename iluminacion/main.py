import os
import cv2
import numpy as np
from matplotlib import pyplot as plt

# os.mkdir('Salida')
directory = r'Entrada'
i = 1
for filename in os.listdir(directory):
    fileAndDirectory = os.path.join(directory, filename)
    if filename.endswith(".jpg") or filename.endswith(".png"):
        img = cv2.imread(fileAndDirectory)  # , cv2.IMREAD_GRAYSCALE)
        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        img_h = img_hsv[:, :, 2]
        MaskBrillo = cv2.threshold(img_h, 210, 255, cv2.THRESH_BINARY_INV)[1]
        cv2.imwrite('Salida/FotoMask' + str(i) + '.png', MaskBrillo)
        i += 1
    else:
        continue





