# kirodh boodhraj
# 27 July 2016
# For help with function use, please look in the function files itself, all is explained there

# import the necessary libraries
from processTempandSal import processTempandSal
from opennc import opennc
from pRMSE import pRMSE
from pvert_grid import pvert_grid
from extractdata import extractdata
from getvar import getvar
from pgraph import pgraph
from netCDF4 import Dataset as netcdffile
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.basemap import Basemap
import pylab
import time as time

# this code is to analyse the runs from the c1d_PAPA case after modifying the turbulence schemes (TKE,generic,ke,kw,kkl)
#   for a constant number of vertical levels of 75

# type of turbulence scheme: (change this, ke, kw, generic, kkl, TKE0, TKE10, TKE30)
scheme = "ke"



###########################

# for the original data:

###########################
# Open the netcdf files using the file paths for the files:
# init = opennc("initial_conditions/init_PAPASTATION_m06d15.nc",0)# initial conditions
orig_T = opennc("original_data/t50n145w_dy.cdf",0)              # original data
orig_S = opennc("original_data/s50n145w_dy.cdf",0)

# get/open original data variables here:
time_orig = getvar(orig_S,"time",0) # use one time for all calc, set to 364 days
temp_orig = getvar(orig_T,"T_20",0); #print(temp_orig[0,:])# get temperatures and salinities
sal_orig = getvar(orig_S,"S_41",0)
temp_depth_orig = getvar(orig_T,"depth",0) # get the depths
sal_depth_orig= getvar(orig_S,"depth",0)

# plt.plot(temp_orig)
# print(sal_depth_orig)

# process the original Temp and Sal data:
# This will resize and get rid of NaN values from the data
# it is to exclude the (obvious) 1,1 dimension that s the 3rd and 4th dimension, must include the time steps 364 of them as well as the temp and sal data for each time step.
[temp_orig ,sal_orig]= processTempandSal(temp_orig,sal_orig,len(time_orig))
# print(temp_orig.shape) # testing
# print(sal_orig.shape)
# plt.plot(temp_orig)


###########################

# for the calculated data:

###########################

# (CHANGE FOLDER NAMES ONLY) and all should be fine
# # open the files
scheme_T_21 = opennc("lev21/"+scheme+"/PAPA_1d_20100615_20110614_grid_T.nc",0)#output from NEMO, T,W files
scheme_W_21 = opennc("lev21/"+scheme+"/PAPA_1d_20100615_20110614_grid_W.nc",0)
scheme_T_51 = opennc("lev51/"+scheme+"/PAPA_1d_20100615_20110614_grid_T.nc",0)#output from NEMO, T,W files
scheme_W_51 = opennc("lev51/"+scheme+"/PAPA_1d_20100615_20110614_grid_W.nc",0)
scheme_T_75 = opennc("lev75/"+scheme+"/PAPA_1d_20100615_20110614_grid_T.nc",0)#output from NEMO, T,W files
scheme_W_75 = opennc("lev75/"+scheme+"/PAPA_1d_20100615_20110614_grid_W.nc",0)
scheme_T_101 = opennc("lev101/"+scheme+"/PAPA_1d_20100615_20110614_grid_T.nc",0)#output from NEMO, T,W files
scheme_W_101 = opennc("lev101/"+scheme+"/PAPA_1d_20100615_20110614_grid_W.nc",0)
scheme_T_151 = opennc("lev151/"+scheme+"/PAPA_1d_20100615_20110614_grid_T.nc",0)#output from NEMO, T,W files
scheme_W_151 = opennc("lev151/"+scheme+"/PAPA_1d_20100615_20110614_grid_W.nc",0)


# get the important depth variable data for calculations
depth_cal_21 = getvar(scheme_T_21,"deptht",0)
depth_cal_51 = getvar(scheme_T_51,"deptht",0)
depth_cal_75 = getvar(scheme_T_75,"deptht",0)
depth_cal_101 = getvar(scheme_T_101,"deptht",0)
depth_cal_151 = getvar(scheme_T_151,"deptht",0)
# print(depth_cal_21)



# now extract the temp and sal data from the original data using the original depths, this function will fit a spline and get the data needed for te temp and sal
[Ndepth_21, temp_orig_21, sal_orig_21] = extractdata(depth_cal_21,temp_depth_orig,temp_orig,sal_depth_orig,sal_orig,0,len(time_orig))
[Ndepth_51, temp_orig_51, sal_orig_51] = extractdata(depth_cal_51,temp_depth_orig,temp_orig,sal_depth_orig,sal_orig,0,len(time_orig))
[Ndepth_75, temp_orig_75, sal_orig_75] = extractdata(depth_cal_75,temp_depth_orig,temp_orig,sal_depth_orig,sal_orig,0,len(time_orig))
[Ndepth_101, temp_orig_101, sal_orig_101] = extractdata(depth_cal_101,temp_depth_orig,temp_orig,sal_depth_orig,sal_orig,0,len(time_orig))
[Ndepth_151, temp_orig_151, sal_orig_151] = extractdata(depth_cal_151,temp_depth_orig,temp_orig,sal_depth_orig,sal_orig,0,len(time_orig))

# print(temp_orig[0,:])

# # test the dimensions:
# print(temp_orig.shape) # here and below the get var functions, the prints should have the same dimesions
# print(sal_orig.shape)

# get calculated variables here(for the different closure schemes):
# note that the variable is pulled from within the resizing function itself, for convenience. (resizing is done with the [0:364,:,1,1] at the end of the getvar function)
temp_scheme_21 = getvar(scheme_T_21,"votemper",0)[0:364,:,1,1]
sal_scheme_21 = getvar(scheme_T_21,"vosaline",0)[0:364,:,1,1]
temp_scheme_51 = getvar(scheme_T_51,"votemper",0)[0:364,:,1,1]
sal_scheme_51 = getvar(scheme_T_51,"vosaline",0)[0:364,:,1,1]
temp_scheme_75 = getvar(scheme_T_75,"votemper",0)[0:364,:,1,1]
sal_scheme_75 = getvar(scheme_T_75,"vosaline",0)[0:364,:,1,1]
temp_scheme_101 = getvar(scheme_T_101,"votemper",0)[0:364,:,1,1]
sal_scheme_101 = getvar(scheme_T_101,"vosaline",0)[0:364,:,1,1]
temp_scheme_151 = getvar(scheme_T_151,"votemper",0)[0:364,:,1,1]
sal_scheme_151 = getvar(scheme_T_151,"vosaline",0)[0:364,:,1,1]


# print(temp_scheme_21.shape) # part of the test from the top two print statements
# print(sal_scheme.shape)
# print(sal_orig)
# print(temp_orig)
# plt.plot(sal_orig)



############################################

# plot the temps and sals per day value

############################################

# # # # plotting the actual data for salinity and temperature daily with a time delay
# for t in time_orig.tolist():
#     plt.figure()
#     # plt.gca().invert_yaxis() # inverts the y axis, doesnt work
#     plt.plot(temp_scheme_21[t,:],Ndepth_21,"mo-") # plot the graphs for different levels
#     plt.plot(temp_scheme_51[t,:],Ndepth_51,"r*-")
#     plt.plot(temp_scheme_75[t,:],Ndepth_75,"go-")
#     plt.plot(temp_scheme_101[t,:],Ndepth_101,"y*-")
#     plt.plot(temp_scheme_151[t,:],Ndepth_151,"c*-")
#     plt.title(str(t))
#
#     pylab.ylim([0,500])
#
#     plt.pause(0.5) # pause the graph
#     plt.close()
# # theres a lot! dont do this with all the time...
# copy this above code and change to sal if need salinity data



##################################################################

# plot the RMSE's for a certain day for all level choices

##################################################################

# # now plot the RMSE values
# # for salinity and temperature


temp_rmse_21 = pRMSE(temp_scheme_21,temp_orig_21,35,2.5,1,"ke temperature RMSE",None,None,None,1,0)
sal_rmse_21 = pRMSE(sal_scheme_21,sal_orig_21,35,2.5,1,"ke salinity RMSE",None,None,None,1,0)
temp_rmse_51 = pRMSE(temp_scheme_51,temp_orig_51,35,2.5,1,"ke temperature RMSE",None,None,None,1,0)
sal_rmse_51 = pRMSE(sal_scheme_51,sal_orig_51,35,2.5,1,"ke salinity RMSE",None,None,None,1,0)
temp_rmse_75 = pRMSE(temp_scheme_75,temp_orig_75,35,2.5,1,"ke temperature RMSE",None,None,None,1,0)
sal_rmse_75 = pRMSE(sal_scheme_75,sal_orig_75,35,2.5,1,"ke salinity RMSE",None,None,None,1,0)
temp_rmse_101 = pRMSE(temp_scheme_101,temp_orig_101,35,2.5,1,"ke temperature RMSE",None,None,None,1,0)
sal_rmse_101 = pRMSE(sal_scheme_101,sal_orig_101,35,2.5,1,"ke salinity RMSE",None,None,None,1,0)
temp_rmse_151 = pRMSE(temp_scheme_151,temp_orig_151,35,2.5,1,"ke temperature RMSE",None,None,None,1,0)
sal_rmse_151 = pRMSE(sal_scheme_151,sal_orig_151,35,2.5,1,"ke salinity RMSE",None,None,None,1,0)


# print(temp_rmse_21)
# print("\n")
# print(sal_rmse_21)
# print("\n")
# print(temp_rmse_51)
# print("\n")
# print(sal_rmse_51)
# print("\n")
# print(temp_rmse_75)
# print("\n")
# print(sal_rmse_75)
# print("\n")
# print(temp_rmse_101)
# print("\n")
# print(sal_rmse_101)
# print("\n")
# print(temp_rmse_151)
# print("\n")
# print(sal_rmse_151)
# print("\n")

# plot the RMSE for a certain day
day = 200
# for temp:
plt.figure()
plt.title("temp")
plt.plot([temp_rmse_21[day-1],temp_rmse_51[day-1],temp_rmse_75[day-1],temp_rmse_101[day-1],temp_rmse_151[day-1]],"ro-")



# for sal:
plt.figure()
plt.title("sal")
plt.plot([sal_rmse_21[day-1],sal_rmse_51[day-1],sal_rmse_75[day-1],sal_rmse_101[day-1],temp_rmse_151[day-1]],"bo-")


# plot the RMSE for a certain day looping through


######################################################

# plot the depths and spacing between vertical grid

######################################################

# # plot the spacings of the grid, to show the hyperbolic tangent
# pvert_grid(Ndepth,1,35,2.5,0,150,[0,250])



# show all the plots
plt.show()
# a sentimental note, James again proves to have much more luck than I anticipated. A minor error fixed when he poped in the office :-)