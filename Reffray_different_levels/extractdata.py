# import the necessary modules:
import numpy as np
import math as m
from netCDF4 import Dataset as netcdffile
import matplotlib.pyplot as plt
import pylab
from scipy.interpolate import interp1d

# this function is used only for the original data
# this function fits a cubic spline to the temp and sal data and then extracts the sal and temp values according to certain depths
# how to use:
#       resized_data = extractdata(New_depth_values, Temp_orig_depth, Temp_orig_data, Sal_orig_ depth, Sal_orig_data, print_dimension, time_in_days)

def extractdata(Ndepth,Tdepth,Tdata,Sdepth,Sdata,dim=0,time=364):
    # having troubles with fitting data because of bounds, calculated data bounds are much larger than the observed data bounds
    # to fix problem introduce outer bounds with the same values as the end values of the data, the bounds will be 0 at the top


    # resize the depths:
    Tdepth = np.insert(Tdepth,0,0) # insert the first values (0) at top of the array
    Sdepth = np.insert(Sdepth,0,0)


    # rersize the temp/sal data
    # print(Tdata.shape) # testing
    # for the top
    Tdata = np.insert(Tdata,0,Tdata[:,0],axis=1) # insert the first row as a copy of the first values of the original array, need a axis =1 from the layout of the array,
    # the index [:,0] means all 364 values and the 0 is the first value of the temp/sal values
    Sdata = np.insert(Sdata,0,Sdata[:,0],axis=1)



    # run through timesteps (up to time (should be 364)) and fit the data, then use Ndepths to get new values and then append it on to a large array for both the sal and temp.
    usefortemp = []
    useforsal =[]
    for t in range(0,time):
        fitTemp = interp1d(Tdepth,Tdata[t,:],kind="cubic") # fit the data using the orig depths and orig sal/temp,
        fitSal = interp1d(Sdepth,Sdata[t,:],kind="cubic")
        # print(Tdepth[len(Tdepth)-1]) # testing for bounds
        # print(Ndepth[len(Ndepth)-1])

        newtemp = []
        newsal = []

        for i in Ndepth:
            if i <=300:
                newtemp.append(fitTemp(i)) # append the fitted value if it is less than 300
                # newsal.append(fitSal(i)) # append the fitted value if it is less than 300
            else:
                newtemp.append(Tdata[t,len(Tdata[0,:])-1]) # otherwise just use the last value, avoid complication with the fitting functions
                # newsal.append(Sdata[t,len(Sdata[0,:])-1]) # otherwise just use the last value, avoid complication with the fitting functions
            if i <=200:
                # newtemp.append(fitTemp(i)) # append the fitted value if it is less than 300
                newsal.append(fitSal(i)) # append the fitted value if it is less than 300
            else:
                # newtemp.append(Tdata[t,len(Tdata[0,:])-1]) # otherwise just use the last value, avoid complication with the fitting functions
                newsal.append(Sdata[t,len(Sdata[0,:])-1]) # otherwise just use the last value, avoid complication with the fitting functions



        # append the data on to a big array
        usefortemp.append(newtemp)
        useforsal.append(newsal)
    # plt.plot(Ndepth,newsal,'ro-') # testing
    # plt.plot(Sdepth,Sdata[time-1,:])
    # reconvert to numpy array and return for use
    NEWTdata = np.array(usefortemp)
    NEWSdata = np.array(useforsal)
    if dim: # print the dimensions
        print("TData dim: "+str(NEWTdata.shape))
        print("SData dim: "+str(NEWSdata.shape))
    return [Ndepth, NEWTdata, NEWSdata]