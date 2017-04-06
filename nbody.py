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

################################################################################

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
                          text=str((i + 1) * tick_jump) + " Rsun", anchor="w")
        # Top Tick Labels
        frame.create_text((i + 1) * tick_spacing, tick_length + 5, 
                          text=str((i + 1) * tick_jump) + " Rsun", anchor="c")

################################################################################
if __name__ == "__main__":
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
        box_size = args.boxsize
        scale = window_size/box_size
    else:
        box_size = 1000
        scale = window_size/box_size

    if args.timestep:
        time_step = args.timestep
    else:
        time_step = 0.0027 # 1 day

    if args.ticknum:
        tick_num = args.ticknum
    else:
        tick_num = 10 

    if args.ticklength:
        tick_length = args.ticklength
    else:
        tick_length = 20 


    window = tk.Tk()
    window.title("N-Body Simulation")
    frame = tk.Canvas(window, height=str(window_size), width=str(window_size))
    frame.pack()


    draw_grid(frame, window_size, box_size, tick_num, tick_length)


    tk.mainloop()