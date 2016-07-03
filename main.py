import halosim.crystals
import halosim.plotting
import numpy as np

NUM_RAYS = 3
PLOT_EVERY_CRYSTAL = False

# Alt/az in degrees
SUN_AZIMUTH = 180.0
SUN_ALTITUDE = 30.0


def main():
    for ray_idx in range(NUM_RAYS):
        vertices, triangles = halosim.crystals.generate_hexagonal_crystal()

        rotate_a = 0.01 * 2.0 * np.pi * np.random.randn()
        rotate_b = 0.01 * 2.0 * np.pi * np.random.randn()
        rotate_c = 2.0 * np.pi * np.random.rand()
        vertices = halosim.crystals.rotate(vertices, rotate_a, rotate_b, rotate_c)

        normals = halosim.crystals.get_normals(vertices, triangles)

        # Generate ray
        # Currently the ray is always the same; later on direction can be randomized on sun's disk.
        ray = np.array([0.0, 0.0, 1.0])
        ray = np.array([
            ray[0],
            np.cos(SUN_ALTITUDE) - np.sin(SUN_ALTITUDE),
            np.sin(SUN_ALTITUDE) + np.cos(SUN_ALTITUDE)
        ])
        ray = np.array([
            np.cos(SUN_AZIMUTH) - np.sin(SUN_AZIMUTH),
            ray[1],
            np.sin(SUN_AZIMUTH) + np.cos(SUN_AZIMUTH)
        ])

        visible_triangles = []
        for triangle_idx, triangle in enumerate(triangles):
            normal = normals[:, triangle_idx]
            dot_product = np.dot(normal, ray)
            if dot_product > 0.0:
                visible_triangles.append(triangle_idx)

        if PLOT_EVERY_CRYSTAL:
            halosim.plotting.plot_crystal(vertices, triangles)

if __name__ == '__main__':
    main()
