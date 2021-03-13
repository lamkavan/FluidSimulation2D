# CSC417: Final Project
# Real-time 2D Fluid Simulation
# Author: Kavan Lam (1003038802)
# Date: Dec 21, 2020

"""
The following provides the required functions to advance a fluid forward
in time. The operations range from diffusion to pressure projection.
"""

import numpy as np
import math
import copy

def idx(row, col, fluid_size):
    """
    Converts a 2D index into a 1D index assuming a row wise flattening
    """
    return col + (row * fluid_size)


def pressureProjection(u, v, fluid_size, time_step, density, gauss_seidel_iter):
    """
    Apply a simplified version of pressure projection that does not use the staggered grid.
    This function is required to keep the simulation mass conserving or in other words
    enforce the fact that we are simulating a incompressible fluid.
    """
    particle_spacing = 1.0 / fluid_size
    divergence = np.zeros(u.shape[0])
    pressure = np.zeros(u.shape[0])

    # First compute the divergence of the velocity field at each cell
    for row in range(1, fluid_size - 1):
        for col in range(1, fluid_size - 1):
            divergence[idx(row, col, fluid_size)] = (-0.5 * particle_spacing) * ((u[idx(row, col + 1, fluid_size)] - u[idx(row, col - 1, fluid_size)]) +
                                                                                                             (v[idx(row + 1, col, fluid_size)] - v[idx(row - 1, col, fluid_size)]))
            pressure[idx(row, col, fluid_size)] = 0.0

    divergence = set_boundary_values(0, divergence, fluid_size)
    pressure = set_boundary_values(0, pressure, fluid_size)

    # Now compute the pressures by solving a linear system and we use the Gauss-Seidel method
    for iteration in range(gauss_seidel_iter):
        for row in range(1, fluid_size - 1):
            for col in range(1, fluid_size - 1):
                pressure[idx(row, col, fluid_size)] = (divergence[idx(row, col, fluid_size)] + pressure[idx(row + 1, col, fluid_size)] + pressure[idx(row - 1, col, fluid_size)]
                                                       + pressure[idx(row, col + 1, fluid_size)] + pressure[idx(row, col - 1, fluid_size)]) / 4.0

        pressure = set_boundary_values(0, pressure, fluid_size)

    # Finally update the velocities
    for row in range(1, fluid_size - 1):
        for col in range(1, fluid_size - 1):
            u[idx(row, col, fluid_size)] -= (0.5 / particle_spacing) * (pressure[idx(row, col + 1, fluid_size)] - pressure[idx(row, col - 1, fluid_size)])
            v[idx(row, col, fluid_size)] -= (0.5 / particle_spacing) * (pressure[idx(row + 1, col, fluid_size)] - pressure[idx(row - 1, col, fluid_size)])

    u = set_boundary_values(1, u, fluid_size)
    v = set_boundary_values(2, v, fluid_size)

    return u, v


def diffusion(array, diffuse_type, time_step, fluid_size, diffusion_rate, gauss_seidel_iter):
    """
    Diffuse some physical quantity throughout the fluid. This could be
    the horizontal velocities (diffuse_type = 1) or vertical velocities (diffuse_type = 2)
    or the dye (diffuse_type = 3). The new values are computed by solving a linear system and we
    use the Gauss-Seidel method to solve.
    """
    diffusion_factor = diffusion_rate * time_step * ((fluid_size - 2) ** 2)  # The factor should scale up with the fluid size

    # Diffuse the quantity stored in array
    array_new = copy.deepcopy(array)
    for iteration in range(gauss_seidel_iter):
        for row in range(1, fluid_size - 1):
            for col in range(1, fluid_size - 1):
                array_new[idx(row, col, fluid_size)] = (array[idx(row, col, fluid_size)] + diffusion_factor *
                                                 (array_new[idx(row - 1, col, fluid_size)] +
                                                  array_new[idx(row + 1, col, fluid_size)] +
                                                  array_new[idx(row, col - 1, fluid_size)] +
                                                  array_new[idx(row, col + 1, fluid_size)])) / (4.0 * diffusion_factor + 1.0)

        array_new = set_boundary_values(diffuse_type, array_new, fluid_size)

    return array_new


def advection(array, advect_type, time_step, fluid_size, u, v):
    """
    Applies advection to some physical quantity based u and v which are the
    horizontal and vertical velocities of the fluid system. If the physical quantity
    is dye then advect_type = 3. If the physical quantity is horizontal velocity then
    advect_type = 1 and advect_type = 2 for vertical velocity.
    """
    scaled_time_step = time_step * (fluid_size - 2)  # The time step scales with the fluid size

    # Advect the quantity stored in array
    array_new = np.zeros(array.shape[0])
    for row in range(1, fluid_size - 1):
        for col in range(1, fluid_size - 1):
            # Compute the cell of where the fluid particle would have came from
            other_row = row - (scaled_time_step * v[idx(row, col, fluid_size)])
            other_col = col - (scaled_time_step * u[idx(row, col, fluid_size)])

            # Clamp the other row and col so that it lies within the simulation border
            # All indices are relative to the cell center so a particle has 0.5 space to move within a cell
            # i.e if you are on the last row then you can still move 0.5 down further and still be in the fluid border
            if other_row < 0.5:
                other_row = 0.5
            elif other_row > ((fluid_size - 2) + 0.5):
                other_row = ((fluid_size - 2) + 0.5)

            if other_col < 0.5:
                other_col = 0.5
            elif other_col > ((fluid_size - 2) + 0.5):
                other_col = ((fluid_size - 2) + 0.5)

            # We employ a linear interpolation so we need the neighbouring particles
            neighbour_row_1 = math.floor(other_row)
            neighbour_row_2 = neighbour_row_1 + 1
            neighbour_col_1 = math.floor(other_col)
            neighbour_col_2 = neighbour_col_1 + 1

            # Get the weights for the interpolation
            weight_row_1 = other_row - neighbour_row_1
            weight_row_2 = 1 - weight_row_1
            weight_col_1 = other_col - neighbour_col_1
            weight_col_2 = 1 - weight_col_1

            # Linearly interpolate the advected quantity
            array_new[idx(row, col, fluid_size)] = weight_col_2 * (weight_row_2 * (array[idx(neighbour_row_1, neighbour_col_1, fluid_size)]) + weight_row_1 * (array[idx(neighbour_row_2, neighbour_col_1, fluid_size)]))
            array_new[idx(row, col, fluid_size)] += weight_col_1 * (weight_row_2 * (array[idx(neighbour_row_1, neighbour_col_2, fluid_size)]) + weight_row_1 * (array[idx(neighbour_row_2, neighbour_col_2, fluid_size)]))


    array_new = set_boundary_values(advect_type, array_new, fluid_size)

    return array_new


def set_boundary_values(diffuse_type, array_new, fluid_size):
    # Set all of the boarder values that are non corners
    for index in range(1, fluid_size - 1):
        # Left and right border
        if diffuse_type == 1:
            array_new[idx(index, 0, fluid_size)] = -1.0 * array_new[idx(index, 1, fluid_size)]
            array_new[idx(index, fluid_size - 1, fluid_size)] = -1.0 * array_new[idx(index, fluid_size - 2, fluid_size)]
        else:
            array_new[idx(index, 0, fluid_size)] = array_new[idx(index, 1, fluid_size)]
            array_new[idx(index, fluid_size - 1, fluid_size)] = array_new[idx(index, fluid_size - 2, fluid_size)]

        # Top and bottom border
        if diffuse_type == 2:
            array_new[idx(0, index, fluid_size)] = -1.0 * array_new[idx(1, index, fluid_size)]
            array_new[idx(fluid_size - 1, index, fluid_size)] = -1.0 * array_new[idx(fluid_size - 2, index, fluid_size)]
        else:
            array_new[idx(0, index, fluid_size)] = array_new[idx(1, index, fluid_size)]
            array_new[idx(fluid_size - 1, index, fluid_size)] = array_new[idx(fluid_size - 2, index, fluid_size)]


    # Set the value for the 4 corners (just average of the two closest non diagonal neighbours)
    # Top left
    array_new[idx(0, 0, fluid_size)] = (array_new[idx(1, 0, fluid_size)] + array_new[idx(0, 1, fluid_size)]) * 0.5
    # Bottom left
    array_new[idx(fluid_size - 1, 0, fluid_size)] = (array_new[idx(fluid_size - 2, 0, fluid_size)] + array_new[idx(fluid_size - 1, 1, fluid_size)]) * 0.5
    # Top right
    array_new[idx(0, fluid_size - 1, fluid_size)] = (array_new[idx(0, fluid_size - 2, fluid_size)] + array_new[idx(1, fluid_size - 1, fluid_size)]) * 0.5
    # Bottom right
    array_new[idx(fluid_size - 1, fluid_size - 1, fluid_size)] = (array_new[idx(fluid_size - 2, fluid_size - 1, fluid_size)] + array_new[idx(fluid_size - 1, fluid_size - 2, fluid_size)]) * 0.5

    return array_new


if __name__ == "__main__":
    print("Executing FluidOperations2D.py will do nothing. Please start the simulation via main.py")
