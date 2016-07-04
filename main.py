import numpy as np

from halosim.crystals import generate_hexagonal_crystal
from halosim.plotting import plot_crystal
from halosim.raytracing import generate_primary_ray, get_primary_intersection

NUM_RAYS = 10
PLOT_EVERY_CRYSTAL = True

# Alt/az
SUN_AZIMUTH = np.radians(0.0)
SUN_ALTITUDE = np.radians(30.0)


def main():
    for ray_idx in range(NUM_RAYS):
        # Generate crystal
        rotation_std = 0.01
        c_a_ratio = 0.5 + np.random.randn() * 0.01
        vertices, triangles, normals, areas = generate_hexagonal_crystal(rotation_std, rotation_std, c_a_ratio)

        # Generate ray
        sun_direction = generate_primary_ray(SUN_AZIMUTH, SUN_ALTITUDE)

        # Find primary ray intersection point
        hit_triangle_index, intersection = get_primary_intersection(vertices, triangles, normals, areas, sun_direction)
        hit_triangle_normal = normals[:, hit_triangle_index]

        incident_angle = np.arccos(np.dot(sun_direction, hit_triangle_normal))
        transmitted_angle = np.arcsin(np.sin(incident_angle) / 1.31)
        reflectivity_parallel = np.square(np.cos(incident_angle) - 1.31 * np.cos(transmitted_angle) / (
            np.cos(incident_angle) + np.cos(transmitted_angle)))
        reflectivity_perpendicular = np.square(np.cos(transmitted_angle) - 1.31 * np.cos(incident_angle) / (
            np.cos(transmitted_angle) + np.cos(incident_angle)))
        reflectivity = 0.5 * (reflectivity_parallel + reflectivity_perpendicular)
        if np.random.rand() < reflectivity:
            # Reflect
            reflection_vector = 2.0 * np.cos(incident_angle) * hit_triangle_normal - sun_direction
            reflection_vector /= np.linalg.norm(reflection_vector)
            # TODO: Record ray direction
        else:
            # Refract
            normal_factor = np.cos(incident_angle) / 1.31 - np.sqrt(
                1.0 - np.square(np.sin(transmitted_angle)))
            refraction_vector = normal_factor * hit_triangle_normal - sun_direction / 1.31
            # TODO: Trace ray until it exits the crystal and then record direction

        if PLOT_EVERY_CRYSTAL:
            plot_crystal(vertices, triangles, sun_direction, highlight_triangle=hit_triangle_index, point=intersection)


if __name__ == '__main__':
    main()
