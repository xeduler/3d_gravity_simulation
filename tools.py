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