import VariablesGlobales as s
import Outils
import math

def read(filepath):
    type = readType(filepath)
    if (type == None):
        raise Exception
    if (type == "P2\n"):
        imageread, s.width, s.height, s.graylevel = readPGMascii(filepath)
    else:
        imageread, s.width, s.height, s.graylevel = readPGMbinary(filepath)
    if (imageread == None):
        raise Exception
    else:
        s.isread = True
        s.image_orig = Outils.arrayToMatrix(imageread, s.width, s.height)


def readType(filepath):
    try:
        file = open(filepath, 'r')
        type = file.readline()
    except UnicodeDecodeError:
        file = open(filepath, 'rb')
        type = file.readline().decode()
    if not ("P2" in type or "P5" in type):
        file.close()
        return None
    file.close()
    return type


def readPGMascii(filepath):
    file = open(filepath, 'r')
    file.readline()
    while True:
        line = file.readline()
        if line[0] != '#': break
    dimx, dimy = line.split()
    dimx, dimy = int(dimx), int(dimy)
    nivg = int(file.readline())
    imageread = []
    for line in file.readlines():
        for num in line.split():
            imageread.append(int(num))
    if len(imageread) != dimx * dimy:
        file.close()
        return None, -1, -1, -1
    file.close()
    return imageread, dimx, dimy, nivg


def readPGMbinary(filepath):
    file = open(filepath, 'rb')
    file.readline()
    while True:
        line = file.readline().decode()
        if line[0] != '#': break
    dimx, dimy = line.split()
    dimx, dimy = int(dimx), int(dimy)
    nivg = int(file.readline().decode())
    imageread = []
    imageread = list(file.read(dimx * dimy))
    if len(imageread) != dimx * dimy:
        file.close()
        return None, -1, -1, -1
    file.close()
    return imageread, dimx, dimy, nivg


def write(filepath, image):
    data = Outils.matrixToArray(image, s.height, s.width)
    writePGM(filepath, data)


def writePGM(filepath, image):
    # image is a tuple of (data,width,height,graylevel)
    file = open(filepath, "w")
    file.write("P2\n")
    file.write("#Created by Souha Ben Hassine & Cyrine Zaouali\n")
    file.write(str(s.width) + " " + str(s.height) + "\n")
    file.write(str(s.graylevel) + "\n")
    for num in range(0, len(image)):
        # file.write(str(num)+"\t")
        file.write(str(image[num]) + " ")
        if ((num + 1) % s.width == 0):
            file.write("\n")
    file.close()



def nbPixels():
    return s.width * s.height


def average(image):
    avg = 0
    for h in range(s.height):
        for w in range(s.width):
            avg += image[h][w]
    return avg / nbPixels()


def deviation(image):
    avg = average(image)
    dev = 0
    for h in range(s.height):
        for w in range(s.width):
            dev += (image[h][w] - avg) ** 2
    return math.sqrt(dev / nbPixels())


def histogram(image):
    hist = [0] * (s.graylevel + 1)
    for h in range(s.height):
        for w in range(s.width):
            hist[image[h][w]] += 1
    return hist


def cumulated_histogram(image):
    hist = histogram(image)
    cum_hist = [0] * (s.graylevel + 1)
    cum_hist[0] = hist[0]
    for g in range(1, s.graylevel + 1):
        cum_hist[g] = hist[g] + cum_hist[g - 1]
    return cum_hist

