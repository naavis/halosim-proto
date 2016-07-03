from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
import matplotlib.pyplot as plt


def plot_crystal(vertices, triangles, ray, point=None):
    """
    Plot given crystal.
    :param point: Show point in plot.
    :param vertices: 3xn array of vertex coordinates.
    :param triangles: nx3 array of vertex indices.
    :param ray: Ray pointing to light source.
    """
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for triangle in triangles:
        vertices_in_triangle = vertices[:, triangle].T
        vertices_in_triangle = [vertices_in_triangle[:, [2, 0, 1]]]
        ax.add_collection3d(Poly3DCollection(vertices_in_triangle, facecolors='w', alpha=0.5))

    ax.plot([0.0, 3.0 * ray[2]], [0.0, 3.0 * ray[0]], [0.0, 3.0 * ray[1]], color='k')
    if point is not None:
        ax.scatter(point[2], point[0], point[1], color='r')

    ax.set_xlim(-1.0, 1.0)
    ax.set_ylim(-1.0, 1.0)
    ax.set_zlim(-1.0, 1.0)
    ax.set_xlabel('z')
    ax.set_ylabel('x')
    ax.set_zlabel('y')
    ax.set_aspect('equal')
    fig.tight_layout()

    plt.show()
