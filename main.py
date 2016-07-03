import numpy as np

import halosim.crystals
import halosim.raytracing
import halosim.plotting

NUM_RAYS = 5
PLOT_EVERY_CRYSTAL = True

# Alt/az
SUN_AZIMUTH = np.radians(0.0)
SUN_ALTITUDE = np.radians(30.0)


def main():
    for ray_idx in range(NUM_RAYS):
        # Generate crystal
        vertices, triangles, normals, areas = halosim.crystals.generate_hexagonal_crystal(0.01, 0.01,
                                                                                          0.5 + np.random.randn() * 0.1)

        # Generate ray
        ray = halosim.raytracing.generate_ray(SUN_AZIMUTH, SUN_ALTITUDE)

        visible_triangles_indices = []
        for triangle_idx, triangle in enumerate(triangles):
            normal = normals[:, triangle_idx]
            dot_product = np.dot(normal, ray)
            if dot_product > 0.0:
                visible_triangles_indices.append(triangle_idx)

        if PLOT_EVERY_CRYSTAL:
            halosim.plotting.plot_crystal(vertices, triangles, ray)


if __name__ == '__main__':
    main()
