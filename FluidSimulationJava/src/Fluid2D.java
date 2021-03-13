// CSC417: Final Project
// Real-time 2D Fluid Simulation
// Author: Kavan Lam (1003038802)
// Date: Dec 21, 2020

/*
Implementation is based on the paper here https://www.researchgate.net/publication/2560062_Real-Time_Fluid_Dynamics_for_Games by Jos Stam
 */

/*
The following models a fluid in 2 dimensions on a particle per particle basis where each pixel
represents one fluid particle.
*/

public class Fluid2D {
    // The fluid properties
    int fluid_size;
    double density;
    double viscosity;
    double diffusion_rate;

    // Create the arrays to store the fluid state
    // Each array is a 1D row wise flatten version of the 2D counter part
    // fluid_size - 2 is used since there is a 1px thick border containing our fluid
    double[] u; // Velocities in the horizontal direction
    double[] v;  // Velocities in the vertical direction
    double[] dye;  // Amount of fluid

    // Other parameters
    int gauss_seidel_iter;

    public Fluid2D(int fluid_size, double density, double viscosity, double diffusion_rate, int gauss_seidel_iter){
        this.fluid_size = fluid_size;
        this.density = density;
        this.viscosity = viscosity;
        this.diffusion_rate = diffusion_rate;
        this.gauss_seidel_iter = gauss_seidel_iter;

        this.u = new double[fluid_size * fluid_size];
        this.v = new double[fluid_size * fluid_size];
        this.dye = new double[fluid_size * fluid_size];
    }

    public void add_u(double amount, int row, int col){
        /*
        Add some velocity in the horizontal direction to a particular location
        */
        int index = col + (row * this.fluid_size);
        this.u[index] += amount;
    }

    public void add_v(double amount, int row, int col){
        /*
        Add some velocity in the vertical direction to a particular location
        */
        int index = col + (row * this.fluid_size);
        this.v[index] += amount;
    }

    public void add_dye(double amount, int row, int col){
        /*
        Add some dye/fluid to a particular location on the simulation grid
        */
        int index = col + (row * this.fluid_size);
        this.dye[index] += amount;
    }

    public static void main(String[] args){
        System.out.println("Executing Fluid2D.java will do nothing. Please start the simulation via Main.java");
    }
}
