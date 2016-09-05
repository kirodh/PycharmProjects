# this file processes te Temperature, seeing that the 4th value in the original data is a nan


from netCDF4 import Dataset as netcdffile
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.basemap import Basemap
import pylab


# how to use:
#  [temp, Sal] = processTemp(temp_data, sal_data, fixed_time_step_used_in_all_calculations)


def processTempandSal(Tdata,Sdata,time):
    # take out the forth value and replace it with the average between the values next to it on left and right
    # plt.plot(Tdata[0:time,:,0,0])
    for i in range(Tdata.shape[0]):
        Tdata[i,3] = (Tdata[i,2]+Tdata[i,4])/2.0
    # now reshape the values so that they are not 4 dimensional but 2 dimensional
    # this also sets the time to be a fixed time step
    Tdata = Tdata[0:time,:,0,0]
    Sdata = Sdata[0:time,:,0,0]
    # plt.plot(Tdata)
    return [Tdata, Sdata]


