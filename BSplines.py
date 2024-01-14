import numpy as np
import pygame as pg
import math

C2_BSpline_matrix = np.array(np.mat([[1/6, 2/3, 1/6, 0],
                                     [-1/2, 0, 1/2, 0],
                                     [1/2, -1, 1/2, 0],
                                     [-1/6, 1/2, -1/2, 1/6]]))

def b_spline(matrix, points):
    return lambda t: np.matmul(np.array([1, t, t**2, t**3]),
                               np.matmul(matrix, points))
def b_spline_deriv(matrix, points):
    return lambda t: np.matmul(np.array([0, 1, 2*t, 3*(t**2)]),
                               np.matmul(matrix, points))
def b_spline_deriv_2(matrix, points):
    return lambda t: np.matmul(np.array([0, 0, 2, 6*t]),
                               np.matmul(matrix, points))

def draw_b_spline(surface, points, color):
    n = len(points)
    for i in range(-3, n):
        pts = [points[((i + j) if (i + j) >= 0 else 0)
                    if (i + j) < n else n - 1]
                        for j in range(0, 4)]
        curve = b_spline(C2_BSpline_matrix, pts)

        step = 0.001
        for j in range(0, int(1 / step)):
            pt_1 = curve(j * step)
            pt_1 = [int(coord) for coord in pt_1]

            surface.set_at(pt_1, color)

def get_derivative(curve):
    return lambda t: [
        (curve(t + 0.1)[i] - curve(t)[i]) / 0.1
                      for i in range(0, 2)]
def draw_derivative_vectors(surface, points, color):
    n = len(points)
    for i in range(-3, n):
        pts = [points[((i + j) if (i + j) >= 0 else 0)
                    if (i + j) < n else n - 1]
                        for j in range(0, 4)]
        curve = b_spline(C2_BSpline_matrix, pts)
        derivative = b_spline_deriv_2(C2_BSpline_matrix, pts)

        step = 1 / 10
        for j in range(0, 10):
            pt_1 = curve(j * step)
            pt_1 = [int(coord) for coord in pt_1]        
            pt_2 = derivative(j * step)
            pt_2 = [int(coord) for coord in pt_2]
            pt_2 = [pt_2[i] + pt_1[i] for i in range(0, 2)]
            
            pg.draw.line(surface, color, pt_1, pt_2)

def hash_func(i, j):
    return str(i) + "-" + str(j)

def N_basis(i, j, knots, memo_table):
    key = hash_func(i, j)
    try:
        val = memo_table[key]
        return val
    except KeyError:
        if j == 0:
            func = lambda t: (1 if t >= knots[i] and
                                t <= knots[i + 1] else 0)
        else:
            d_1 = (knots[i + j] - knots[i])
            d_2 = (knots[i + j + 1] - knots[i + 1])
            func = lambda t: (
                (((t - knots[i]) / d_1) * N_basis(i, j - 1, knots, memo_table)(t)
                    if d_1 > 0 else 0) + 
                (((knots[i + j + 1] - t) / d_2) * N_basis(i + 1, j - 1, knots, memo_table)(t)
                    if d_2 > 0 else 0)
                )
        
        memo_table[key] = func
        return func        

def generate_bases(num_points):
    k = 3
    n = num_points - 1
    knots = [i for i in range(0, n + 2 - k)]
    # Side knots
    knots = [0 for i in range(0, k)] + knots
    knots = knots + [n + 1 - k for i in range(0, k)]
    memo_table = {}

    N_bases = [N_basis(i, k, knots, memo_table) for i in range(0, n + 1)]

    return N_bases

def BSpline_curve(bases, points, t):
    sum = [0 for _ in points[0]]
    for i in range(0, len(points)):
        sum = np.add(sum, np.multiply(bases[i](t), points[i])).tolist()
    return sum

def generate_curve(points, bases):
    return lambda t: BSpline_curve(bases, points, t)

def draw_curve(surface, n, curve, color):
    step = 0.002
    for i in range(0, int((n - 3) / step)):
        pt = curve(i * step)
        pt = [int(coord) for coord in pt]

        surface.set_at(pt, color)