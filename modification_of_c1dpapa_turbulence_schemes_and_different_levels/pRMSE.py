# import the necessary modules:
import numpy as np
import math as m
from netCDF4 import Dataset as netcdffile
import matplotlib.pyplot as plt
import pylab

# this function plots the RMSE values for temp or salinity
# how to use:
# pRMSE(calculated_data, observed_data, font_size, line_thickness, horizontal_line, title, horizontal_line_thickness, x_limits, y_limits)


def pRMSE(cal_data,obs_data,font = 35,thickness = 2.5,horz = 0,title = "",horz_value = None,ylim=None,xlim=None):
    # make the time step up to 350, no complications wanted at 365 if there are missing values or NANs
    time_step = []
    for i in range(0,350): time_step.append(i) # sequential days
    time_step = np.array(time_step)

    #plot the data
    rmse = (cal_data-obs_data)**2 # first compute the difference of the values in the matrix


    # now for some data processing: this is for the temperature correction needed, none needed for salinity
    # # from the above data, the forth value for each time step seems to be blowing up, I am omitting this line
    # # delete the entries:
    if rmse[0,3] > 1e5 or rmse[0,3] < 1e-5:
        trmse = []
        for t in range(rmse.shape[0]): # run through the time steps
            toappend = np.delete(rmse[t,:],3,axis=0) # delete and then:
            trmse.append(toappend) # append the result on
        rmse = np.array(trmse) # change it to np array again.
    # data processing done

    rmse = np.mean(rmse,axis=1) # Now get the means of the columns
    rmse = rmse**0.5 # lastly find the sqrt of the resulting matrix
    # ready for plotting:
    makeplot = plt.figure() # create the figure
    # set the number of time steps to 350 for all, will avoid complications with the data processing above.
    plt.plot(time_step,rmse[0:350],'r-',label='computed',linewidth = thickness)
    plt.title(title,fontsize = font) # label titles
    plt.xlabel("Time (days)",fontsize = font)
    plt.ylabel("RMSE",fontsize = font)
    plt.tick_params(labelsize=font) # axes size
    pylab.xlim(xlim) # set the x axis limits
    pylab.ylim(ylim) # set the y axis limits
    if horz: # makes the horizontal line to see convergence
        plt.axhline(y=horz_value,linewidth = thickness) # to draw the horizontal line
    makeplot.show()
    # return 0
