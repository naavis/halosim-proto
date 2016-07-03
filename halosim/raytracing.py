import numpy as np


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