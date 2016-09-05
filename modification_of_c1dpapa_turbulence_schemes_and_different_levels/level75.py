# kirodh boodhraj
# 27 July 2016
# For help with function use, please look in the function files itself, all is explained there

# import the necessary libraries
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

# Open the netcdf files using the file paths for the files:
init = opennc("initial_conditions/init_PAPASTATION_m06d15.nc",0)# initial conditions
orig_T = opennc("original_data/t50n145w_dy.cdf",0)              # original data
orig_S = opennc("original_data/s50n145w_dy.cdf",0)
ke_T = opennc("nc_files_ke_lev75/PAPA_1d_20100615_20110614_grid_T.nc",0)#output from NEMO, T,W files
ke_W = opennc("nc_files_ke_lev75/PAPA_1d_20100615_20110614_grid_W.nc",0)
kw_T = opennc("nc_files_kw_lev75/PAPA_1d_20100615_20110614_grid_T.nc",0)
kw_W = opennc("nc_files_kw_lev75/PAPA_1d_20100615_20110614_grid_W.nc",0)
kkl_T = opennc("nc_files_kkl_lev75/PAPA_1d_20100615_20110614_grid_T.nc",0)
kkl_W = opennc("nc_files_kkl_lev75/PAPA_1d_20100615_20110614_grid_W.nc",0)
generic_T = opennc("nc_files_generic_lev75/PAPA_1d_20100615_20110614_grid_T.nc",0)
generic_W = opennc("nc_files_generic_lev75/PAPA_1d_20100615_20110614_grid_W.nc",0)
TKE0_T = opennc("nc_files_TKE0_lev75/PAPA_1d_20100615_20110614_grid_T.nc",0)
TKE0_W = opennc("nc_files_TKE0_lev75/PAPA_1d_20100615_20110614_grid_W.nc",0)
TKE10_T = opennc("nc_files_TKE10_lev75/PAPA_1d_20100615_20110614_grid_T.nc",0)
TKE10_W = opennc("nc_files_TKE10_lev75/PAPA_1d_20100615_20110614_grid_W.nc",0)
TKE30_T = opennc("nc_files_TKE30_lev75/PAPA_1d_20100615_20110614_grid_T.nc",0)
TKE30_W = opennc("nc_files_TKE30_lev75/PAPA_1d_20100615_20110614_grid_W.nc",0)

# initial variables
# put in the indexes to map the depth values here: (found from observation)
mapindexsalinity = [1,8,11,13,14,15,17,19,22,24,25,28,30]; #print(len(mapindexsalinity))
mapindextemperature = [1,4,8,9,10,11,13,14,15,17,19,21,24,25,27,29,30,34]; #print(len(mapindextemperature))
# initial variables done

# get/open original data variables here:
time_orig = getvar(orig_S,"time",0) # use one time for all calc, set to 364 days
temp_orig = getvar(orig_T,"T_20",0); #print(temp_orig[0,:])# get temperatures and salinities
sal_orig = getvar(orig_S,"S_41",0)
depth_temp_orig = getvar(orig_T,"depth",0) # get the depths
depth_sal_orig= getvar(orig_S,"depth",0)

# will need to resize from 4 dims to 2 dims otherwise havoc
# it is to exclude the (obvious) 1,1 dimension that s the 3rd and 4th dimension, must include the time steps 364 of them as well as the temp and sal data for each time step.
temp_orig = temp_orig[0:len(time_orig),:].reshape(len(time_orig),len(mapindextemperature)) #also need to use 364 indexes out of 365 because of the data structures
sal_orig = sal_orig.reshape(len(time_orig),len(mapindexsalinity))
# original data done

# get calculated variables here(for the different closure schemes):
# note that the variable is pulled from within the resizing function itself, for convenience. (resizing is done with the [:,:,1,1] at the end of the getvar function)
temp_ke = extractdata(getvar(ke_T,"votemper",0)[:,:,1,1],mapindextemperature,0)
sal_ke = extractdata(getvar(ke_T,"vosaline",0)[:,:,1,1],mapindexsalinity,0)
temp_kw = extractdata(getvar(kw_T,"votemper",0)[:,:,1,1],mapindextemperature,0)
sal_kw = extractdata(getvar(kw_T,"vosaline",0)[:,:,1,1],mapindexsalinity,0)
temp_kkl = extractdata(getvar(kkl_T,"votemper",0)[:,:,1,1],mapindextemperature,0)
sal_kkl = extractdata(getvar(kkl_T,"vosaline",0)[:,:,1,1],mapindexsalinity,0)
temp_generic = extractdata(getvar(generic_T,"votemper",0)[:,:,1,1],mapindextemperature,0)
sal_generic = extractdata(getvar(generic_T,"vosaline",0)[:,:,1,1],mapindexsalinity,0)
temp_TKE0 = extractdata(getvar(TKE0_T,"votemper",0)[:,:,1,1],mapindextemperature,0)
sal_TKE0 = extractdata(getvar(TKE0_T,"vosaline",0)[:,:,1,1],mapindexsalinity,0)
temp_TKE10 = extractdata(getvar(TKE10_T,"votemper",0)[:,:,1,1],mapindextemperature,0)
sal_TKE10 = extractdata(getvar(TKE10_T,"vosaline",0)[:,:,1,1],mapindexsalinity,0)
temp_TKE30 = extractdata(getvar(TKE30_T,"votemper",0)[:,:,1,1],mapindextemperature,0)
sal_TKE30 = extractdata(getvar(TKE30_T,"vosaline",0)[:,:,1,1],mapindexsalinity,0)


# # plot biases
# # temp and salinity biases for each turbulence scheme
# pgraph(time_orig,depth_temp_orig,np.subtract(temp_ke,temp_orig),"Time (days)","Depth (m)",35,1,0,1,None,[0,150],[-2.5,2.5],"ke temperature bias")
# pgraph(time_orig,depth_sal_orig,np.subtract(sal_ke,sal_orig),"Time (days)","Depth (m)",35,1,0,1,None,[0,150],[-.25,.25],"ke salinity bias")
# pgraph(time_orig,depth_temp_orig,np.subtract(temp_kw,temp_orig),"Time (days)","Depth (m)",35,1,0,1,None,[0,150],[-2.5,2.5],"kw temperature bias")
# pgraph(time_orig,depth_sal_orig,np.subtract(sal_kw,sal_orig),"Time (days)","Depth (m)",35,1,0,1,None,[0,150],[-.25,.25],"kw salinity bias")
# pgraph(time_orig,depth_temp_orig,np.subtract(temp_kkl,temp_orig),"Time (days)","Depth (m)",35,1,0,1,None,[0,150],[-2.5,2.5],"kkl temperature bias")
# pgraph(time_orig,depth_sal_orig,np.subtract(sal_kkl,sal_orig),"Time (days)","Depth (m)",35,1,0,1,None,[0,150],[-.25,.25],"kkl salinity bias")
# pgraph(time_orig,depth_temp_orig,np.subtract(temp_generic,temp_orig),"Time (days)","Depth (m)",35,1,0,1,None,[0,150],[-2.5,2.5],"generic temperature bias")
# pgraph(time_orig,depth_sal_orig,np.subtract(sal_generic,sal_orig),"Time (days)","Depth (m)",35,1,0,1,None,[0,150],[-.25,.25],"generic salinity bias")
# pgraph(time_orig,depth_temp_orig,np.subtract(temp_TKE0,temp_orig),"Time (days)","Depth (m)",35,1,0,1,None,[0,150],[-2.5,2.5],"TKE0 temperature bias")
# pgraph(time_orig,depth_sal_orig,np.subtract(sal_TKE0,sal_orig),"Time (days)","Depth (m)",35,1,0,1,None,[0,150],[-.25,.25],"TKE0 salinity bias")
# pgraph(time_orig,depth_temp_orig,np.subtract(temp_TKE10,temp_orig),"Time (days)","Depth (m)",35,1,0,1,None,[0,150],[-2.5,2.5],"TKE10 temperature bias")
# pgraph(time_orig,depth_sal_orig,np.subtract(sal_TKE10,sal_orig),"Time (days)","Depth (m)",35,1,0,1,None,[0,150],[-.25,.25],"TKE10 salinity bias")
# pgraph(time_orig,depth_temp_orig,np.subtract(temp_TKE30,temp_orig),"Time (days)","Depth (m)",35,1,0,1,None,[0,150],[-2.5,2.5],"TKE30 temperature bias")
# pgraph(time_orig,depth_sal_orig,np.subtract(sal_TKE30,sal_orig),"Time (days)","Depth (m)",35,1,0,1,None,[0,150],[-.25,.25],"TKE30 salinity bias")



#
# # now plot the RMSE values
# # for salinity and temperature
# pRMSE(temp_ke,temp_orig,35,2.5,1,"ke temperature RMSE",1.5,[0,1.5])
# pRMSE(sal_ke,sal_orig,35,2.5,1,"ke salinity RMSE",0.1,[0,1.5])
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


# plot the spacings of the grid, to show the hyperbolic tangent
depth_full = getvar(ke_T,"deptht") # get all the depths

pvert_grid(depth_full,1,35,2.5,0,150,[0,250]) # spacing of grid plot

# plotting the actual data for salinity and temperature
temp_fulltke10 = getvar(ke_T,"votemper")[0:len(time_orig),:,1,1] # get all the  temp's and sal's
sal_fulltke10 = getvar(ke_T,"vosaline")[0:len(time_orig),:,1,1]

pgraph(time_orig,depth_full,temp_fulltke10,"Time (days)","Depth (m)",35,1,0,1,None,[0,150],None,"TKE10 temperature")
pgraph(time_orig,depth_full,sal_fulltke10,"Time (days)","Depth (m)",35,1,0,1,None,[0,150],[32,33],"TKE10 salinity")



plt.show()
# a sentimental note, James again proves to have much more luck than I anticipated. A minor error fixed when he poped in the office :-)