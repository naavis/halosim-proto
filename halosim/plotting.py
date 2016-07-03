from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.pyplot as plt


def plot_crystal(vertices, triangles):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for triangle in triangles:
        vertices_in_triangle = vertices[:, triangle].T
        vertices_in_triangle = [vertices_in_triangle[:, [2, 0, 1]]]
        ax.add_collection3d(Poly3DCollection(vertices_in_triangle, facecolors='w', alpha=0.5))

    ax.set_xlim(-1.0, 1.0)
    ax.set_ylim(-1.0, 1.0)
    ax.set_zlim(-1.0, 1.0)
    ax.set_xlabel('z')
    ax.set_ylabel('x')
    ax.set_zlabel('y')
    ax.set_aspect('equal')
    fig.tight_layout()

    plt.show()
