import numpy as np


def generate_hexagonal_prototype_crystal():
    """
    Generate a hexagonal prototype crystal with a c/a ratio of 1.0 and c axis parallel to the y coordinate axis.
    :return: 3xn array of vertex coordinates and nx3 array of vertex indices to indicate each triangle.
    """
    angles = 2.0 * np.pi * np.arange(0.0, 1.0, 1.0 / 6.0)
    vertices = np.array([np.cos(angles), np.sin(angles)])
    height = 1.0  # This should make c/a ration 1.0 by default
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


def generate_hexagonal_crystal(rot_a_std, rot_b_std, c_a_ratio):
    # Generate prototype hexagonal crystal with c/a ratio of 1.0 and c axis parallel to y coordinate axis.
    vertices, triangles = generate_hexagonal_prototype_crystal()

    vertices[1, :] = c_a_ratio * vertices[1, :]
    vertices /= vertices.max()

    # Calculate areas
    areas = np.zeros((triangles.shape[0],))
    # Basal faces
    big_basal_area = 0.5 * np.sqrt(3.0)
    small_basal_area = 0.5 * (1.5 * np.sqrt(3.0) - 2.0 * big_basal_area)
    areas[0] = small_basal_area
    areas[1] = big_basal_area
    areas[2] = big_basal_area
    areas[3] = small_basal_area
    areas[4] = small_basal_area
    areas[5] = big_basal_area
    areas[6] = big_basal_area
    areas[7] = small_basal_area
    # Prism faces
    areas[8:] = 0.5 * c_a_ratio

    # Make sure areas sum to 1.0 for easier probability calculations.
    areas /= np.sum(areas)

    # Rotate vertices of crystal
    rotate_a = rot_a_std * 2.0 * np.pi * np.random.randn()
    rotate_b = rot_b_std * 2.0 * np.pi * np.random.randn()
    rotate_c = 2.0 * np.pi * np.random.rand()
    vertices = rotate(vertices, rotate_a, rotate_b, rotate_c)

    # Calculate normals of crystal
    normals = get_normals(vertices, triangles)

    return vertices, triangles, normals, areas


def rotate(vertices, rotate_a, rotate_b, rotate_c):
    """
    Rotate vertices of a crystal.
    :param vertices: 3xn ndarray of coordinates.
    :param rotate_a: Rotation angle around crystal a-axis.
    :param rotate_b: Rotation angle around crystal b-axis.
    :param rotate_c: Rotation angle around crystal c-axis.
    :return: Modified vertex coordinates as 3xn array.
    """
    rasin = np.sin(rotate_a)
    racos = np.cos(rotate_a)
    vertices = np.array([
        vertices[0, :],
        racos * vertices[1, :] - rasin * vertices[2, :],
        rasin * vertices[1, :] + racos * vertices[2, :]
    ])

    rbsin = np.sin(rotate_b)
    rbcos = np.cos(rotate_b)
    vertices = np.array([
        rbcos * vertices[0, :] - rbsin * vertices[1, :],
        rbsin * vertices[0, :] + rbcos * vertices[1, :],
        vertices[2, :]
        ])

    rcsin = np.sin(rotate_c)
    rccos = np.cos(rotate_c)
    vertices = np.array([
        rccos * vertices[0, :] - rcsin * vertices[2, :],
        vertices[1, :],
        rcsin * vertices[0, :] + rccos * vertices[2, :]
    ])

    return vertices


def get_normals(vertices, triangles):
    """
    Calculate normals for each triangle in crystal.
    :param vertices: 3xn array of vertex coordinates.
    :param triangles: nx3 list of vertex indices.
    :return: 3xn array of normalized normal vectors.
    """
    normals = []
    for triangle in triangles:
        vertices_in_triangle = vertices[:, triangle]
        normal = np.cross(vertices_in_triangle[:, 2] - vertices_in_triangle[:, 0], vertices_in_triangle[:, 1] - vertices_in_triangle[:, 0])
        normal /= np.linalg.norm(normal)
        normals.append(normal)
    normals = np.array(normals).T
    return normals
