import numpy as np


def generate_primary_ray(azimuth, altitude):
    """
    Generate primary rays pointing to the sun/moon based on sun's
    azimuth and altitude. Point on the sun's disk is randomized.
    :param azimuth:
    :param altitude:
    :return:
    """
    sun_diameter = 0.0087266  # 0.5 degrees in radians
    azimuth = azimuth + np.random.rand() * sun_diameter - 0.5 * sun_diameter
    altitude = altitude + np.random.rand() * sun_diameter - 0.5 * sun_diameter
    ray = np.array([0.0, 0.0, 1.0])
    ray = np.array([
        ray[0],
        ray[1] * np.cos(-altitude) - ray[2] * np.sin(-altitude),
        ray[1] * np.sin(-altitude) + ray[2] * np.cos(-altitude)
    ])
    ray = np.array([
        ray[0] * np.cos(-azimuth) - ray[2] * np.sin(-azimuth),
        ray[1],
        ray[0] * np.sin(-azimuth) + ray[2] * np.cos(-azimuth)
    ])
    return ray


def get_primary_intersection(vertices, triangles, normals, areas, ray):
    """
    Find random intersection point between primary ray and crystal.
    :param vertices: Crystal vertices as 3xn array.
    :param triangles: nx3 array of vertex indices.
    :param normals: 3xn array of normals.
    :param areas: Array of triangle areas.
    :param ray: Ray pointing towards light source.
    :return: Index of hit triangle and exact point of intersection.
    """
    # Find triangle to intersect
    visible_triangles_indices = []
    projected_areas = []
    for triangle_idx, triangle in enumerate(triangles):
        normal = normals[:, triangle_idx]
        dot_product = np.dot(normal, ray)
        if dot_product > 0.0:
            visible_triangles_indices.append(triangle_idx)
            projected_areas.append(dot_product * areas[triangle_idx])

    # Find intersection point using barycentric coordinates
    hit_triangle_idx = visible_triangles_indices[weighted_choice(projected_areas)]
    hit_triangle_vertices = vertices[:, triangles[hit_triangle_idx]]
    bary_a = np.random.rand()
    bary_b = np.random.rand() * (1.0 - bary_a)
    bary = np.array([bary_a, bary_b, 1.0 - bary_a - bary_b])
    intersection = np.dot(hit_triangle_vertices, bary)
    return hit_triangle_idx, intersection


def weighted_choice(weights):
    """
    Choose random item with given probabilities.
    E.g. weighted_choice([1.0, 0.5]) would return 0 twice as often as 1.
    Based on third implementation in: http://eli.thegreenplace.net/2010/01/22/weighted-random-generation-in-python/
    :param weights: Probabilities for each element.
    :return: Index of randomly chosen element.
    """
    rnd = np.random.rand() * sum(weights)
    for i, w in enumerate(weights):
        rnd -= w
        if rnd < 0:
            return i


def get_reflectivity(normal, incident_vector):
    """
    Calculate reflectivity given a normal vector and an incident direction vector.
    :param normal: Normal vector for surface.
    :param incident_vector: Vector denoting direction of incident light (note: points away from surface).
    :return: Incident angle, reflectivity and transmitted angle.
    """
    incident_angle = np.arccos(np.dot(incident_vector, normal))
    transmitted_angle = np.arcsin(np.sin(incident_angle) / 1.31)
    reflectivity_parallel = np.square(np.cos(incident_angle) - 1.31 * np.cos(transmitted_angle) / (
        np.cos(incident_angle) + np.cos(transmitted_angle)))
    reflectivity_perpendicular = np.square(np.cos(transmitted_angle) - 1.31 * np.cos(incident_angle) / (
        np.cos(transmitted_angle) + np.cos(incident_angle)))
    reflectivity = np.minimum(1.0, 0.5 * (reflectivity_parallel + reflectivity_perpendicular))
    return incident_angle, reflectivity, transmitted_angle
