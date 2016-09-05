# kirodh boodhraj
# 27 July 2016
# For help with function use, please look in the function files itself, all is explained there

# import the necessary libraries
from opennc import opennc
# from pRMSE import pRMSE
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
ke_T = opennc("ncfiles/PAPA_1d_20100615_20110614_grid_T.nc",0)#output from NEMO, T,W files
# ke_W = opennc("ncfiles_ke_lev75/PAPA_1d_20100615_20110614_grid_W.nc",0)

ke_T_temp = getvar(ke_T,"votemper",1)
ke_T_sal = getvar(ke_T,"vosaline",1)
ke_T_dep = getvar(ke_T,"deptht",1)
ke_T_time = getvar(ke_T,"time_counter",1)

pgraph(ke_T_time,ke_T_dep,ke_T_temp[0:364,:,1,1],"time (days)","depth",35,1,0,1,None,[0,200])
pgraph(ke_T_time,ke_T_dep,ke_T_sal[0:364,:,1,1],"time (days)","depth",35,1,0,1,None,[0,200])



plt.show()
# a sentimental note, James again proves to have much more luck than I anticipated. A minor error fixed when he poped in the office :-)