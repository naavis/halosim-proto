import numpy as np
import sys

from halosim.crystals import generate_hexagonal_crystal
from halosim.plotting import plot_crystal, plot_outgoing_rays
from halosim.raytracing import generate_primary_ray, get_primary_intersection, get_reflectivity

NUM_RAYS = 10000
PLOT_EVERY_CRYSTAL = False

# Alt/az
SUN_AZIMUTH = np.radians(0.0)
SUN_ALTITUDE = np.radians(10.0)


def main():
    outgoing_rays = np.zeros((3, NUM_RAYS))
    for ray_idx in range(NUM_RAYS):
        # Generate crystal
        rotation_std = 0.005
        c_a_ratio = 0.5 + np.random.randn() * 0.01
        vertices, triangles, normals, areas = generate_hexagonal_crystal(rotation_std, rotation_std, c_a_ratio)

        # Generate ray
        sun_direction = generate_primary_ray(SUN_AZIMUTH, SUN_ALTITUDE)

        # Find primary ray intersection point
        hit_triangle_index, intersection = get_primary_intersection(vertices, triangles, normals, areas, sun_direction)
        hit_triangle_normal = normals[:, hit_triangle_index]

        if PLOT_EVERY_CRYSTAL:
            plot_crystal(vertices, triangles, sun_direction, highlight_triangle=hit_triangle_index, point=intersection)

        incident_angle, reflectivity, transmitted_angle = get_reflectivity(hit_triangle_normal, sun_direction)
        if np.random.rand() < reflectivity:
            # Reflect
            reflection_vector = get_reflection_vector(hit_triangle_normal, incident_angle, sun_direction)
            outgoing_rays[:, ray_idx] = reflection_vector
        else:
            # Refract
            refraction_vector = get_refraction_vector(hit_triangle_normal, incident_angle, transmitted_angle,
                                                      sun_direction)
            inside_crystal = True
            normals = -normals
            ray_origin = intersection
            ray_direction = refraction_vector
            while inside_crystal:
                intersection, triangle_index = ray_crystal_intersection(vertices, triangles, ray_origin, ray_direction)
                incident_angle, reflectivity, transmitted_angle = get_reflectivity(normals[:, triangle_index], -ray_direction)
                if np.random.rand() < reflectivity:
                    ray_direction = get_reflection_vector(normals[:, triangle_index], incident_angle, -ray_direction)
                    ray_origin = intersection
                else:
                    outgoing_rays[:, ray_idx] = get_refraction_vector(normals[:, triangle_index], incident_angle, transmitted_angle, -ray_direction)
                    inside_crystal = False

            # Trace ray until it leaves the crystal

    plot_outgoing_rays(outgoing_rays)


def get_refraction_vector(hit_triangle_normal, incident_angle, transmitted_angle, sun_direction):
    normal_factor = np.cos(incident_angle) / 1.31 - np.sqrt(
        1.0 - np.square(np.sin(transmitted_angle)))
    refraction_vector = normal_factor * hit_triangle_normal - sun_direction / 1.31
    refraction_vector /= np.linalg.norm(refraction_vector)
    return refraction_vector


def get_reflection_vector(hit_triangle_normal, incident_angle, sun_direction):
    reflection_vector = 2.0 * np.cos(incident_angle) * hit_triangle_normal - sun_direction
    reflection_vector /= np.linalg.norm(reflection_vector)
    return reflection_vector


def ray_crystal_intersection(vertices, triangles, ray_origin, ray_direction):
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
    Ray-triangle intersection using Trumbore-Möller algorithm.
    :param triangle_vertices: 3x3 array of vertex coordinates.
    :param ray_origin: Vector corresponding to the ray origin.
    :param ray_direction: Unit vector corresponding to the ray direction.
    :return: Distance to intersection, or None.
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

if __name__ == '__main__':
    main()
