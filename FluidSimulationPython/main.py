# CSC417: Final Project
# Real-time 2D Fluid Simulation
# Author: Kavan Lam (1003038802)
# Date: Dec 21, 2020


# Implementation is based on the paper here https://www.researchgate.net/publication/2560062_Real-Time_Fluid_Dynamics_for_Games by Jos Stam


"""
The following is the starting point for executing the simulation. Here we setup our pygame
environment which will be used for rendering and displaying the fluid. We also setup our
fluid with hardcoded values for it's properties. These hardcoded values may be modified to
produce different behaviours for the fluid. This file also hosts the main simulation loop
and calls the appropriate fluid methods to advanced the simulation.
"""

####################################################################
# NOTE: The Python version is very slow so we need to keep the     #
# screen size and gauss_seidel_iter low                            #
####################################################################

import pygame
from Fluid2D import *
from FluidOperations2D import *

### Hyperparameters (Feel free to change these accordingly) ###
# Display Constants
screen_size = 30  # This will also be the fluid size (the size of the fluid we are simulating)
screen_scale = 20

# Fluid Constants
density = 0.1
viscosity = 0.0005
diffusion_rate = 0.000001

# Simulation Constants
time_step = 0.5
gauss_seidel_iter = 2
###############################################################

# Initialize pygame
pygame.init()

# Create the display
display = pygame.display.set_mode((screen_size * screen_scale, screen_size * screen_scale))
pygame.display.set_caption("2D Fluid Simulation")

# Setup the simulation clock
clock = pygame.time.Clock()

# Create and initialize our fluid
my_fluid = Fluid2D(screen_size, density, viscosity, diffusion_rate, gauss_seidel_iter)

# Main simulation loop
run_simulation = True
prev_mouse_location = np.array([-1, -1])

while run_simulation:
    # Set the background color
    display.fill((0, 0, 0))

    # Go through the list of events and act accordingly
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run_simulation = False

        elif event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0] == 1:
            # Deal with the mouse location
            mouse_position = np.array([int(pygame.mouse.get_pos()[0] / screen_scale), int(pygame.mouse.get_pos()[1] / screen_scale)])
            if prev_mouse_location[0] == -1:
                prev_mouse_location[0] = mouse_position[0]
                prev_mouse_location[1] = mouse_position[1]

            # Add sources of dye and fluid velocity
            mouse_drag_velocity = mouse_position - prev_mouse_location
            my_fluid.add_dye(255, mouse_position[1], mouse_position[0])
            my_fluid.add_u(mouse_drag_velocity[0], mouse_position[1], mouse_position[0])
            my_fluid.add_v(mouse_drag_velocity[1], mouse_position[1], mouse_position[0])

            # Need to store prev mouse position so we can compute velocity next time
            prev_mouse_location = mouse_position

        elif event.type == pygame.MOUSEBUTTONUP:
            prev_mouse_location = np.array([-1, -1])

    # Advance the simulation forward in time
    my_fluid.u = diffusion(my_fluid.u, 1, time_step, my_fluid.fluid_size, viscosity, gauss_seidel_iter)
    my_fluid.v = diffusion(my_fluid.v, 2, time_step, my_fluid.fluid_size, viscosity, gauss_seidel_iter)

    my_fluid.u, my_fluid.v = pressureProjection(my_fluid.u, my_fluid.v, my_fluid.fluid_size, time_step, density, gauss_seidel_iter)

    my_fluid.u = advection(my_fluid.u, 1, time_step, my_fluid.fluid_size, my_fluid.u, my_fluid.v)
    my_fluid.v = advection(my_fluid.v, 2, time_step, my_fluid.fluid_size, my_fluid.u, my_fluid.v)

    my_fluid.u, my_fluid.v = pressureProjection(my_fluid.u, my_fluid.v, my_fluid.fluid_size, time_step, density, gauss_seidel_iter)

    my_fluid.dye = diffusion(my_fluid.dye, 3, time_step, my_fluid.fluid_size, diffusion_rate, gauss_seidel_iter)
    my_fluid.dye = advection(my_fluid.dye, 3, time_step, my_fluid.fluid_size, my_fluid.u, my_fluid.v)

    # Draw/render the 2D fluid by going over the dye array
    for row in range(my_fluid.fluid_size):
        for col in range(my_fluid.fluid_size):
            dye_amount = my_fluid.dye[idx(row, col, my_fluid.fluid_size)]
            dye_amount = max(0, min(dye_amount, 255))
            pygame.draw.rect(display, (dye_amount, dye_amount, dye_amount), (col * screen_scale, row * screen_scale, screen_scale, screen_scale))

    # Update the display with the new frame
    pygame.display.update()
    clock.tick(60)
