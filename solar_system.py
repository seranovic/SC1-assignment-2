import numpy as np
from scipy import constants
import matplotlib.pyplot as plt

positions = np.array([
    [0, 0],  # Sun
    [0, constants.astronomical_unit],  # Earth
    [0, 5.2*constants.astronomical_unit]  # Jupiter
])

velocities = np.array([[0, 0], [30e3, 0], [13e3, 0]])
masses = np.array([[2e30], [6e24], [2e27]])

gravitational_constant = constants.gravitational_constant
day = 24*60*60
year = 365*day
time_step = 7*day
time = 0

def get_forces(pos, mass):
    forces = np.zeros_like(pos)
    for idx in range(len(forces)):
        vectors = pos - pos[idx]
        distances_row = np.sum(vectors**2, axis=1)**0.5
        distances = distances_row[:, np.newaxis]
        distances[idx] = np.inf
        prefactors = gravitational_constant*mass*mass[idx]/distances**3
        pair_force = prefactors*vectors
        total_force = np.sum(pair_force, axis=0)
        forces[idx] = total_force
    return forces

plt.figure()

while time < 4*year:
    x = positions[:, 0]
    y = positions[:, 1]
    plt.plot(x, y, 'o')
    forces = get_forces(positions, masses)
    accelerations = forces / masses
    velocities = velocities + accelerations * time_step
    positions = positions + velocities * time_step
    time = time + time_step

plt.axis('equal')
plt.show()

