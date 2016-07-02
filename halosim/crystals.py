import numpy as np


def generate_hexagonal_crystal():
    angles = 2.0 * np.pi * np.arange(0.0, 1.0, 1.0 / 6.0)
    vertices = np.array([np.cos(angles), np.sin(angles)])
    height = 0.5
    xs = np.tile(vertices[0, :], 2)
    ys = np.concatenate((np.tile(height, 6), np.tile(-height, 6)))
    zs = np.tile(vertices[1, :], 2)

    triangles = np.zeros((20, 3), np.int)
    # Top basal face
    triangles[0] = [0, 1, 2]
    triangles[1] = [0, 2, 5]
    triangles[2] = [2, 3, 5]
    triangles[3] = [3, 4, 5]
    # Bottom basal face
    triangles[4] = [6, 8, 7]
    triangles[5] = [6, 11, 8]
    triangles[6] = [8, 11, 9]
    triangles[7] = [9, 11, 10]
    # Prism faces
    triangles[8] = [0, 5, 11]
    triangles[9] = [0, 11, 6]
    triangles[10] = [4, 10, 5]
    triangles[11] = [5, 10, 11]
    triangles[12] = [3, 9, 4]
    triangles[13] = [4, 9, 10]
    triangles[14] = [2, 8, 3]
    triangles[15] = [3, 8, 9]
    triangles[16] = [1, 7, 2]
    triangles[17] = [2, 7, 8]
    triangles[18] = [0, 6, 1]
    triangles[19] = [1, 6, 7]

    return np.array([xs, ys, zs]), triangles
