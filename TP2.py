from turtle import TPen
import VariablesGlobales as s
import TP1 as io
from Outils import clone


def equalization(image):
    cum_hist = io.cumulated_histogram(image)
    LUT = [0] * (s.graylevel + 1)
    for g in range(s.graylevel + 1):
        LUT[g] = int(s.graylevel * cum_hist[g] / io.nbPixels())
    new_image = clone(image)
    for h in range(s.height):
        for w in range(s.width):
            new_image[h][w] = LUT[image[h][w]]
    return new_image


def linear_transformation(image, points):
    LUT = [0] * (s.graylevel + 1)
    for p in range(1, len(points)):
        slope = (points[p][1] - points[p - 1][1]) / (points[p][0] - points[p - 1][0])
        intercept = points[p][1] - slope * points[p][0]
        for g in range(points[p - 1][0], points[p][0] + 1):
            LUT[g] = int(slope * g + intercept)
    new_image = clone(image)
    for h in range(s.height):
        for w in range(s.width):
            new_image[h][w] = LUT[new_image[h][w]]
    return new_image


def dark_dilatation(image):
    points = [
        [0, 0],
        [int(s.graylevel / 4), int(s.graylevel / 2)],
        [s.graylevel, s.graylevel]
    ]
    return linear_transformation(image, points)


def inverse(image):
    points = [
        [0, s.graylevel],
        [s.graylevel, 0]
    ]
    return linear_transformation(image, points)


def light_dilatation(image):
    points = [
        [0, 0],
        [int(s.graylevel / 2), int(s.graylevel / 4)],
        [s.graylevel, s.graylevel]
    ]
    return linear_transformation(image, points)
