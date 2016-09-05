# import the necessary modules:
import numpy as np
import math as m
from netCDF4 import Dataset as netcdffile
import matplotlib.pyplot as plt
import pylab

# this function pulls out the data for those depths corrosponding to indexes in an array and returns the data
# how to use:
#       resized_data = extractdata(raw_data, array_of_depth_indexes, time_in_days, shape_of_data_0_or_1)

def extractdata(data,indexarray,dim=0,time=364):
    # this is for the biases of salinity and temperature
    # this involves subtracting the observed and computed data
    # the computed data must first be resized to fit the observed data
    # then everything must be plotted using pgraph()


    # resize the computed data done automatically i.e. only one column of the 3x3 horz grid is used for the vertical column
    # run through timesteps (up to 364) and then pull out the indexed values, convert to list and append on and reconvert to numpy array.
    usefortemp = []
    for t in range(0,time):
        # check if the dimensions are right(if some thing goes wrong here)
        usemetemp = np.take(data[t,:],indexarray)
        # convert to list (makes it easier to append)
        usemetemp = usemetemp.tolist()
        # append the data on to a big array
        usefortemp.append(usemetemp)
        # if t == 363: print(usemetemp) # testing last entry
    # reconvert to numpy array with the same name
    data = np.array(usefortemp)
    if dim: print("Data dim: "+str(data.shape))
    return data