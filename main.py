import halosim.crystals
import halosim.plotting
import numpy as np


def main():
    vertices, triangles = halosim.crystals.generate_hexagonal_crystal()

    rotate_a = 0.01 * 2.0 * np.pi * np.random.randn()
    rotate_b = 0.01 * 2.0 * np.pi * np.random.randn()
    rotate_c = 2.0 * np.pi * np.random.rand()
    vertices = halosim.crystals.rotate(vertices, rotate_a, rotate_b, rotate_c)

    normals = halosim.crystals.get_normals(vertices, triangles)

    halosim.plotting.plot_crystal(vertices, triangles)

if __name__ == '__main__':
    main()
