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
# # for 51:
# [space_t,other1,space_w,other2] = zgrid(51,np.nan,np.nan,np.nan,30.0,6.0,1.0,4200,0,np.nan,np.nan,np.nan)
# # for 21:
# [space_t,other1,space_w,other2] = zgrid(21,np.nan,np.nan,np.nan,15.0,3.0,1.0,4200,0,np.nan,np.nan,np.nan)
# # for 101:
# [space_t,other1,space_w,other2] = zgrid(101,np.nan,np.nan,np.nan,60.0,15.0,1.0,4200,0,np.nan,np.nan,np.nan)
# # for 101_ modified hyperbolic tangent function:
[space_t,other1,space_w,other2] = zgrid(101,np.nan,np.nan,np.nan,81.9,12.5,1.0,4200,0,np.nan,np.nan,np.nan)
# # for 151:
# [space_t,other1,space_w,other2] = zgrid(151,np.nan,np.nan,np.nan,100.0,20.0,1.0,4200,0,np.nan,np.nan,np.nan)



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



############
# plot the graphs to see if they are good or not
# for the temperature
makeplot = plt.figure() # make the plot
plt.plot(xdata,ydata_T,'ro-') # plot the orig data
plt.plot(xnew,fit_temp(xnew),'b*-') # plot the fitted data
makeplot.show()

# for the salinity
makeplot = plt.figure() # make the plot
plt.plot(xdata,ydata_S,'ro-') # plot the orig data
plt.plot(xnew,fit_sal(xnew),'b*-') # plot the fitted data
makeplot.show()

# plt.show()
#############

#################################
# write the netcdf file
# set out the temp and salinity and depth data for the new netcdf file
# give it the old subscript for clarity, these come from the original netcdf file
longitude_old = fh_init.variables["longitude"][:]
latitude_old = fh_init.variables["latitude"][:]
depth_old = xnew
time_old = fh_init.variables["time_counter"][:];# print(time_old)
temp_old = fit_temp(depth_old)
sal_old = fit_sal(depth_old)

# now write the data to the new_nc_file folder as the same file name with the modified data

# create the file container
new_file = netcdffile('new_nc_file/init_PAPASTATION_m06d15.nc',"w",format="NETCDF3_64BIT")

# create the dimensions variables
# this was done by looking at the original netcdf file and using the ncdump function to see the different dimensions and attributes
new_file.createDimension("longitude",len(longitude_old))
new_file.createDimension("latitude",len(latitude_old))
new_file.createDimension("deptht",len(depth_old))
new_file.createDimension("time_counter",None)

# create the variables and give then attributes:
longitude_new = new_file.createVariable("longitude","d",("longitude")) # no attributes and d is for double, f4 is for float
latitude_new = new_file.createVariable("latitude","d",("latitude"))

depth_new = new_file.createVariable("deptht","d",("deptht"))
depth_new.units = "m"
depth_new.positive = "down"
depth_new.point_spacing = "uneven"
depth_new.axis = "Z"
depth_new.standard_name = "depth"

time_new = new_file.createVariable("time_counter","d",("time_counter"))
time_new.units = "days since 1950-01-01 00:00:00"
time_new.time_origin = "01-JAN-1950 00:00:00"
time_new.axis = "T"
time_new.standard_name = "time"

temp_new = new_file.createVariable("votemper","d",("time_counter","deptht","latitude","longitude"))
sal_new = new_file.createVariable("vosaline","d",("time_counter","deptht","latitude","longitude"))


# now fill the variables with data
longitude_new[:] = longitude_old
latitude_new[:] = latitude_old
depth_new[:] = depth_old
time_new[:] = time_old
# write a 4 dim thing..., need to make a 3x3 layer per depth of the temp and salinity values
# for the temp:
# make a 3-d array and fill it with zeros according to the variables lengths
cont_T = np.zeros((len(depth_old),len(latitude_old),len(longitude_old)))
# now loop over each level and fill in the level with the temperature values
for i in range(len(depth_old)):
    # here we indicate each level with i and the [i,:,:] indicates the entire 3x3 level and the .fill
    # populates the level and the value that goes in is a numpy array value which needs to be converted in to a
    # list and then the list needs to be removed and this is done by taking the first value from it
    cont_T[i,:,:].fill(temp_old.tolist()[i])
# print(cont) # testing
print(cont_T.shape) # testing
cont_T.resize((1,len(depth_old),3,3)) # reshape the array
print(cont_T.shape)
temp_new[:,:,:,:] = np.array(cont_T) # write the data to the nc file


# for the sal:
# make a 3-d array and fill it with zeros according to the variables lengths
cont_S = np.zeros((len(depth_old),len(latitude_old),len(longitude_old)))
# now loop over each level and fill in the level with the temperature values
for i in range(len(depth_old)):
    # here we indicate each level with i and the [i,:,:] indicates the entire 3x3 level and the .fill
    # populates the level and the value that goes in is a numpy array value which needs to be converted in to a
    # list and then the list needs to be removed and this is done by taking the first value from it
    cont_S[i,:,:].fill(sal_old.tolist()[i])
# print(cont) # testing
# print(cont_S.shape) # testing
cont_S.resize((1,len(depth_old),3,3)) # reshape the array
# print(cont_S.shape)
sal_new[:,:,:,:] = np.array(cont_S) # write the data to the nc file



# dont forget to close the file
new_file.close()



# test the dimensions and data by opening and viewing data
open_test_file = opennc("new_nc_file/init_PAPASTATION_m06d15.nc",1)
dep = getvar(open_test_file,"votemper",1)
dep1 = getvar(open_test_file,"vosaline",1)
# print(dep.shape)
# print(dep[:,:,:])
# print(dep1.shape)
# print(dep1[:,:,:])



#################################

# this command made the record dimension
# ncks --mk_rec_dmn time_counter init_PAPASTATION_m06d15.nc init_PAPASTATION_m00d00.nc


