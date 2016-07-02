import halosim.crystals
import halosim.plotting


def main():
    vertices, triangles = halosim.crystals.generate_hexagonal_crystal()
    halosim.plotting.plot_crystal(vertices, triangles)

if __name__ == '__main__':
    main()
