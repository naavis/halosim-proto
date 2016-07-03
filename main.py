import halosim.crystals
import halosim.plotting
import numpy as np

NUM_RAYS = 5
PLOT_EVERY_CRYSTAL = True

# Alt/az
SUN_AZIMUTH = np.radians(0.0)
SUN_ALTITUDE = np.radians(30.0)


def main():
    for ray_idx in range(NUM_RAYS):
        # Generate crystal
        vertices, triangles, normals, areas = halosim.crystals.generate_hexagonal_crystal(0.01, 0.01, 0.5)

        # Generate ray
        ray = generate_ray(SUN_AZIMUTH, SUN_ALTITUDE)

        visible_triangles_indices = []
        for triangle_idx, triangle in enumerate(triangles):
            normal = normals[:, triangle_idx]
            dot_product = np.dot(normal, ray)
            if dot_product > 0.0:
                visible_triangles_indices.append(triangle_idx)

        if PLOT_EVERY_CRYSTAL:
            halosim.plotting.plot_crystal(vertices, triangles, ray)


def generate_ray(azimuth, altitude):
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


if __name__ == '__main__':
    main()
