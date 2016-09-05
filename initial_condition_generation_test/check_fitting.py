# import the necessary libraries
from opennc import opennc
from getvar import getvar
from pinitgraph import pinitgraph

from netCDF4 import Dataset as netcdffile
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.basemap import Basemap
import pylab

# read initial conditions from NETcdf file ".nc"
infile1 = 'nc_files/chlorophyll_PAPASTATION.nc'
infile2 = 'nc_files/forcing_PAPASTATION_1h_y2010.nc'
infile3 = 'nc_files/forcing_PAPASTATION_1h_y2011.nc'
infile4 = 'nc_files/init_PAPASTATION_m06d15.nc'



# open the netcdf file
fh_chlor = opennc(infile1,1)
fh_2010 = opennc(infile2,1)
fh_2011 = opennc(infile3,1)
fh_init = opennc(infile4,1)

#####################################################

# get the variables and see which need changing....
# DC means it doesn't need changing and
# C means the variable needs changing

# # for fh_chlor: (nothing needs changing for this initial condition file)
# chlor_chlor= getvar(fh_chlor,"CHLA",1) # DC
# chlor_month= getvar(fh_chlor,"MONTH_REG",1) # DC
# chlor_xaxis= getvar(fh_chlor,"XAXIS",1) # DC
# chlor_yaxis= getvar(fh_chlor,"YAXIS",1) # DC


# # for fh_2010:
# f2010_lat = getvar(fh_2010,"nav_lat",1) # DC
# f2010_lon = getvar(fh_2010,"nav_lon",1) # DC
# f2010_wndwe = getvar(fh_2010,"wndwe",1) # DC
# f2010_wndsn = getvar(fh_2010,"wndsn",1) # DC
# f2010_tinst = getvar(fh_2010,"time_instant",1) # DC
# f2010_tcount = getvar(fh_2010,"time_counter",1) # DC
# f2010_relhumid = getvar(fh_2010,"humi_r",1) # DC
# f2010_humid = getvar(fh_2010,"humi",1) # DC
# f2010_sw = getvar(fh_2010,"qsr",1) # DC
# f2010_lw = getvar(fh_2010,"qlw",1) # DC
# f2010_airtem = getvar(fh_2010,"tair",1) # DC
# f2010_rain = getvar(fh_2010,"prec",1) # DC
# f2010_snow = getvar(fh_2010,"snow",1) # DC


# # for fh_2011:
# f2011_lat = getvar(fh_2011,"nav_lat",1) # DC
# f2011_lon = getvar(fh_2011,"nav_lon",1) # DC
# f2011_wndwe = getvar(fh_2011,"wndwe",1) # DC
# f2011_wndsn = getvar(fh_2011,"wndsn",1) # DC
# f2011_tinst = getvar(fh_2011,"time_instant",1) # DC
# f2011_tcount = getvar(fh_2011,"time_counter",1) # DC
# f2011_relhumid = getvar(fh_2011,"humi_r",1) # DC
# f2011_humid = getvar(fh_2011,"humi",1) # DC
# f2011_sw = getvar(fh_2011,"qsr",1) # DC
# f2011_lw = getvar(fh_2011,"qlw",1) # DC
# f2011_airtem = getvar(fh_2011,"tair",1) # DC
# f2011_rain = getvar(fh_2011,"prec",1) # DC
# f2011_snow = getvar(fh_2011,"snow",1) # DC


# for fh_init:
init_lon = getvar(fh_init,"longitude",1) # DC
init_lat = getvar(fh_init,"latitude",1) # DC
init_time = getvar(fh_init,"time_counter",1) # DC

init_dept = getvar(fh_init,"deptht",1); # C
init_temp = getvar(fh_init,"votemper",1) ; init_temp = init_temp[0,:,1,1] # C
init_sal = getvar(fh_init,"vosaline",1);init_sal = init_sal[0,:,1,1] # C

pinitgraph(init_dept,init_temp,"temperature")
# print(init_temp[:,:,1,1])
print(init_dept)
# print(init_lon)
# print(init_lat)

plt.show()


#####################################################





