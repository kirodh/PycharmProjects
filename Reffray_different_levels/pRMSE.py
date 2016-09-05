# import the necessary modules:
import numpy as np
import math as m
from netCDF4 import Dataset as netcdffile
import matplotlib.pyplot as plt
import pylab

# this function plots the RMSE values for temp or salinity
# how to use:
# pRMSE(calculated_data, observed_data, font_size, line_thickness, horizontal_line, title, horizontal_line_thickness, x_limits, y_limits)


def pRMSE(cal_data,obs_data,font = 35,thickness = 2.5,horz = 0,title = "",horz_value = None,ylim=None,xlim=None,ret_rmse=0,plotit=1):
    # make the time step, use the number of rows, will give the time step ( this is used for plotting the data)
    time_step = []
    for i in range(len(cal_data[:,0])): time_step.append(i) # sequential days
    time_step = np.array(time_step) # convert to np array for plotting
    # print(time_step) # testing

    #break down the calculation( take 70% of the corresponding depth values to reduce the error from the addition of the last data values to the calculated data)
    # The index [:,0:int(0.7*len(cal_data[0,:]))] reads as taking all the time steps, and type casting the result into an int or a decimal index would result
    #   from the calculation throwing an error, then 70% (i.e. 0.7) of the maximum length of the depths (I took the first time step, could have used any) and use these only
    rmse = np.subtract(cal_data[:,0:int(0.7*len(cal_data[0,:]))],obs_data[:,0:int(0.7*len(cal_data[0,:]))])**2 # first compute the difference of the values in the matrix
    # print(rmse)
    rmse = np.mean(rmse,axis=1) # Now get the means of the columns
    rmse = rmse**0.5 # lastly find the sqrt of the resulting matrix
    # print(time_step.shape)
    # print(rmse.shape)
    # print(rmse)
    # ready for plotting:
    if plotit:
        makeplot = plt.figure() # create the figure
        plt.plot(time_step[0:360],rmse[0:360],'r-',label='computed',linewidth = thickness)
        plt.title(title,fontsize = font) # label titles
        plt.xlabel("Time (days)",fontsize = font)
        plt.ylabel("RMSE",fontsize = font)
        plt.tick_params(labelsize=font) # axes size
        pylab.xlim(xlim) # set the x axis limits
        pylab.ylim(ylim) # set the y axis limits
        if horz: # makes the horizontal line to see convergence
            plt.axhline(y=horz_value,linewidth = thickness) # to draw the horizontal line
        makeplot.show()

    if ret_rmse: return rmse[0:360]
