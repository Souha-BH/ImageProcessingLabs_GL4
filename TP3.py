import VariablesGlobales as s
from Outils import clone
import random
import math
from TP1 import average

def filter_median(image, size):
    if (size % 2 == 0):
        size += 1
    new_image = clone(image)
    for h in range(s.height):
        for w in range(s.width):
            medians = []
            for py in range(max(0, h - size // 2), min(s.height, h + size // 2 + 1)):
                for px in range(max(0, w - size // 2), min(s.width, w + size // 2 + 1)):
                    medians.append(image[py][px])
            medians.sort()
            new_image[h][w] = medians[len(medians) // 2 + 1]
    return new_image


def convolution(image, filter, size):
    new_image = clone(image)
    for h in range(s.height):
        for w in range(s.width):
            conv = 0
            for py in range(-size // 2, size // 2 + 1):
                if not (((py + h) < 0) or ((py + h) >= s.height)):
                    for px in range(-size // 2, size // 2 + 1):
                        if not (((px + w) < 0) or ((px + w) >= s.width)):
                            conv += image[py + h][px + w] * filter[py + size // 2][px + size // 2]
            if (conv < 0):
                conv = 0
            if (conv > s.graylevel):
                conv = s.graylevel
            new_image[h][w] = int(conv)
    return new_image


def filter_average(image, size):
    if (size % 2 == 0):
        size += 1
    filter = [[1 / size ** 2 for i in range(size)] for j in range(size)]
    return convolution(image, filter, size)


def filter_gauss(image, size):
    if (size % 2 == 0):
        size += 1
    filter = [[1 for i in range(size)] for j in range(size)]
    sum = 0
    center = size // 2
    for py in range(-center, center + 1):
        for px in range(-center, center + 1):
            filter[py + center][px + center] = 2 ** (center ** 2 - abs(py) - abs(px))
            sum += filter[py + center][px + center]
    for py in range(-center, center + 1):
        for px in range(-center, center + 1):
            filter[py + center][px + center] /= sum
    return convolution(image, filter, size)


def filter_high(image):
    filter = [[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]]
    return convolution(image, filter, 3)

def noise(Matrix, width, height, val):
    new_Matrix = clone(Matrix)
    for h in range(height):
        for w in range(width):
            x = random.randint(0, 20)
            if (x == 0):
                new_Matrix[h][w] = 0
            if (x == 20):
                new_Matrix[h][w] = val
    return new_Matrix


def SNR(image):
    avg = average(s.image_orig)
    S = 0
    B = 0
    for h in range(s.height):
        for w in range(s.width):
            S += (s.image_orig[h][w] - avg) ** 2
            B += (image[h][w] - s.image_orig[h][w]) ** 2
    if (B == 0):
        return 0.0
    return math.sqrt(S / B)