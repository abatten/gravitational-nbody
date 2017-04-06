import tkinter as tk
import numpy as np
import time
import os
import sys
import argparse


######### CONSTANTS ##########
R_sun = 6.957e8 # Solar Radius in meters
M_sun = 2e30 # Solar Mass in kg
year = 365.25 * 24 * 60 * 60 # 1 year in s
grav_constant = 6.67e-11

################################################################################
class Particle:
    def __init__(self, init_pos, init_vel, mass, radius, colour, index):
        """ Initialise the parameters of the particle """

        self.position = init_pos
        self.velocity = init_vel
        self.mass = mass
        self.radius = radius
        self.colour = colour
        self.index = index

        self.properties()
        self.draw()

    def properties(self):
        """ Print out the properties of the particle. """

        print("Particle:", self.index)
        print("Position:", self.position)
        print("Velocity:", self.velocity)

    def draw(self):
        """ Draw the particle at its position."""

        frame.create_oval((self.position[0] * scale) - (self.radius * scale) - 2,
                          (self.position[1] * scale) - (self.radius * scale) - 2,
                          (self.position[0] * scale) + (self.radius * scale) - 2,
                          (self.position[1] * scale) + (self.radius * scale) - 2,
                          tag="Particle" + str(self.index) + "Shape",
                          fill=self.colour, disableddash=True)

    def distance_to(self, other):
        """
        Calculates the distance between itself and another particle.

        Args:
            other (particle): The particle to find the distance to.

        Returns:
            distance (float): The distance between the particles

        """

        x1 = self.position[0]
        x2 = other.position[0]

        y1 = self.position[1]
        y2 = other.position[1]

        distance = np.sqrt((x2 - x1)**2.0 + (y2 - y1)**2.0)

        return(distance)

    def update_position(self, dt, cycle):
        dx = self.velocity[0] * dt
        dy = self.velocity[1] * dt

        self.position[0] += dx
        self.position[1] += dy

        frame.move("Particle" + str(self.index) + "Shape", dx * scale, dy * scale)

################################################################################
def gravitation(particles, dt):
    for p1 in particles:
        for p2 in particles:
            if p1.index != p2.index: # No self gravity
                F = (grav_constant * p1.mass * p2.mass)/(p1.distance_to(p2))**2.0

                deltaX = p2.position[0] - p1.position[0]
                deltaY = p2.position[1] - p1.position[1]

                theta = np.arctan2(deltaX, deltaY)

                Fx = F * np.sin(theta)
                Fy = F * np.cos(theta)

                ax = Fx / p1.mass
                ay = Fy / p1.mass

                p1.velocity[0] += (ax * dt)
                p1.velocity[1] += (ay * dt)

                print("Particle: ", p1.index, p1.velocity)

def draw_grid(frame, window_size, box_size, tick_num, tick_length):
    """ Draws the grid lines and values around the outside of the box."""

    # Difference between adjacent tick values
    tick_jump = box_size / tick_num

    # Physical Distance between ticks on the screen
    tick_spacing = window_size / tick_num


    # Draw the tick marks
    for i in range(tick_num):
        frame.create_line(0, i * tick_spacing,
                          tick_length, i * tick_spacing,
                          tag="LeftTicks", fill="#000000")

        frame.create_line(window_size - tick_length, i * tick_spacing,
                          window_size, i * tick_spacing,
                          tag="RightTicks", fill="#000000")

        frame.create_line(i * tick_spacing, 0,
                          i * tick_spacing, tick_length, 
                          tag="TopTicks", fill="#000000")

        frame.create_line(i * tick_spacing, window_size - tick_length,
                          i * tick_spacing, window_size,
                          tag="BottomTicks", fill="#000000")

    # Annotate the tick marks with values
    for i in range(tick_num - 1):
        # Left Tick Labels
        frame.create_text(tick_length + 5, (i + 1) * tick_spacing,
                          text=str("{0:3f}".format((i + 1) * tick_jump)) + " Rsun", anchor="w")
        # Top Tick Labels
        frame.create_text((i + 1) * tick_spacing, tick_length + 5, 
                          text=str((i + 1) * tick_jump) + " Rsun", anchor="c")

################################################################################
if __name__ == "__main__":

    # Add the arguments for the user
    parser = argparse.ArgumentParser()
    parser.add_argument("--boxsize", help="The dimentions of the box in solar \
                         radii. Default: 1000", type=int)
    parser.add_argument("--timestep", help="The length of the time step \
                         between calculations", type=float)
    parser.add_argument("--windowsize", help="The height and width of the \
                         window in pixels. Default: 1000", type=int)
    parser.add_argument("--ticknum", help="The number of ticks on each side \
                         of the window. Default: 10", type=int)
    parser.add_argument("--ticklength", help="The length of each tick on the \
                         side of the window in pixels. Default: 20", type=int)

    args = parser.parse_args()


    # Setup defults and read arguments
    if args.windowsize:
        window_size = args.windowsize
    else:
        window_size = 1000

    if args.boxsize:
        box_size = args.boxsize * R_sun
        scale = window_size/box_size
    else:
        box_size = 1000 * R_sun
        scale = window_size/box_size

    if args.timestep:
        time_step = args.timestep
    else:
        time_step = 24 * 3600 # 1 day in seconds

    if args.ticknum:
        tick_num = args.ticknum
    else:
        tick_num = 10 

    if args.ticklength:
        tick_length = args.ticklength
    else:
        tick_length = 20 

    # Create window and frame 
    window = tk.Tk()
    window.title("N-Body Simulation")
    frame = tk.Canvas(window, height=str(window_size), width=str(window_size))
    frame.pack()


    draw_grid(frame, window_size, box_size, tick_num, tick_length)
    

    particle0 = Particle([100*R_sun, 100*R_sun], [0,10000], 2e30, 20 * R_sun, "#FF0000", 0)
    particle1 = Particle([300*R_sun, 450*R_sun], [9000,0], 2e30, 20 * R_sun, "#00FF00", 1)
    particle2 = Particle([900*R_sun, 900*R_sun], [2250,-2250], 2e30, 20 * R_sun, "#0000FF", 2)


    particles = [particle0, particle1, particle2]

    for i in range(10000):
        for j in range(len(particles)):
            gravitation(particles, time_step)
            particles[j].update_position(time_step, i)
            frame.update()
            time.sleep(0.005)

    tk.mainloop()