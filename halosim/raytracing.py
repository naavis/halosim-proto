import sys

import numpy as np


def generate_primary_ray(azimuth, altitude):
    """
    Generate incident primary ray from the sun/moon based on sun's
    azimuth and altitude. Point on the sun's disk is randomized.
    :param azimuth: Sun azimuth.
    :param altitude: Sun altitude.
    :return: Incident light ray.
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
    return -ray


def get_primary_intersection(vertices, triangles, normals, areas, ray):
    """
    Find random intersection point between primary ray and crystal.
    :param vertices: Crystal vertices as 3xn array.
    :param triangles: nx3 array of vertex indices.
    :param normals: 3xn array of normals.
    :param areas: Array of triangle areas.
    :param ray: Incident ray.
    :return: Index of hit triangle and exact point of intersection.
    """
    # Find triangle to intersect
    visible_triangles_indices = []
    projected_areas = []
    for triangle_idx, triangle in enumerate(triangles):
        normal = normals[:, triangle_idx]
        dot_product = np.dot(normal, -ray)
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


def get_reflectivity(normal, incident_ray, n1, n2):
    """
    Calculate reflectivity given a normal vector and an incident direction vector.
    :param n1: Refractive index of the first material.
    :param n2: Refractive index of the second material.
    :param normal: Normal vector for surface.
    :param incident_ray: Vector denoting direction of incident light.
    :return: Incident angle, reflectivity and transmitted angle.
    """
    incident_angle = np.arccos(np.dot(-incident_ray, normal))
    if n2 / n1 < np.sin(incident_angle):
        transmitted_angle = None
        reflectivity = 1.0
        return incident_angle, reflectivity, transmitted_angle
    transmitted_angle = np.arcsin(n1 * np.sin(incident_angle) / n2)
    reflectivity_parallel = np.square(n1 * np.cos(incident_angle) - n2 * np.cos(transmitted_angle) / (
        n1 * np.cos(incident_angle) + n2 * np.cos(transmitted_angle)))
    reflectivity_perpendicular = np.square(n1 * np.cos(transmitted_angle) - n2 * np.cos(incident_angle) / (
        n1 * np.cos(transmitted_angle) + n2 * np.cos(incident_angle)))
    reflectivity = 0.5 * (reflectivity_parallel + reflectivity_perpendicular)
    return incident_angle, reflectivity, transmitted_angle


def get_refraction_vector(normal, incident_angle, transmitted_angle, incident_ray, n1, n2):
    """
    Calculate refracted ray.
    :param n1: Refractive index of the first material.
    :param n2: Refractive index of the second material.
    :param normal: Surface normal.
    :param incident_angle: Incident ray angle.
    :param transmitted_angle: Transmitted ray angle.
    :param incident_ray: Incident ray.
    :return: Refracted ray.
    """
    normal_factor = n1 * np.cos(incident_angle) / n2 - np.sqrt(1.0 - np.square(np.sin(transmitted_angle)))
    refraction_vector = n1 * normal_factor * normal + incident_ray / n2
    refraction_vector /= np.linalg.norm(refraction_vector)
    return refraction_vector


def get_reflection_vector(normal, incident_angle, incident_ray):
    """
    Calculates reflected ray.
    :param normal: Surface normal.
    :param incident_angle: Incident ray angle.
    :param incident_ray: Incident ray.
    :return: Reflected ray.
    """
    reflection_vector = 2.0 * np.cos(incident_angle) * normal + incident_ray
    reflection_vector /= np.linalg.norm(reflection_vector)
    return reflection_vector


def ray_crystal_intersection(vertices, triangles, ray_origin, ray_direction):
    """
    Finds intersection point of a ray and a convex crystal.
    :param vertices: Vertices of the crystal.
    :param triangles: Vertex indices of each triangle.
    :param ray_origin: Starting point of ray.
    :param ray_direction: Ray direction.
    :return: Intersection point.
    """
    closest_distance = sys.float_info.max
    closest_triangle_idx = -1
    for triangle_idx, triangle in enumerate(triangles):
        triangle_vertices = vertices[:, triangle]
        dist = ray_triangle_intersection(triangle_vertices, ray_origin, ray_direction)
        if (dist is not None) and (dist < closest_distance):
            closest_distance = dist
            closest_triangle_idx = triangle_idx
    return ray_origin + closest_distance * ray_direction, closest_triangle_idx


def ray_triangle_intersection(triangle_vertices, ray_origin, ray_direction):
    """
    Ray-triangle intersection using Möller-Trumbore algorithm.
    :param triangle_vertices: 3x3 array of vertex coordinates.
    :param ray_origin: Vector corresponding to the ray origin.
    :param ray_direction: Unit vector corresponding to the ray direction.
    :return: Distance to intersection along given ray, or None.
    """
    edge0 = triangle_vertices[:, 1] - triangle_vertices[:, 0]
    edge1 = triangle_vertices[:, 2] - triangle_vertices[:, 0]
    p = np.cross(ray_direction, edge1)
    determinant = np.dot(edge0, p)
    inverse_determinant = 1.0 / determinant

    t = ray_origin - triangle_vertices[:, 0]
    bary_u = np.dot(t, p) * inverse_determinant
    if (bary_u < 0.0) or (bary_u > 1.0):
        return None

    q = np.cross(t, edge0)
    bary_v = np.dot(ray_direction, q) * inverse_determinant
    if (bary_v < 0.0) or (bary_u + bary_v > 1.0):
        return None

    t = np.dot(edge1, q) * inverse_determinant
    if t < 0.000001:
        return None

    return t
