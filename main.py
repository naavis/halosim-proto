import numpy as np

from halosim.crystals import generate_hexagonal_crystal
from halosim.raytracing import generate_ray
from halosim.plotting import plot_crystal

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
        ray = generate_ray(SUN_AZIMUTH, SUN_ALTITUDE)

        # Find triangle to intersect
        visible_triangles_indices = []
        projected_areas = []
        for triangle_idx, triangle in enumerate(triangles):
            normal = normals[:, triangle_idx]
            dot_product = np.dot(normal, ray)
            if dot_product > 0.0:
                visible_triangles_indices.append(triangle_idx)
                projected_areas.append(np.cos(dot_product) * areas[triangle_idx])
        hit_triangle_idx = visible_triangles_indices[weighted_choice(projected_areas)]

        if PLOT_EVERY_CRYSTAL:
            plot_crystal(vertices, triangles, ray)


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

if __name__ == '__main__':
    main()
