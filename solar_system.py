'''A simulation of the solar system animated using the pygames module


Controls:
    [Enter] to reset velocities
    [Space] to pause / unpause
    [r] to rewind simulation.'''

import numpy as np
from scipy import constants
import matplotlib.pyplot as plt
import pygame
import sys

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
    # [0,5.2*constants.astronomical_unit], #Jupiter
    # [0,1.5*constants.astronomical_unit], #Mars
    # [0,0.72*constants.astronomical_unit],#Venus
    # [0,9.5*constants.astronomical_unit] #Saturn
])

velocities = np.array([
    [0, 0], # sun
    [30e3, 0], # earth
    # [13e3, 0], # jupiter
    # [24e3,0], # mars
    # [35e3,0], # venus
    # [96e3,0] # saturn
])
masses = np.array([
    [2e30], # sun
    [6e24], # earth
    # [2e27], # jupiter
    # [64e23], # mars
    # [486e24], # venus
    # [5683e26] # saturn
])

Colors = {
    'Earth' : BLUE,
    'Jupiter' : LIGHT_YELLOW,
    'Mars' : RED,
    'Venus' : ORANGE,
    'Saturn' : MOCCASIN
}

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

def draw_planets(surface, positions, colors, radii):
    for idx in range(len(positions)):
        pygame.draw.circle(surface, YELLOW, positions[idx], 50)


# Initialize PyGame
pygame.init()
# Create PyGame screen:
# 1. specify screen size
screen_width, screen_height = 800, 600
# 2. define screen
screen = pygame.display.set_mode((screen_width, screen_height))
# 3. set caption
pygame.display.set_caption("Solar System")

# Update pygames clock use the framerate
clock = pygame.time.Clock()

#Game loop variables
running = True
moving = True
pos_init = positions
vel_init = velocities
mass_init = masses

#Game loop:

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:  # when the space key is pressed the sim pauses
            moving = not moving

        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:  # when r key is pressed the velocity is reversed.
            time_step = -time_step
            print("reverse")

        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            positions = pos_init
            velocities = vel_init
            masses = mass_init

    screen.fill(BLACK)

    if moving:
        x = positions[:, 0]
        y = positions[:, 1]
        print(f"x: {x}")
        print(f"y: {y}")
        forces = get_forces(positions, masses)
        accelerations = forces / masses
        velocities = velocities + accelerations * time_step
        positions = positions + velocities * time_step
        time = time + time_step

    # Redraw the screen
    pygame.display.flip()

    #Limit the framerate
    clock.tick(frames_per_second)

# Close game after the game loop

pygame.quit()
sys.exit()

