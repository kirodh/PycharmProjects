# import the necessary modules:
import numpy as np
import math as m
from netCDF4 import Dataset as netcdffile
import matplotlib.pyplot as plt
import pylab

# this function plots the number of levels and spacing between levels values for temp or salinity
# how to use:
# pvert_grid(data, plot_graph_of_spacing,font_size, line_thickness, horizontal_line, horizontal_line_thickness, y_limits, x_limits)


def pvert_grid(data,spacing=0,font = 35,thickness = 2.5,horz = 0,horz_value = None,ylim=None,xlim=None):
    # make the time step up to 350, no complications wanted at 365 if there are missing values or NANs
    num_levels = []
    for i in range(0,len(data)): num_levels.append(i) # sequential levels
    num_levels = np.array(num_levels)

    #plot the data
    makeplot = plt.figure() # create the figure
    plt.plot(num_levels,data,'r-',label='computed',linewidth = thickness) # to plot the depth against the number of levels, easy to see how many levels per depth
    # plt.title(title,fontsize = font) # label titles
    plt.xlabel("number of levels",fontsize = font)
    plt.ylabel("Depth (m)",fontsize = font)
    plt.tick_params(labelsize=font) # axes size
    pylab.xlim(xlim) # set the x axis limits
    pylab.ylim(ylim) # set the y axis limits
    if horz: # makes the horizontal line to see convergence
        plt.axhline(y=horz_value,linewidth = thickness) # to draw the horizontal line
    if spacing:
        #plot the data
        makeplot1 = plt.figure() # create the figure
        # now make an array that will shift all values one forewards and then subtract the data and will get the spacings, delete the first entry and also delete the last entry and then subtract the two arrays
        plt.plot(num_levels[0:len(data)-1],np.subtract(np.delete(data,0),np.delete(data,len(data)-1)),'r-',label='computed',linewidth = thickness)
        # plt.title(title,fontsize = font) # label titles
        plt.xlabel("number of levels",fontsize = font)
        plt.ylabel("Spacing between levels (m)",fontsize = font)
        plt.tick_params(labelsize=font) # axes size
        pylab.xlim(xlim) # set the x axis limits
        pylab.ylim(ylim) # set the y axis limits
        makeplot1.show()
    makeplot.show()
    # return 0
