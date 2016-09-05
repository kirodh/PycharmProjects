# import the necessary modules:
import numpy as np
import math as m
from netCDF4 import Dataset as netcdffile
import matplotlib.pyplot as plt
import pylab

# this function plots the graphs
# how to use:
# template = pgraph(data1_x_time, data2_y_depth, data3_z_salinity_etc, xlabel, yalabel, font_size, invert_y_axis,
#                                        grayscale_plot, include_colourbar, x_limits, y_limits, colourbar_limits, title)
#example = (data1, data2, data3, "x axis", "y axis", 45, 1, 0, 1, None, [0,500], None, "the title")
def pgraph(data1,data2,data3,xlab,ylab,font = 35,invert = 0,grey = 0,colourbar = 0,xlim=None,ylim=None,cblim=None,title = ""):
    #plot the data
    makeplot = plt.figure() # create the figure
    plt.pcolormesh(data1,data2,data3.T) # plot data # need to transpose the matrix data! then all is good
    plt.title(title,fontsize = font) # label titles
    plt.xlabel(xlab,fontsize = font)
    plt.ylabel(ylab,fontsize = font)
    plt.tick_params(labelsize=font) # axes size
    pylab.xlim(xlim) # set the x axis limits
    pylab.ylim(ylim) # set the y axis limits
    if invert:
        plt.gca().invert_yaxis() # inverts the y axis
    if grey:
        plt.set_cmap('gray') # set the plot to grayscale
    if colourbar:
        cb = plt.colorbar()
        cb.ax.tick_params(labelsize = font)
        plt.clim(cblim) # to set the colour bar limits
    makeplot.show()
    # return 0