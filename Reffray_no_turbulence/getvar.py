 # import the necessary modules:
import numpy as np
import math as m
from netCDF4 import Dataset as netcdffile
import matplotlib.pyplot as plt
import pylab

# this function gets the variable you need from a netcdf file and prints the dimensions of the variables if you need it
#how to use:
# variable = getvar("netcdf file name with full path", "name of variable in netcdf file", "print the dimension, can be 0 or 1")
def getvar(nc_file,variable,show=0):
    gen_var = nc_file.variables[variable][:]
    if show:
        print(str(variable)+": "+str(gen_var.shape))
    return np.array(gen_var)