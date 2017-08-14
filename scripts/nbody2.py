import pygame as pyg

import numpy as np 
import argparse
import sys
import os
import configparser as config 

import constants as C

class Particle:
    """
    Class to represent point masses.

    Parameters
    ----------
    pos : [float, float, float]
        The particle position in the window
        Unit: Rsun
    vel : [float, float, float]
        Array of velocities of the partcle
        Unit: km/s
    mas : float
        Mass of the particle.
        Unit Msun
    dex : int
        Index of the particle
    col : (int, int, int)
        Colour of the particle

    """
    def __init__(self, win, init_pos, init_vel, mass=1, rad=1, dex=0, col=(0,0,0)):
        self.pos = [x * C.XRSUN for x in init_pos] # Conver to meters
        self.vel = [v * C.XKM for v in init_vel]  # Convert to meters
        self.mas = mass * C.XMSUN  # Convert to kilograms
        self.rad = rad #* C.XRSUN  #  Convert to meters
        self.dex = dex
        self.col = col


    def __repr__(self):
        return ('Position:{x} Velocity:{v} Mass:{m} Radius:{r} Index:{d} Colour:{c}'.format(
                x=self.pos, v=self.vel, m=self.mas, r=self.rad, d=self.dex, c=self.col))


    def draw(self, win, SCALE):
        """
        Draws the particle in its initial position.

        Parameters
        ----------
        win : pygame.display
            The window to draw the particle

        Returns
        -------
        NONE
        """
        pyg.draw.circle(win, self.col, (int(self.pos[0]/C.XRSUN*SCALE), int(self.pos[1]/C.XRSUN*SCALE)), int(self.rad*SCALE) + 2 , 0)


    def dist_to(self, other):
        """
        Calculates the distance between itself an another particle.

        Parameters
        ----------
        other : particle
            The particle to find the distance to.
    
        Returns
        -------
        dist : float
            The distance between the two particles   
        """

        x1 = self.pos[0]
        y1 = self.pos[1]
        z1 = self.pos[2]

        x2 = other.pos[0]
        y2 = other.pos[1]
        z2 = other.pos[2]

        dist = np.sqrt((x1 - x2)**2.0 + (y1 - y2)**2.0 + (z1 - z2)**2.0)

        return dist


    def acceleration(self, position, particleList):
        """
        Finds the acceleration on a particle due to all other particles.

        Parameters
        ----------
        position : float
            The position at which to calculate the gravitational acceleration
        particle_list : list
            List of all gravitating particles
    
        Returns
        -------
        a : [float, float, float]
            The acceleration comppnents on the particle   
        """   
        ax = 0
        ay = 0
        az = 0

        for p1 in particleList:
            if p1 is not self:
                dX = (p1.pos[0] - position[0])
                dY = (p1.pos[1] - position[1])
                dZ = (p1.pos[2] - position[2])

                d = self.dist_to(p1)
                dsquared = d**2.0

                #  C.XG is Gravitational Strength
                Force = C.XG * self.mas * p1.mas / dsquared
                ax += (Force / self.mas) * (dX / d)
                ay += (Force / self.mas) * (dY / d)
                az += (Force / self.mas) * (dZ / d)

        return ax, ay, az



def rk4(particle, particleList, dt):
    """
    Returns the position and velocity of a particle after a given timestep.

    Finds the new position and velocity of a particle by using the 
    Runge-Kutta method (RK4).  

    Parameters
    ----------
    particle : Particle
        The particle whose position and velosities are to be updated.
    particleList : List
        The list of all gravitating particles in the simulation.
    dt : float
        The timestep to increase by.

    Returns
    -------
    new_pos : [float, float, float]
        The cordinates of the new position of the particle.
    new_vel : [float, float, float]
        The components of the new velocity of the particle.
    """
    #  Current Velocity   
    vx1 = particle.vel[0]
    vy1 = particle.vel[1]
    vz1 = particle.vel[2]

    #  Current Position
    px1 = particle.pos[0] 
    py1 = particle.pos[1] 
    pz1 = particle.pos[2] 

    #  Current Acceleration
    ax1, ay1, az1 = particle.acceleration([px1, py1, pz1], particleList)

    #  Step 2
    vx2 = vx1 + 0.5 * dt * ax1
    vy2 = vy1 + 0.5 * dt * ay1
    vz2 = vz1 + 0.5 * dt * az1

    px2 = px1 + 0.5 * dt * vx2
    py2 = py1 + 0.5 * dt * vy2
    pz2 = pz1 + 0.5 * dt * vz2

    ax2, ay2, az2 = particle.acceleration([px2, py2, pz2], particleList)

    #  Step 3
    vx3 = vx1 + 0.5 * dt * ax2
    vy3 = vy1 + 0.5 * dt * ay2
    vz3 = vz1 + 0.5 * dt * az2

    px3 = px1 + 0.5 * dt * vx3
    py3 = py1 + 0.5 * dt * vy3
    pz3 = pz1 + 0.5 * dt * vz3

    ax3, ay3, az3 = particle.acceleration([px3, py3, pz3], particleList)

    #  Step 4
    vx4 = vx1 + 0.5 * dt * ax3
    vy4 = vy1 + 0.5 * dt * ay3
    vz4 = vz1 + 0.5 * dt * az3

    px4 = px1 + 0.5 * dt * vx4
    py4 = py1 + 0.5 * dt * vy4
    pz4 = pz1 + 0.5 * dt * vz4

    ax4, ay4, az4 = particle.acceleration([px3, py3, pz3], particleList)

    #  Final positions and velocities
    new_vx = vx1 + (1.0/6.0) * dt * (ax1 + 2 * (ax2 + ax3) + ax4)
    new_vy = vy1 + (1.0/6.0) * dt * (ay1 + 2 * (ay2 + ay3) + ay4)
    new_vz = vz1 + (1.0/6.0) * dt * (az1 + 2 * (az2 + az3) + az4)

    new_px = px1 + (1.0/6.0) * dt * (vx1 + 2 * (vx2 + vx3) + vx4)
    new_py = py1 + (1.0/6.0) * dt * (vy1 + 2 * (vy2 + vy3) + vy4)
    new_pz = pz1 + (1.0/6.0) * dt * (vz1 + 2 * (vz2 + vz3) + vz4)
  
    new_vel = [new_vx, new_vy, new_vz]
    new_pos = [new_px, new_py, new_pz]

    return new_pos, new_vel


def update_particles(win, Plist, dt, SCALE):
    for i in range(len(Plist)):
        Plist[i].pos, Plist[i].vel = rk4(Plist[i], Plist, dt)
        Plist[i].draw(win, SCALE)


def draw_axes(win, WINSIZE, BOXSIZE, TICKNUM, TICKLEN):
    """
    Draws the grid lines and labels around the outside of the box.

    Parameters
    ----------
    win : pygame.display
        The window to draw the axes in.
    WINSIZE : int
        The height and width of the window to be created.
    BOXSIZE : int
        The hight and width of the window in physical units.
    TICKNUM : int
        The number of tick marks along each edge of the window.
    TICKLEN : int
        The length of with tick mark in pixels.
    
    Returns
    -------
    NONE   
    """

    TICKJUMP = BOXSIZE / TICKNUM  # Value difference between axis labels
    TICKSPACE = WINSIZE / TICKNUM  # Physical distance bwtween axis labels
    TICKCOLOUR = 0x000000  # Black
    TICKTHICK = 2  # THickness of the ticks

    # Draw the tick marks
    for i in range(TICKNUM):

        #  Left Ticks
        pyg.draw.line(win, TICKCOLOUR, (0, i * TICKSPACE),
                          (TICKLEN, i * TICKSPACE), TICKTHICK)
        #  Right Ticks
        pyg.draw.line(win, TICKCOLOUR, (WINSIZE - TICKLEN, i * TICKSPACE),
                          (WINSIZE, i * TICKSPACE), TICKTHICK)
        #  Top Ticks
        pyg.draw.line(win, TICKCOLOUR, (i * TICKSPACE, 0),
                          (i * TICKSPACE, TICKLEN), TICKTHICK)
        # Bottom Ticks
        pyg.draw.line(win, TICKCOLOUR, (i * TICKSPACE, WINSIZE - TICKLEN),
                          (i * TICKSPACE, WINSIZE), TICKTHICK)      

    #  Font Type    
    label_font = pyg.font.SysFont("monospace", 13)
    LABELPAD = 5  # Padding around the ticks for the label
    LABELCOLOUR = (0,0,0)  # Font colour of the labels

    for i in range(TICKNUM -1):
        #  Create Labels
        label = label_font.render(str("{0:.1f}".format(
                                 (i + 1) * TICKJUMP / C.XRSUN)) + "Rsun", 
                                 0, LABELCOLOUR)

        #  Display Left Ticks
        win.blit(label, (TICKLEN + LABELPAD, (i+1) * TICKSPACE - label.get_height() / 2.0 ))

        #  Display Top Ticks
        win.blit(label, ((i+1) * TICKSPACE - label.get_width() / 2.0, TICKLEN + LABELPAD))


def time_display(win, time, WINSIZE, TICKLEN, BACKCOLOUR):
    """
    Create Time Box in lower right hand corner.

    Creates a box to display the current time in the simulation.
    The time is specified to 5 decimal places.
    Parameters
    ----------
    win : pygame.display
        The window to draw the axes in.
    WINSIZE : int
        The height and width of the window to be created.
    TICKLEN : int
        The length of with tick mark in pixels.
    
    Returns
    -------
    NONE
    """

    TIMEBOX_WIDTH = 110  
    TIMEBOX_HEIGHT = 20
    TEXTCOLOUR = (0,0,0)   # Black
    RECT_PAD = 20  # Padding around the ticks


    #  rect(x,y, width, height, fill=True)
    pyg.draw.rect(win, BACKCOLOUR, (WINSIZE - TIMEBOX_WIDTH - TICKLEN - RECT_PAD,
                                    WINSIZE - TIMEBOX_HEIGHT - TICKLEN - RECT_PAD,
                                    TIMEBOX_WIDTH,
                                    TIMEBOX_HEIGHT), 0)

    timer_font = pyg.font.SysFont("monospace", 15)
    timer = timer_font.render(str("{0:.5f}".format(time)) + " yr", 2, TEXTCOLOUR)
    win.blit(timer, (WINSIZE - TIMEBOX_WIDTH - TICKLEN - RECT_PAD,
                     WINSIZE - TICKLEN - RECT_PAD - timer.get_height()) )


def initialise_display(WINSIZE, BOXSIZE, TICKNUM, TICKLEN, time=0):
    """
    Initialise the window that everything will be displayed in.

    Creates a screen using pygame. Initialises the BACKCOLOUR and 
    draws axes along each edge and displays the current time in the 
    bottom right hand corner.
    Parameters
    ----------
    WINSIZE : int
        The height and width of the window to be created.
    BOXSIZE : int
        The hight and width of the window in physical units.
    TICKNUM : int
        The number of tick marks along each edge of the window.
    TICKLEN : int
        The length of with tick mark in pixels.
    time : float
        The initial time to print in the bottom right hand corner.
    Returns
    -------
    win : pygame.display
        The window that everything will be displayed in.
    BACKCOLOUR : tuple
        The colour of the background
    """

    BACKCOLOUR = (255, 255, 255)  # White

    pyg.init()
    win = pyg.display.set_mode((WINSIZE,WINSIZE))
    win.fill(BACKCOLOUR)
    pyg.display.set_caption("3D n-Body Gravitational Simulator")

    draw_axes(win, WINSIZE, BOXSIZE, TICKNUM, TICKLEN)
    time_display(win, time, WINSIZE, TICKLEN, BACKCOLOUR)
    pyg.display.flip() 

    return win, BACKCOLOUR


def read_args():
    """
    Read the arguments specified by the user.

    Utilises argparse to read the arguments that the 
    user specified. These arguments are used to change the 
    display. The arguments that the user can specify are:

    --winsize, --boxsize, --timestep, --ticknum, --ticklen

    Parameters
    ----------
    NONE

    Returns
    -------
    WINSIZE : int
        The height and width of the window to be created.
    BOXSIZE : int
        The hight and width of the window in physical units.
    SCALE : float
        The ratio between the WINSIZE and the BOXSIZE. 
    TICKNUM : int
        The number of tick marks along each edge of the window.
    TICKLEN : int
        The length of with tick mark in pixels.
    """

    # Add the arguments for the user
    parser = argparse.ArgumentParser()
    parser.add_argument("--boxsize", help="The height/width of the physical box. \
                        Unit: solar radii, Default 1000.", type=int)
    parser.add_argument("--timestep", help="The length of the time step \
                         between calculations. \
                         Unit: seconds, Default: 8640 (0.1 days).", type=float)
    parser.add_argument("--winsize", help="The height and width of the \
                         window in pixels. Default: 1000", type=int)
    parser.add_argument("--ticknum", help="The number of ticks on each side \
                         of the window. Default: 10", type=int)
    parser.add_argument("--ticklen", help="The length of each tick on the \
                         side of the window in pixels. Default: 20", type=int)

    args = parser.parse_args()

    # Setup defaults and read arguments
    if args.winsize:
        WINSIZE = args.winsize
    else:
        WINSIZE = 1000

    if args.boxsize:
        BOXSIZE = args.boxsize * C.XRSUN
        SCALE = WINSIZE / args.boxsize
    else:
        BOXSIZE = 1000 * C.XRSUN
        SCALE = WINSIZE / 1000

    if args.timestep:
        TIMESTEP = args.timestep
    else:
        TIMESTEP = C.XDAY / 100  # 1 day in seconds

    if args.ticknum:
        TICKNUM = args.ticknum
    else:
        TICKNUM = 10

    if args.ticklen:
        TICKLEN = args.ticklen
    else:
        TICKLEN = 20   

    return WINSIZE, BOXSIZE, SCALE, TIMESTEP, TICKNUM, TICKLEN

def main():

    WINSIZE, BOXSIZE, SCALE, TIMESTEP, TICKNUM, TICKLEN = read_args()

    win, BACKCOLOUR = initialise_display(WINSIZE, BOXSIZE, TICKNUM, TICKLEN)

    print(BOXSIZE/(2*C.XRSUN))

    Plist = [Particle(win, [BOXSIZE/(2*C.XRSUN) + 0.0000, BOXSIZE/(2*C.XRSUN), 0], [0,   0,    0], 1, 10, 1, (255,255,0)), # Sun
             Particle(win, [BOXSIZE/(2*C.XRSUN) + 66.120, BOXSIZE/(2*C.XRSUN), 0], [0, -58.98, 0], 0.000000165, 4, 1, (105,105,105)), # Mercury
             Particle(win, [BOXSIZE/(2*C.XRSUN) + 154.50, BOXSIZE/(2*C.XRSUN), 0], [0, -35.26, 0], 0.000002447, 4, 1, (210,105,30)), # Venus
             Particle(win, [BOXSIZE/(2*C.XRSUN) + 211.40, BOXSIZE/(2*C.XRSUN), 0], [0, -30.29, 0], 0.000003003, 4, 0, (0,255,0)), # Earth
             Particle(win, [BOXSIZE/(2*C.XRSUN) + 297.00, BOXSIZE/(2*C.XRSUN), 0], [0, -26.50, 0], 0.000000321, 4, 1, (255,0,0))]#, # Mars
             #Particle(win, [BOXSIZE/(2*C.XRSUN) + 1064.4, BOXSIZE/(2*C.XRSUN), 0], [0, -13.72, 0], 0.0009543, 4, 0, (160,82,45)),  # Jupiter
             #Particle(win, [BOXSIZE/(2*C.XRSUN) + 1944.2, BOXSIZE/(2*C.XRSUN), 0], [0, -10.18, 0], 0.0002857, 4, 0, (102,102,0)),  # Saturn
             #Particle(win, [BOXSIZE/(2*C.XRSUN) + 3940.3, BOXSIZE/(2*C.XRSUN), 0], [0, -7.110, 0], 0.00004364, 4, 0, (102,255,170)),  # Uranus
             #Particle(win, [BOXSIZE/(2*C.XRSUN) + 6388.5, BOXSIZE/(2*C.XRSUN), 0], [0, -5.500, 0], 0.00005149, 4, 0, (0,0,255))]  # Neptune
             #]

    time = 0
    running = True
    while running:
        pyg.display.flip()  # Refresh Display
        time += TIMESTEP / C.XYR

        update_particles(win, Plist, TIMESTEP, SCALE)
        time_display(win, time, WINSIZE, TICKLEN, BACKCOLOUR)
        draw_axes(win, WINSIZE, BOXSIZE, TICKNUM, TICKLEN)

        # Check of the close button is pushed and Quit if so.
        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                running = False

if __name__ == '__main__':
    main()
