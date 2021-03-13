# CSC417: Final Project
# Real-time 2D Fluid Simulation
# Author: Kavan Lam (1003038802)
# Date: Dec 21, 2020

"""
The following models a fluid in 2 dimensions on a particle per particle basis where each pixel
represents one fluid particle.
"""

import numpy as np


class Fluid2D:
    def __init__(self, fluid_size, density, viscosity, diffusion_rate, gauss_seidel_iter):
        # Set the fluid properties
        self.fluid_size = fluid_size
        self.density = density
        self.viscosity = viscosity
        self.diffusion_rate = diffusion_rate

        # Create the empty numpy arrays to store the fluid state
        # Each array is a 1D row wise flatten version of the 2D counter part
        # fluid_size - 2 is used since there is a 1px thick border containing our fluid
        self.u = np.zeros(fluid_size ** 2)  # Velocities in the horizontal direction
        self.v = np.zeros(fluid_size ** 2)  # Velocities in the verticle direction
        self.dye = np.zeros(fluid_size ** 2)  # Amount of fluid

        # Other parameters
        self.gauss_seidel_iter = gauss_seidel_iter

    def add_u(self, amount, row, col):
        """
        Add some velocity in the horizontal direction to a particular location
        """
        index = col + (row * self.fluid_size)
        self.u[index] += amount

    def add_v(self, amount, row, col):
        """
        Add some velocity in the vertical direction to a particular location
        """
        index = col + (row * self.fluid_size)
        self.v[index] += amount

    def add_dye(self, amount, row, col):
        """
        Add some dye/fluid to a particular location on the simulation grid
        """
        index = col + (row * self.fluid_size)
        self.dye[index] += amount


if __name__ == "__main__":
    print("Executing Fluid2D.py will do nothing. Please start the simulation via main.py")