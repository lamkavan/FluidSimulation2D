// CSC417: Final Project
// Real-time 2D Fluid Simulation
// Author: Kavan Lam (1003038802)
// Date: Dec 21, 2020

/*
Implementation is based on the paper here https://www.researchgate.net/publication/2560062_Real-Time_Fluid_Dynamics_for_Games by Jos Stam
 */

/*
The following is the starting point for executing the simulation. Here we setup our Processing
environment which will be used for rendering and displaying the fluid. We also setup our
fluid with hardcoded values for it's properties. These hardcoded values may be modified to
produce different behaviours for the fluid. This file also hosts the main simulation loop
and calls the appropriate fluid methods to advanced the simulation.
*/

import processing.core.PApplet;

public class Main extends PApplet{
    /* Hyperparameters (Feel free to change these accordingly) */
    // Display Constants
    public int screen_size = 150;  // This will also be the fluid size (the size of the fluid we are simulating)
    public int screen_scale = 4;  // Upscale factor so we can get a better look at the fluid

    // Fluid Constants
    public double density = 0.01;
    public double viscosity = 0.00005;
    public double diffusion_rate = 0.00005;  // Be careful to not set this too high otherwise the fluid will diffuse to quickly for you to see the animation

    // Simulation Constants
    public double time_step = 0.15;  // I recommend to keep this at 0.5. You can lower it to get slow motion animation
    public int gauss_seidel_iter = 30;

    /* Realtime simulation options */
    public boolean color_mode = false;  // Press C on the keyboard to toggle color mode (default is greyscale)

    /* The other parameters */
    public Fluid2D fluid;
    public int[] prev_mouse_location = {-1, -1};  // Used for ability to drag mouse to add dye
    public int[] mouse_drag_velocity = {0, 0};  // Used for ability to drag mouse to add dye

    public static void main(String[] args){
        String[] processingArgs = {"2D Fluid Simulation"};
        Main main_simulation_loop = new Main();

        // Ensure screen size is large enough
        if (main_simulation_loop.screen_size < 10){
            System.out.println("Simulation will has been terminated since the screen size is too small (size must be >= 10)");
            return;
        }

        // Print some information to the user
        System.out.println("Simulation starting. Enjoy!!!");
        System.out.println("Click and drag to add dye.");
        System.out.println("Use the arrow keys to shot dye in a certain direction.");
        System.out.println("Press C to toggle color mode.");
        System.out.println("Press V to reset the simulation.");

        // Start the Processing rendering and simulation
        PApplet.runSketch(processingArgs, main_simulation_loop);
    }

    public Main(){
        // Create and initialize our fluid
        this.fluid = new Fluid2D(this.screen_size, this.density, this.viscosity, this.diffusion_rate, this.gauss_seidel_iter);
    }

    public void settings(){
        // Create the display
        size(screen_size * screen_scale, screen_size * screen_scale);
    }

    public void setup(){
        // Sets the title for the Processing window
        surface.setTitle("2D Fluid Simulation");
    }

    public void draw(){
        /*
        This is the main simulation loop and is where we advance the fluid forward in time and render it.
         */

        // Set the background color (this also clears the previous frame)
        background(0, 0, 0);

        // Advance the fluid forward in time
        // First we deal with the velocities
        this.fluid.u = FluidOperations2D.diffusion(this.fluid.u, 1, this.time_step, this.fluid.fluid_size, this.fluid.viscosity, this.fluid.gauss_seidel_iter);
        this.fluid.v = FluidOperations2D.diffusion(this.fluid.v, 2, this.time_step, this.fluid.fluid_size, this.fluid.viscosity, this.fluid.gauss_seidel_iter);

        Object[] temp1 = FluidOperations2D.pressureProjection(this.fluid.u, this.fluid.v, this.fluid.fluid_size, this.time_step, this.fluid.density, this.fluid.gauss_seidel_iter);
        this.fluid.u = (double[]) temp1[0];
        this.fluid.v = (double[]) temp1[1];

        this.fluid.u = FluidOperations2D.advection(this.fluid.u, 1, this.time_step, this.fluid.fluid_size, this.fluid.u, this.fluid.v);
        this.fluid.v = FluidOperations2D.advection(this.fluid.v, 2, this.time_step, this.fluid.fluid_size, this.fluid.u, this.fluid.v);

        Object[] temp2 = FluidOperations2D.pressureProjection(this.fluid.u, this.fluid.v, this.fluid.fluid_size, this.time_step, this.fluid.density, this.fluid.gauss_seidel_iter);
        this.fluid.u = (double[]) temp2[0];
        this.fluid.v = (double[]) temp2[1];

        // Now deal with the dye
        this.fluid.dye = FluidOperations2D.diffusion(this.fluid.dye, 3, this.time_step, this.fluid.fluid_size, this.fluid.diffusion_rate, this.fluid.gauss_seidel_iter);
        this.fluid.dye = FluidOperations2D.advection(this.fluid.dye, 3, this.time_step, this.fluid.fluid_size, this.fluid.u, this.fluid.v);

        // Draw/render the 2D fluid by going over the dye array (render particle by particle where each particle is a pixel)
        for (int row = 0; row < this.fluid.fluid_size; row++){
            for (int col = 0; col < this.fluid.fluid_size; col++){
                double dye_amount = this.fluid.dye[idx(row, col, this.fluid.fluid_size)];
                dye_amount = Math.max(0, Math.min(dye_amount, 255));
                noStroke();
                if (this.color_mode){
                    colorMode(HSB, 100);
                    fill((float) dye_amount, (float) (dye_amount), 100);
                } else{
                    colorMode(RGB, 255);
                    fill((float) dye_amount, (float) dye_amount, (float) dye_amount);
                }
                rect(col * this.screen_scale, row * this.screen_scale, this.screen_scale, this.screen_scale);
            }
        }
    }

    public void keyPressed(){
        // Detect dye reset and color mode toggle
        if (key == 'C' || key == 'c'){
            this.color_mode = !this.color_mode;
        } else if (key == 'V' || key == 'v'){
            // Remove all the dye from the simulation to reset
            for (int row = 0; row < this.fluid.fluid_size; row++){
                for (int col = 0; col < this.fluid.fluid_size; col++){
                    this.fluid.dye[idx(row, col, this.fluid.fluid_size)] = 0.0;
                }
            }
        }

        // Detect if arrow keys are pressed to add fluid
        int[] velocity_to_use = {0, 0};
        int temp = (int)(this.screen_size / 2.0);
        if (keyCode == UP){  // Shot dye upwards
            velocity_to_use[1] = -15;
            this.fluid.add_dye(1500, this.screen_size - 3, temp);
            this.fluid.add_u(velocity_to_use[0], this.screen_size - 3, temp);
            this.fluid.add_v(velocity_to_use[1], this.screen_size - 3, temp);
        } else if (keyCode == DOWN){  // Shot dye downwards
            velocity_to_use[1] = 15;
            this.fluid.add_dye(1500, 3, temp);
            this.fluid.add_u(velocity_to_use[0], 3, temp);
            this.fluid.add_v(velocity_to_use[1], 3, temp);
        } else if (keyCode == RIGHT){  // Shot dye towards the right
            velocity_to_use[0] = 15;
            this.fluid.add_dye(1500, temp, 3);
            this.fluid.add_u(velocity_to_use[0], temp, 3);
            this.fluid.add_v(velocity_to_use[1], temp, 3);
        }  else if (keyCode == LEFT){  // Shot dye towards the left
            velocity_to_use[0] = -15;
            this.fluid.add_dye(1500, temp, this.screen_size - 3);
            this.fluid.add_u(velocity_to_use[0], temp, this.screen_size - 3);
            this.fluid.add_v(velocity_to_use[1], temp, this.screen_size - 3);
        }
    }

    public void mouseDragged(){
        /*
        Here we detect the moused begin clicked and dragged. Doing so will add dye to the fluid so
        you can see it move!
         */

        // Deal with the mouse location
        int[] mouse_position = {0, 0};
        mouse_position[0] = (mouseX / this.screen_scale);
        mouse_position[1] = (mouseY / this.screen_scale);

        if (mouse_position[0] > (this.screen_size - 2) || mouse_position[0] < 0 || mouse_position[1] > (this.screen_size - 2) || mouse_position[1] < 0){
            return;
        }

        if (this.prev_mouse_location[0] == -1){
            this.prev_mouse_location[0] = mouse_position[0];
            this.prev_mouse_location[1] = mouse_position[1];
        }

        // Add sources of dye and fluid velocity
        this.mouse_drag_velocity[0] = mouse_position[0] - this.prev_mouse_location[0];
        this.mouse_drag_velocity[1] = mouse_position[1] - this.prev_mouse_location[1];
        this.fluid.add_dye(255, mouse_position[1], mouse_position[0]);
        this.fluid.add_u(this.mouse_drag_velocity[0], mouse_position[1], mouse_position[0]);
        this.fluid.add_v(this.mouse_drag_velocity[1], mouse_position[1], mouse_position[0]);

        // Need to store prev mouse position so we can compute velocity next time
        this.prev_mouse_location = mouse_position;
    }

    public void mouseReleased(){
        this.prev_mouse_location[0] = -1;
        this.prev_mouse_location[1] = -1;
    }

    public int idx(int row, int col, int fluid_size){
        /*
        Converts a 2D index into a 1D index assuming a row wise flattening
        */
        return col + (row * fluid_size);
    }
}


