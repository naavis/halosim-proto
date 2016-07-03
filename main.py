import numpy as np

from halosim.crystals import generate_hexagonal_crystal
from halosim.plotting import plot_crystal
from halosim.raytracing import generate_primary_ray, get_primary_intersection

NUM_RAYS = 5
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
        ray = generate_primary_ray(SUN_AZIMUTH, SUN_ALTITUDE)

        # Find primary ray intersection point
        hit_triangle_index, intersection = get_primary_intersection(vertices, triangles, normals, areas, ray)

        if PLOT_EVERY_CRYSTAL:
            plot_crystal(vertices, triangles, ray, highlight_triangle=hit_triangle_index, point=intersection)


if __name__ == '__main__':
    main()
