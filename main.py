import numpy as np

from halosim.crystals import generate_hexagonal_crystal
from halosim.plotting import plot_crystal, plot_outgoing_rays
from halosim.raytracing import generate_primary_ray, get_primary_intersection, get_reflectivity, get_refraction_vector, \
    get_reflection_vector, ray_crystal_intersection

NUM_RAYS = 5000
PLOT_EVERY_CRYSTAL = False

# Alt/az
SUN_AZIMUTH = np.radians(0.0)
SUN_ALTITUDE = np.radians(50.0)


def main():
    outgoing_rays = np.zeros((3, NUM_RAYS))
    rot_a = np.radians(90.0)
    rot_a_std = np.radians(1.0)
    rot_b = np.radians(0.0)
    rot_b_std = np.radians(180.0)
    c_a_ratio = 2.0
    c_a_ratio_std = 0.01
    for ray_idx in range(NUM_RAYS):
        # Generate crystal
        vertices, triangles, normals, areas = generate_hexagonal_crystal(rot_a, rot_a_std, rot_b, rot_b_std, c_a_ratio,
                                                                         c_a_ratio_std)

        # Generate ray
        ray_direction = generate_primary_ray(SUN_AZIMUTH, SUN_ALTITUDE)

        # Find primary ray intersection point
        hit_triangle_index, intersection = get_primary_intersection(vertices, triangles, normals, areas, ray_direction)
        hit_normal = normals[:, hit_triangle_index]

        if PLOT_EVERY_CRYSTAL:
            plot_crystal(vertices, triangles, -ray_direction, highlight_triangle=hit_triangle_index, point=intersection)

        incident_angle, reflectivity, transmitted_angle = get_reflectivity(hit_normal, ray_direction, 1.0, 1.31)
        if np.random.rand() < reflectivity:
            # Reflect
            reflection_vector = get_reflection_vector(hit_normal, incident_angle, ray_direction)
            outgoing_rays[:, ray_idx] = -reflection_vector
        else:
            # Refract
            refraction_vector = get_refraction_vector(hit_normal, incident_angle, transmitted_angle,
                                                      ray_direction, 1.0, 1.31)
            inside_crystal = True
            normals = -normals  # Flip normals when inside crystal
            ray_origin = intersection
            ray_direction = refraction_vector
            while inside_crystal:
                intersection, triangle_index = ray_crystal_intersection(vertices, triangles, ray_origin, ray_direction)
                hit_normal = normals[:, triangle_index]
                incident_angle, reflectivity, transmitted_angle = get_reflectivity(hit_normal, ray_direction, 1.31, 1.0)
                if np.random.rand() < reflectivity:
                    ray_direction = get_reflection_vector(hit_normal, incident_angle, ray_direction)
                    ray_origin = intersection
                else:
                    outgoing_rays[:, ray_idx] = -get_refraction_vector(hit_normal, incident_angle, transmitted_angle,
                                                                       ray_direction, 1.31, 1.0)
                    inside_crystal = False

    plot_outgoing_rays(outgoing_rays, SUN_AZIMUTH, SUN_ALTITUDE)


if __name__ == '__main__':
    main()
