import os
import cv2

def Recortes(step, y0, x0, xFinal, yFinal, image, nombre, nombreDIR):
    pixelsx = xFinal - x0
    pixelsy = yFinal - y0
    numx = pixelsx / step
    numy = pixelsy / step
    png = ".png"
    cv2.rectangle(image, (x0, y0), (xFinal, yFinal), (0, 0, 255), 5)
    for i in range(int(numy)):
        for j in range(int(numx)):
            oko = image[y0 + i * step:y0 + (i + 1) * step, x0 + j * step:x0 + (j + 1) * step]
            cv2.imwrite(nombreDIR + "/" + nombre + "%s" % i + "%s" % j + png, oko)

def RecorteDeImagen(imagePNG, nombreDIR1, nombreDIR2, nombreDIR3):
    image = cv2.imread(imagePNG)

    (h, w, d) = image.shape
    print("width={}, height={}, depth={}".format(w, h, d))

    x0 = 2000
    y0 = 5
    xFinal = 4000
    yFinal = 2550
    pixelsx = xFinal - x0
    pixelsy = yFinal - y0
    step = 300
    numx = pixelsx / step
    numy = pixelsy / step
    nombre = "Recorte:"
    png = ".png"

    output = image.copy()
    cv2.rectangle(output, (x0, y0), (xFinal, yFinal), (0, 0, 255), 5)
    for i in range(int(numy)):
        for j in range(int(numx)):
            oko = output[y0 + i * step:y0 + (i + 1) * step, x0 + j * step:x0 + (j + 1) * step]
            cv2.imwrite(nombreDIR1 + "/" + nombre + "%s" % i + "%s" % j + png, oko)

    outhsv = cv2.cvtColor(output, cv2.COLOR_BGR2HSV)
    h = outhsv[:, :, 0]
    for i in range(int(numy)):
        for j in range(int(numx)):
            oko = h[y0 + i * step:y0 + (i + 1) * step, x0 + j * step:x0 + (j + 1) * step]
            # esto yo creo que esta mal porque si le pasas un hsv a imwrite te lo lee como un BGR
            cv2.imwrite(nombreDIR2 + "/" + nombre + "%s" % i + "%s" % j + png, oko)

    gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)[1]
    for i in range(int(numy)):
        for j in range(int(numx)):
            oko = thresh[y0 + i * step:y0 + (i + 1) * step, x0 + j * step:x0 + (j + 1) * step]
            cv2.imwrite(nombreDIR3 + "/" + nombre + "%s" % i + "%s" % j + png, oko)

    # cv2.imshow("Imagen recortada 2", elRecorte2)
    cv2.waitKey(0)


#os.mkdir('Normal2')
#os.mkdir('HSV2')
#os.mkdir('UMBRAL2')
RecorteDeImagen("venv/03_11_2020_IMAG0684.jpg", 'Normal2', 'HSV2', 'UMBRAL2')
RecorteDeImagen("venv/03_11_2020_IMAG0471.jpg", 'Normal2', 'HSV2', 'UMBRAL2')
