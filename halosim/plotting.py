from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.pyplot as plt


def plot_crystal(vertices, triangles):
    fig = plt.figure()
    ax = Axes3D(fig)
    for triangle in triangles:
        vertices_in_triangle = [vertices[:, triangle].T]
        ax.add_collection3d(Poly3DCollection(vertices_in_triangle))

    ax.set_xlim(-1.0, 1.0)
    ax.set_ylim(-1.0, 1.0)
    ax.set_zlim(-1.0, 1.0)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.set_aspect('equal')

    plt.show()
