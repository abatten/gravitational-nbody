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

    """
    def __init__(self, win, init_pos, init_vel, mass=1, rad=1, dex=0, col=(0,0,0)):
        self.pos = init_pos
        self.vel = init_vel
        self.mas = mass * C.XMSUN  # Convert to kilograms
        self.rad = rad #* C.XRSUN  #  Convert to meters
        self.dex = dex
        self.col = col
        self.display = True

        self.draw(win)

    def __repr__(self):
        return ('Position:{x} Velocity:{v} Mass:{m} Radius:{r} Index:{d} Colour:{c}'.format(
                x=self.pos, v=self.vel, m=self.mas, r=self.rad, d=self.dex, c=self.col))

    def draw(self, win):
        """
        Draws the particle in its initial position
        """
        pyg.draw.circle(win, self.col, (self.pos[0],self.pos[1]), self.rad , 0)

        return()

def dist_to(particle1, particle2):
    """
    Calculates the distance between two particles.

    Parameters
    ----------
    particle1: particle
    particle2: particle
    
    Returns
    -------
    dist : float
        The distance between the two particles   
    """

    x1 = particle1.pos[0]
    y1 = particle1.pos[1]
    z1 = particle1.pos[2]

    x2 = particle2.pos[0]
    y2 = particle2.pos[1]
    z2 = particle2.pos[2]

    dist = np.sqrt((x1 - x2)**2.0 + (y1 - y2)**2.0 + (z1 - z2)**2.0)

    return dist

def find_acceleration(Particle_list):
    """
    Finds the acceleration on a particle due to all other particles.

    Parameters
    ----------
    particle1: particle
    particle2: particle
    
    Returns
    -------
    accel : float
        The acceleration on the particle   
    """   


def draw_axes(win, WINSIZE, BOXSIZE, TICKNUM, TICKLEN):
    """
    Draws the grid lines and labels around the outside of the box.

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
    
    Returns
    -------
    NONE   
    """

    TICKJUMP = BOXSIZE / TICKNUM  # Value difference between axis labels
    TICKSPACE = WINSIZE / TICKNUM  # Physical distance bwtween axis labels
    TICKCOLOUR = 0x000000  # Black

    # Draw the tick marks
    for i in range(TICKNUM):

        #  Left Ticks
        pyg.draw.line(win, TICKCOLOUR, (0, i * TICKSPACE),
                          (TICKLEN, i * TICKSPACE), 2)
        #  Right Ticks
        pyg.draw.line(win, TICKCOLOUR, (WINSIZE - TICKLEN, i * TICKSPACE),
                          (WINSIZE, i * TICKSPACE), 2)
        #  Top Ticks
        pyg.draw.line(win, TICKCOLOUR, (i * TICKSPACE, 0),
                          (i * TICKSPACE, TICKLEN), 2)
        # Bottom Ticks
        pyg.draw.line(win, TICKCOLOUR, (i * TICKSPACE, WINSIZE - TICKLEN),
                          (i * TICKSPACE, WINSIZE), 2)      

    #  Font Type    
    tick_font = pyg.font.SysFont("monospace", 13)

    for i in range(TICKNUM -1):
        #  Create Labels
        label = tick_font.render(str("{0:.1f}".format((i + 1) * TICKJUMP / C.XRSUN)) + "Rsun", 2, (0,0,0))

        #  Display Left Ticks
        win.blit(label, (TICKLEN + 5, (i+1) * TICKSPACE - label.get_height() / 2.0 ))

        #  Display Top Ticks
        win.blit(label, ((i+1) * TICKSPACE - label.get_width() / 2.0, TICKLEN + 5))


def time_display(win, time, WINSIZE, TICKLEN, BACKCOLOUR):
    """
    Create Time Box in lower right hand corner.

    Creates a box to display the current time in the simulation.
    The time is specified to 5 decimal places.
    Parameters
    ----------
    WINSIZE : int
        The height and width of the window to be created.
    TICKLEN : int
        The length of with tick mark in pixels.
    
    Returns
    -------
    NONE
    """

    TIMEBOX_WIDTH = 90  
    TIMEBOX_HEIGHT = 20
    text_col = (0,0,0)   # Black
    RECT_PAD = 20  # Padding around the ticks


    #  rect(x,y, width, height, fill=True)
    pyg.draw.rect(win, BACKCOLOUR, (WINSIZE - TIMEBOX_WIDTH - TICKLEN - RECT_PAD,
                                    WINSIZE - TIMEBOX_HEIGHT - TICKLEN - RECT_PAD,
                                    TIMEBOX_WIDTH,
                                    TIMEBOX_HEIGHT), 0)

    timer_font = pyg.font.SysFont("monospace", 15)
    timer = timer_font.render(str("{0:.5f}".format(time)) + " yr", 2, text_col)
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
    parser.add_argument("--boxsize", help="The dimentions of the box in solar \
                         radii. Default: 1000", type=int)
    parser.add_argument("--timestep", help="The length of the time step \
                         between calculations. Default: 1 day", type=float)
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
        SCALE = WINSIZE / BOXSIZE
    else:
        BOXSIZE = 1000 * C.XRSUN
        SCALE = WINSIZE / BOXSIZE

    if args.timestep:
        TIMESTEP = args.timestep
    else:
        TIMESTEP = C.XDAY / 10  # 0.1 day in seconds

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

    Plist = [Particle(win, [500, 200, 300], [0, 0, 0], 10, 4, 0, (255,0,0)),
             Particle(win, [300, 100, 400], [0, 0, 0], 10, 4, 0, (0,255,0))]

    print(dist_to(Plist[0], Plist[1]))
    running = True
    while running:
        pyg.display.flip()  # Refresh Display


        # Check of the close button is pushed and Quit if so.
        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                running = False


if __name__ == '__main__':
    main()
