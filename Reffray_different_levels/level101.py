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

# this code is to analyse the runs from the c1d_PAPA case after modifying the turbulence schemes (TKE,generic,ke,kw,kkl)
#   for a constant number of vertical levels of 75

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
ke_T = opennc("lev101/ke/PAPA_1d_20100615_20110614_grid_T.nc",0)#output from NEMO, T,W files
ke_W = opennc("lev101/ke/PAPA_1d_20100615_20110614_grid_W.nc",0)
kw_T = opennc("lev101/kw/PAPA_1d_20100615_20110614_grid_T.nc",0)
kw_W = opennc("lev101/kw/PAPA_1d_20100615_20110614_grid_W.nc",0)
kkl_T = opennc("lev101/kkl/PAPA_1d_20100615_20110614_grid_T.nc",0)
kkl_W = opennc("lev101/kkl/PAPA_1d_20100615_20110614_grid_W.nc",0)
generic_T = opennc("lev101/generic/PAPA_1d_20100615_20110614_grid_T.nc",0)
generic_W = opennc("lev101/generic/PAPA_1d_20100615_20110614_grid_W.nc",0)
TKE0_T = opennc("lev101/TKE0/PAPA_1d_20100615_20110614_grid_T.nc",0)
TKE0_W = opennc("lev101/TKE0/PAPA_1d_20100615_20110614_grid_W.nc",0)
TKE10_T = opennc("lev101/TKE10/PAPA_1d_20100615_20110614_grid_T.nc",0)
TKE10_W = opennc("lev101/TKE10/PAPA_1d_20100615_20110614_grid_W.nc",0)
TKE30_T = opennc("lev101/TKE30/PAPA_1d_20100615_20110614_grid_T.nc",0)
TKE30_W = opennc("lev101/TKE30/PAPA_1d_20100615_20110614_grid_W.nc",0)

# get the important depth variable data for calculations (can use any of the files above)
depth_cal = getvar(ke_T,"deptht",0)
# print(depth_cal)



# now extract the temp and sal data from the original data using the original depths, this function will fit a spline and get the data needed for te temp and sal
[Ndepth, temp_orig, sal_orig] = extractdata(depth_cal,temp_depth_orig,temp_orig,sal_depth_orig,sal_orig,0,len(time_orig))

# print(temp_orig[0,:])

# # test the dimensions:
# print(temp_orig.shape) # here and below the get var functions, the prints should have the same dimesions
# print(sal_orig.shape)

# get calculated variables here(for the different closure schemes):
# note that the variable is pulled from within the resizing function itself, for convenience. (resizing is done with the [0:364,:,1,1] at the end of the getvar function)
temp_ke = getvar(ke_T,"votemper",0)[0:364,:,1,1]
sal_ke = getvar(ke_T,"vosaline",0)[0:364,:,1,1]
temp_kw = getvar(kw_T,"votemper",0)[0:364,:,1,1]
sal_kw = getvar(kw_T,"vosaline",0)[0:364,:,1,1]
temp_kkl = getvar(kkl_T,"votemper",0)[0:364,:,1,1]
sal_kkl = getvar(kkl_T,"vosaline",0)[0:364,:,1,1]
temp_generic = getvar(generic_T,"votemper",0)[0:364,:,1,1]
sal_generic = getvar(generic_T,"vosaline",0)[0:364,:,1,1]
temp_TKE0 = getvar(TKE0_T,"votemper",0)[0:364,:,1,1]
sal_TKE0 = getvar(TKE0_T,"vosaline",0)[0:364,:,1,1]
temp_TKE10 = getvar(TKE10_T,"votemper",0)[0:364,:,1,1]
sal_TKE10 = getvar(TKE10_T,"vosaline",0)[0:364,:,1,1]
temp_TKE30 = getvar(TKE30_T,"votemper",0)[0:364,:,1,1]
sal_TKE30 = getvar(TKE30_T,"vosaline",0)[0:364,:,1,1]

# print(temp_ke.shape) # part of the test from the top two print statements
# print(sal_ke.shape)
# print(sal_orig)
# print(temp_orig)
# plt.plot(sal_orig)



################################

# plot the temps and sals

################################

# # # plotting the actual data for salinity and temperature
pgraph(time_orig,Ndepth,temp_ke,"Time (days)","Depth (m)",35,1,0,1,None,[0,150],None,"ke temperature")
# pgraph(time_orig,Ndepth,sal_ke,"Time (days)","Depth (m)",35,1,0,1,None,[0,150],[32,33],"ke salinity")
# pgraph(time_orig,Ndepth,temp_kw,"Time (days)","Depth (m)",35,1,0,1,None,[0,150],None,"kw temperature")
# pgraph(time_orig,Ndepth,sal_kw,"Time (days)","Depth (m)",35,1,0,1,None,[0,150],[32,33],"kw salinity")
# pgraph(time_orig,Ndepth,temp_kkl,"Time (days)","Depth (m)",35,1,0,1,None,[0,150],None,"kkl temperature")
# pgraph(time_orig,Ndepth,sal_kkl,"Time (days)","Depth (m)",35,1,0,1,None,[0,150],[32,33],"kkl salinity")
# pgraph(time_orig,Ndepth,temp_generic,"Time (days)","Depth (m)",35,1,0,1,None,[0,150],None,"generic temperature")
# pgraph(time_orig,Ndepth,sal_generic,"Time (days)","Depth (m)",35,1,0,1,None,[0,150],[32,33],"generic salinity")
# pgraph(time_orig,Ndepth,temp_TKE0,"Time (days)","Depth (m)",35,1,0,1,None,[0,150],None,"TKE0 temperature")
# pgraph(time_orig,Ndepth,sal_TKE0,"Time (days)","Depth (m)",35,1,0,1,None,[0,150],[32,33],"TKE0 salinity")
# pgraph(time_orig,Ndepth,temp_TKE10,"Time (days)","Depth (m)",35,1,0,1,None,[0,150],None,"TKE10 temperature")
# pgraph(time_orig,Ndepth,sal_TKE10,"Time (days)","Depth (m)",35,1,0,1,None,[0,150],[32,33],"TKE10 salinity")
# pgraph(time_orig,Ndepth,temp_TKE30,"Time (days)","Depth (m)",35,1,0,1,None,[0,150],None,"TKE30 temperature")
# pgraph(time_orig,Ndepth,sal_TKE30,"Time (days)","Depth (m)",35,1,0,1,None,[0,150],[32,33],"TKE30 salinity")





#######################

# plot the biases

#######################

# # plot biases
# # temp and salinity biases for each turbulence scheme
# # the main variables needed for this is the time_orig, Ndepth, temps/sals from the turb schemes and the temp/sal_orig
# pgraph(time_orig,Ndepth,np.subtract(temp_ke,temp_orig),"Time (days)","Depth (m)",35,1,0,1,None,[0,150],[-2.5,2.5],"ke temperature bias")
# pgraph(time_orig,Ndepth,np.subtract(sal_ke,sal_orig),"Time (days)","Depth (m)",35,1,0,1,None,[0,150],[-.25,.25],"ke salinity bias")
# pgraph(time_orig,Ndepth,np.subtract(temp_kw,temp_orig),"Time (days)","Depth (m)",35,1,0,1,None,[0,150],[-2.5,2.5],"kw temperature bias")
# pgraph(time_orig,Ndepth,np.subtract(sal_kw,sal_orig),"Time (days)","Depth (m)",35,1,0,1,None,[0,150],[-.25,.25],"kw salinity bias")
# pgraph(time_orig,Ndepth,np.subtract(temp_kkl,temp_orig),"Time (days)","Depth (m)",35,1,0,1,None,[0,150],[-2.5,2.5],"kkl temperature bias")
# pgraph(time_orig,Ndepth,np.subtract(sal_kkl,sal_orig),"Time (days)","Depth (m)",35,1,0,1,None,[0,150],[-.25,.25],"kkl salinity bias")
# pgraph(time_orig,Ndepth,np.subtract(temp_generic,temp_orig),"Time (days)","Depth (m)",35,1,0,1,None,[0,150],[-2.5,2.5],"generic temperature bias")
# pgraph(time_orig,Ndepth,np.subtract(sal_generic,sal_orig),"Time (days)","Depth (m)",35,1,0,1,None,[0,150],[-.25,.25],"generic salinity bias")
# pgraph(time_orig,Ndepth,np.subtract(temp_TKE0,temp_orig),"Time (days)","Depth (m)",35,1,0,1,None,[0,150],[-2.5,2.5],"TKE0 temperature bias")
# pgraph(time_orig,Ndepth,np.subtract(sal_TKE0,sal_orig),"Time (days)","Depth (m)",35,1,0,1,None,[0,150],[-.25,.25],"TKE0 salinity bias")
# pgraph(time_orig,Ndepth,np.subtract(temp_TKE10,temp_orig),"Time (days)","Depth (m)",35,1,0,1,None,[0,150],[-2.5,2.5],"TKE10 temperature bias")
# pgraph(time_orig,Ndepth,np.subtract(sal_TKE10,sal_orig),"Time (days)","Depth (m)",35,1,0,1,None,[0,150],[-.25,.25],"TKE10 salinity bias")
# pgraph(time_orig,Ndepth,np.subtract(temp_TKE30,temp_orig),"Time (days)","Depth (m)",35,1,0,1,None,[0,150],[-2.5,2.5],"TKE30 temperature bias")
# pgraph(time_orig,Ndepth,np.subtract(sal_TKE30,sal_orig),"Time (days)","Depth (m)",35,1,0,1,None,[0,150],[-.25,.25],"TKE30 salinity bias")


######################

# plot the RMSE's

######################

# # now plot the RMSE values
# # for salinity and temperature
# # print(temp_ke)
# # print(temp_orig)
# pRMSE(temp_ke,temp_orig,35,2.5,1,"ke temperature RMSE")#,1.5,[0,1.5])
# pRMSE(sal_ke,sal_orig,35,2.5,1,"ke salinity RMSE")#,0.1,[0,1.5])
# pRMSE(temp_kw,temp_orig,35,2.5,1,"kw temperature RMSE",1.5,[0,1.5])
# pRMSE(sal_kw,sal_orig,35,2.5,1,"kw salinity RMSE",0.1,[0,1.5])
# pRMSE(temp_kkl,temp_orig,35,2.5,1,"kkl temperature RMSE",1.5,[0,1.5])
# pRMSE(sal_kkl,sal_orig,35,2.5,1,"kkl salinity RMSE",0.1,[0,1.5])
# pRMSE(temp_generic,temp_orig,35,2.5,1,"generic temperature RMSE",1.5,[0,1.5])
# pRMSE(sal_generic,sal_orig,35,2.5,1,"generic salinity RMSE",0.1,[0,1.5])
# pRMSE(temp_TKE0,temp_orig,35,2.5,1,"TKE0 temperature RMSE",1.5,[0,1.5])
# pRMSE(sal_TKE0,sal_orig,35,2.5,1,"TKE0 salinity RMSE",0.1,[0,1.5])
# pRMSE(temp_TKE10,temp_orig,35,2.5,1,"TKE10 temperature RMSE",1.5,[0,1.5])
# pRMSE(sal_TKE10,sal_orig,35,2.5,1,"TKE10 salinity RMSE",0.1,[0,1.5])
# pRMSE(temp_TKE30,temp_orig,35,2.5,1,"TKE30 temperature RMSE",1.5,[0,1.5])
# pRMSE(sal_TKE30,sal_orig,35,2.5,1,"TKE30 salinity RMSE",0.1,[0,1.5])



######################################################

# plot the depths and spacing between vertical grid

######################################################

# # plot the spacings of the grid, to show the hyperbolic tangent
# pvert_grid(Ndepth,1,35,2.5,0,150,[0,250])



# show all the plots
plt.show()
# a sentimental note, James again proves to have much more luck than I anticipated. A minor error fixed when he poped in the office :-)