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


def draw_axes(win, window_size, box_size, tick_num, tick_length):
    """
    Draws the grid lines and labels around the outside of the box.
    """

    tick_jump = box_size / tick_num  # Value difference between axis labels
    tick_space = window_size / tick_num  # Physical distance bwtween axis labels
    tick_colour = 0x000000  # Black

    # Draw the tick marks
    for i in range(tick_num):

        #  Left Ticks
        pyg.draw.line(win, tick_colour, (0, i * tick_space),
                          (tick_length, i * tick_space), 2)
        #  Right Ticks
        pyg.draw.line(win, tick_colour, (window_size - tick_length, i * tick_space),
                          (window_size, i * tick_space), 2)
        #  Top Ticks
        pyg.draw.line(win, tick_colour, (i * tick_space, 0),
                          (i * tick_space, tick_length), 2)
        # Bottom Ticks
        pyg.draw.line(win, tick_colour, (i * tick_space, window_size - tick_length),
                          (i * tick_space, window_size), 2)      

    #  Font Type    
    tick_font = pyg.font.SysFont("monospace", 15)

    for i in range(tick_num -1):
        #  Create Labels
        label = tick_font.render(str("{0:.2f}".format((i + 1) * tick_jump / C.XRSUN)) + "Rsun", 2, (0,0,0))

        #  Display Left Ticks
        win.blit(label, (tick_length + 5, (i+1) * tick_space - label.get_height() / 2.0 ))

        #  Display Top Ticks
        win.blit(label, ((i+1) * tick_space - label.get_width() / 2.0, tick_length + 5))


def time_display(win, time, window_size, tick_length):
    """
    Create Timer Box in lower right hand corner
    """

    time_box_width = 120
    time_box_height = 20
    rect_colour = 0xFFFFFF
    text_colour = (0,0,0)

    #  rect(x,y, width, height, fill=True)
    pyg.draw.rect(win, rect_colour,(window_size - time_box_width - tick_length - 30,
                                    window_size - time_box_height - tick_length - 30,
                                    time_box_width,
                                    time_box_height), 0)

    timer_font = pyg.font.SysFont("monospace", 15)
    timer = timer_font.render(str("{0:.5f}".format(time)) + " yr", 2, text_colour)
    win.blit(timer, (window_size - time_box_width - tick_length - 20,
                     window_size - tick_length - 40 - timer.get_height() / 2.0) )


def initialise_display(window_size, box_size, tick_num, tick_length, time):
    """
    Initialise the display by creating window and draws the axes.
    """

    pyg.init()
    win = pyg.display.set_mode((window_size,window_size))
    win.fill((255,255,255))
    pyg.display.set_caption("N-Body 3D gravitational Simulator")

    draw_axes(win, window_size, box_size, tick_num, tick_length)
    time_display(win, time, window_size, tick_length)
    pyg.display.flip() 

    return win


def main():

    window_size = 1000
    box_size = 1000 * C.XRSUN
    tick_num = 10
    tick_length = 20
    time = 0

    win = initialise_display(window_size, box_size, tick_num, tick_length, time)

    Plist = [Particle(win, [500, 200, 300], [0, 0, 0], 10, 10, 0)]

    running = True
    while running:
        time += 1
        pyg.display.flip()  # Refresh Display























        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                running = False


if __name__ == '__main__':
    main()