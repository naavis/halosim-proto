import numpy as np

from halosim.crystals import generate_hexagonal_crystal
from halosim.plotting import plot_crystal, plot_outgoing_rays
from halosim.raytracing import generate_primary_ray, get_primary_intersection, get_reflectivity, get_refraction_vector, \
    get_reflection_vector, ray_crystal_intersection

NUM_RAYS = 5000
PLOT_EVERY_CRYSTAL = False

# Alt/az
SUN_AZIMUTH = np.radians(0.0)
SUN_ALTITUDE = np.radians(45.0)


def main():
    outgoing_rays = np.zeros((3, NUM_RAYS))
    for ray_idx in range(NUM_RAYS):
        # Generate crystal
        rotation_std = np.radians(2.0)
        c_a_ratio = 0.25 + np.random.randn() * 0.01
        vertices, triangles, normals, areas = generate_hexagonal_crystal(rotation_std, rotation_std, c_a_ratio)

        # Generate ray
        ray_direction = generate_primary_ray(SUN_AZIMUTH, SUN_ALTITUDE)

        # Find primary ray intersection point
        hit_triangle_index, intersection = get_primary_intersection(vertices, triangles, normals, areas, ray_direction)
        hit_normal = normals[:, hit_triangle_index]

        if PLOT_EVERY_CRYSTAL:
            plot_crystal(vertices, triangles, -ray_direction, highlight_triangle=hit_triangle_index, point=intersection)

        incident_angle, reflectivity, transmitted_angle = get_reflectivity(hit_normal, ray_direction)
        if np.random.rand() < reflectivity:
            # Reflect
            reflection_vector = get_reflection_vector(hit_normal, incident_angle, ray_direction)
            outgoing_rays[:, ray_idx] = -reflection_vector
        else:
            # Refract
            refraction_vector = get_refraction_vector(hit_normal, incident_angle, transmitted_angle,
                                                      ray_direction)
            inside_crystal = True
            normals = -normals  # Flip normals when inside crystal
            ray_origin = intersection
            ray_direction = refraction_vector
            while inside_crystal:
                intersection, triangle_index = ray_crystal_intersection(vertices, triangles, ray_origin, ray_direction)
                hit_normal = normals[:, triangle_index]
                incident_angle, reflectivity, transmitted_angle = get_reflectivity(hit_normal, ray_direction)
                if np.random.rand() < reflectivity:
                    ray_direction = get_reflection_vector(hit_normal, incident_angle, ray_direction)
                    ray_origin = intersection
                else:
                    outgoing_rays[:, ray_idx] = -get_refraction_vector(hit_normal, incident_angle, transmitted_angle, ray_direction)
                    inside_crystal = False

    plot_outgoing_rays(outgoing_rays, SUN_AZIMUTH, SUN_ALTITUDE)


if __name__ == '__main__':
    main()
