from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
import matplotlib.pyplot as plt
import numpy as np


def plot_crystal(vertices, triangles, ray=None, point=None, highlight_triangle=None):
    """
    Plot given crystal.
    :param highlight_triangle: Highlight triangle with given index.
    :param point: Show point in plot.
    :param vertices: 3xn array of vertex coordinates.
    :param triangles: nx3 array of vertex indices.
    :param ray: Ray pointing to light source.
    """
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for idx, triangle in enumerate(triangles):
        vertices_in_triangle = vertices[:, triangle].T
        vertices_in_triangle = [vertices_in_triangle[:, [2, 0, 1]]]
        color = 'w'
        if (highlight_triangle is not None) and (idx is highlight_triangle):
            color = 'r'
        ax.add_collection3d(Poly3DCollection(vertices_in_triangle, facecolors=color, alpha=0.5))

    if ray is not None:
        ax.plot([0.0, 3.0 * ray[2]], [0.0, 3.0 * ray[0]], [0.0, 3.0 * ray[1]], color='k')

    if point is not None:
        ax.scatter(point[2], point[0], point[1], color='r', depthshade=False)

    ax.set_xlim(-1.0, 1.0)
    ax.set_ylim(-1.0, 1.0)
    ax.set_zlim(-1.0, 1.0)
    ax.set_xlabel('z')
    ax.set_ylabel('x')
    ax.set_zlabel('y')
    ax.set_aspect('equal')
    fig.tight_layout()

    plt.show()


def plot_outgoing_rays(rays, sun_azimuth, sun_altitude):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    norm_rays = rays / np.linalg.norm(rays, axis=0)
    ax.scatter(norm_rays[2, :], norm_rays[0, :], norm_rays[1, :], marker='.', depthshade=True, s=1)

    sun_direction = np.array([0.0, 0.0, 1.0])
    sun_direction = np.array([
        sun_direction[0],
        sun_direction[1] * np.cos(-sun_altitude) - sun_direction[2] * np.sin(-sun_altitude),
        sun_direction[1] * np.sin(-sun_altitude) + sun_direction[2] * np.cos(-sun_altitude)
    ])
    sun_direction = np.array([
        sun_direction[0] * np.cos(-sun_azimuth) - sun_direction[2] * np.sin(-sun_azimuth),
        sun_direction[1],
        sun_direction[0] * np.sin(-sun_azimuth) + sun_direction[2] * np.cos(-sun_azimuth)
    ])

    ax.scatter(sun_direction[2], sun_direction[0], sun_direction[1], s=50, depthshade=False, c='r')

    ax.set_xlim(-1.0, 1.0)
    ax.set_ylim(-1.0, 1.0)
    ax.set_zlim(-1.0, 1.0)
    ax.set_xlabel('z')
    ax.set_ylabel('x')
    ax.set_zlabel('y')
    ax.set_aspect('equal')
    fig.tight_layout()

    plt.show()
