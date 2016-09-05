# this code must fit a curve to the initial condition

from opennc import opennc
from getvar import getvar
from zgrid import zgrid
from scipy.interpolate import interp1d
from pinitgraph import pinitgraph
from netCDF4 import Dataset as netcdffile
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.basemap import Basemap
import pylab
from scipy.optimize import curve_fit

infile4 = 'nc_files/init_PAPASTATION_m06d15.nc'
fh_init = opennc(infile4,1)

init_dept = getvar(fh_init,"deptht",1); # C
init_temp = getvar(fh_init,"votemper",1) ; init_temp = init_temp[0,:,1,1] # C
init_sal = getvar(fh_init,"vosaline",1);init_sal = init_sal[0,:,1,1] # C
longi = fh_init.variables["longitude"][:]



# use the spline interpolation
# gert suggested it and it is found online at:
# http://docs.scipy.org/doc/scipy/reference/tutorial/interpolate.html
# works well for salinity and temperature


# set out the data
xdata = init_dept
ydata_S = init_sal
ydata_T = init_temp

fit_temp = interp1d(xdata,ydata_T,kind='cubic')
fit_sal = interp1d(xdata,ydata_S,kind='cubic')


########
# this part gets the spacings using the translated fortran code from NEMO and also generated the depths from the cumalative sum of these spacings

# get the spacings
[space_t,other1,space_w,other2] = zgrid(51,np.nan,np.nan,np.nan,30.0,6.0,1.0,4200,0,np.nan,np.nan,np.nan)

# make the depths from the cumalative sum of the spacings
cumsum = (space_t[0]).tolist()[0] # need to convert the data to a list and take the 0th value, i.e. remove the list structure
xnew=[]  # this is the new depths # create the array to store the cumalative values in
xnew.append(cumsum) # put in the first value
for i in range(1,len(space_t)): # loop through the 2nd value and carry on
    cumsum += (space_t[i]).tolist()[0]  # convert to list and then remove the list structure otherwise you append on a list, uncool
    xnew.append(cumsum) # append on the new depth
## print the control values if necessary
# print(xnew)
# print(len(xnew))


# plot the graphs to see if they are good or not
# for the temperature
makeplot = plt.figure() # make the plot
plt.plot(xdata,ydata_T,'ro-') # plot the orig data
plt.plot(xnew,fit_temp(xnew),'b*-') # plot the fitted data
plt.title("temperature")
makeplot.show()

# for the salinity
makeplot = plt.figure() # make the plot
plt.plot(xdata,ydata_S,'ro-') # plot the orig data
plt.plot(xnew,fit_sal(xnew),'b*-') # plot the fitted data
plt.title("salinity")
makeplot.show()

# plt.show()

# now try and write the data to a netcdf file:
# the data that needs to be written:
# try one dimensions first
data1 = init_dept

# create the file container:
testfile = netcdffile("testfile.nc","w",format="NETCDF3_64BIT")
testfile.description = "this is a test file"
testfile.positive = "this is a positive statement"

# create the dimension and the depths variable
testfile.createDimension("dep_dim",len(data1))
depths = testfile.createVariable("depth","d",("dep_dim","dep_dim"))
depths.positive = "helllllllo"

# fill in the values
depths[:,:] = np.ones([len(data1), len(data1)])
testfile.close()





open_test_file = opennc("testfile.nc",1)
dep = getvar(open_test_file,"depth",1)
print(dep)











