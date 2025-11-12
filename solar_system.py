'''A simulation of the solar system animated using the pygames module


Controls:
    [Enter] to reset velocities
    [Space] to pause / unpause
    [r] to rewind simulation.'''

import numpy as np
from scipy import constants
import matplotlib.pyplot as plt
import pygame

#initialising pygame
pygame.init()

#colors
BLACK = 0, 0, 0
WHITE = 255, 255, 255
BLUE = 0, 0, 255
RED = 255, 0, 0
YELLOW = 255, 255,0
CYAN = 0,255,255
MAGENTA = 255,0,255
MOCCASIN = 255,228,181
LIGHT_YELLOW = 255,255,224
DEEP_BLUE = 0,191,255
SKY_BLUE = 135,206,235
ORANGE = 255,69,0

#frame rate
frames_per_second = 60

positions = np.array([
    [0,0],  # Sun
    [0, constants.astronomical_unit],   #Earth
    [0,5.2*constants.astronomical_unit], #Jupiter
    [0,1.5*constants.astronomical_unit], #Mars
    [0,0.72*constants.astronomical_unit],#Venus
    [0,9.5*constants.astronomical_unit] #Saturn
])

velocities = np.array([[0, 0], [30e3, 0], [13e3, 0],[24e3,0],[35e3,0],[96e3,0]]) #sun, Earth, Jupiter, Mars, Venus,Saturn
masses = np.array([[2e30], [6e24], [2e27],[64e23],[486e24],[5683e26]]) #sun, Earth, Jupiter, Mars, Venus, Saturn

Colors =([Earth:'BLUE',Jupiter:'LIGHT_YELLOW',Mars:'RED',:Venus:'ORANGE',Saturn:'MOCCASIN'])

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

def draw_sun(surface):
    pygame.draw.circle(surface, 'YELLOW', (300, 200), 50)


#Game loop variables
running = True

#Game loop:

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

            # Space code
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:  # when the space key is pressed the sim pauses

            # r key code for reverse v
        if event.type == pygame.KEYDOWN and event.key == pygame.k_r:  # when r key is pressed the velocity is reveresed.

            # enter key code for positions and velocities reset when [Enter] is pressed.
        if event.type == pygame.KEYDOWN and event.key == pygame.k_ENTER:
    screen.fill(0,0,0)

    # Redraw the screen

    #Limit the framerate
    clock.tick(frames_per_second)

# Close game after the game loop

pygame.quit()
sys.exit()

