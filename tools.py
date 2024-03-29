from math import tan
import numpy as np
from OpenGL.GL import glMultMatrixf

def perspective_projection(fovy, aspect, zNear, zFar):
    f = 1.0 / tan(fovy / 2.0)
    matrix = [
        f / aspect, 0, 0, 0,
        0, f, 0, 0,
        0, 0, (zFar + zNear) / (zNear - zFar), -1,
        0, 0, (2.0 * zFar * zNear) / (zNear - zFar), 0
    ]
    glMultMatrixf(matrix)



def dists(pos0, pos1):
    return np.sum((pos0 - pos1) ** 2)




def acceleration_vector(force, pos0, pos1):
    diff = pos1 - pos0

    part = force / np.sum(np.abs(diff))
    return diff * part