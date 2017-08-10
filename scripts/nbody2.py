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


def draw_axes(win, win_size, box_size, tick_num, tick_len):
    """
    Draws the grid lines and labels around the outside of the box.
    Parameters
    ----------
    win_size : int
        The height and width of the window to be created.
    box_size : int
        The hight and width of the window in physical units.
    tick_num : int
        The number of tick marks along each edge of the window.
    tick_len : int
        The length of with tick mark in pixels.
    
    Returns
    -------
    NONE   
    """

    tick_jump = box_size / tick_num  # Value difference between axis labels
    tick_space = win_size / tick_num  # Physical distance bwtween axis labels
    tick_colour = 0x000000  # Black

    # Draw the tick marks
    for i in range(tick_num):

        #  Left Ticks
        pyg.draw.line(win, tick_colour, (0, i * tick_space),
                          (tick_len, i * tick_space), 2)
        #  Right Ticks
        pyg.draw.line(win, tick_colour, (win_size - tick_len, i * tick_space),
                          (win_size, i * tick_space), 2)
        #  Top Ticks
        pyg.draw.line(win, tick_colour, (i * tick_space, 0),
                          (i * tick_space, tick_len), 2)
        # Bottom Ticks
        pyg.draw.line(win, tick_colour, (i * tick_space, win_size - tick_len),
                          (i * tick_space, win_size), 2)      

    #  Font Type    
    tick_font = pyg.font.SysFont("monospace", 15)

    for i in range(tick_num -1):
        #  Create Labels
        label = tick_font.render(str("{0:.2f}".format((i + 1) * tick_jump / C.XRSUN)) + "Rsun", 2, (0,0,0))

        #  Display Left Ticks
        win.blit(label, (tick_len + 5, (i+1) * tick_space - label.get_height() / 2.0 ))

        #  Display Top Ticks
        win.blit(label, ((i+1) * tick_space - label.get_width() / 2.0, tick_len + 5))


def time_display(win, time, win_size, tick_len, background):
    """
    Create Time Box in lower right hand corner.
    Creates a box to display the current time in the simulation.
    The time is specified to 5 decimal places.
    Parameters
    ----------
    win_size : int
        The height and width of the window to be created.
    tick_len : int
        The length of with tick mark in pixels.
    
    Returns
    -------
    NONE
    """

    time_box_width = 90  
    time_box_height = 20
    rect_col = background #rect_col = 0xFF0000  # White
    text_col = (0,0,0)   # Black
    rect_pad = 20  # Padding around the ticks


    #  rect(x,y, width, height, fill=True)
    pyg.draw.rect(win, rect_col,(win_size - time_box_width - tick_len - rect_pad,
                                 win_size - time_box_height - tick_len - rect_pad,
                                    time_box_width,
                                    time_box_height), 0)

    timer_font = pyg.font.SysFont("monospace", 15)
    timer = timer_font.render(str("{0:.5f}".format(time)) + " yr", 2, text_col)
    win.blit(timer, (win_size - time_box_width - tick_len - rect_pad,
                     win_size - tick_len - rect_pad - timer.get_height()) )


def initialise_display(win_size, box_size, tick_num, tick_len, time=0):
    """
    Initialise the window that everything will be displayed in.
    Creates a screen using pygame. Initialises the background and 
    draws axes along each edge and displays the current time in the 
    bottom right hand corner.
    Parameters
    ----------
    win_size : int
        The height and width of the window to be created.
    box_size : int
        The hight and width of the window in physical units.
    tick_num : int
        The number of tick marks along each edge of the window.
    tick_len : int
        The length of with tick mark in pixels.
    time : float
        The initial time to print in the bottom right hand corner.
    Returns
    -------
    win : pygame.display
        The window that everything will be displayed in.
    """

    background = (255, 255, 255)  # White

    pyg.init()
    win = pyg.display.set_mode((win_size,win_size))
    win.fill(background)
    pyg.display.set_caption("N-Body 3D gravitational Simulator")

    draw_axes(win, win_size, box_size, tick_num, tick_len)
    time_display(win, time, win_size, tick_len, background)
    pyg.display.flip() 

    return win, background


def main():

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
        win_size = args.winsize
    else:
        win_size = 1000

    if args.boxsize:
        box_size = args.boxsize * C.XRSUN
        scale = win_size / box_size
    else:
        box_size = 1000 * C.XRSUN
        scale = win_size / box_size

    if args.timestep:
        time_step = args.timestep
    else:
        time_step = C.XDAY / 10  # 0.1 day in seconds

    if args.ticknum:
        tick_num = args.ticknum
    else:
        tick_num = 10

    if args.ticklen:
        tick_len = args.ticklen
    else:
        tick_len = 20



    win, background = initialise_display(win_size, box_size, tick_num, tick_len)

    Plist = [Particle(win, [500, 200, 300], [0, 0, 0], 10, 10, 0)]

    running = True
    while running:
        pyg.display.flip()  # Refresh Display




        # Check of the close button is pushed and Quit if so.
        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                running = False


if __name__ == '__main__':
    main()
