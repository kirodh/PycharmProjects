# import the necessary libraries
from docutils.parsers import null

from netCDF4 import Dataset as netcdffile
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.basemap import Basemap
import pylab

# read data from NETcdf file ".nc"

infile1_51 = 'nc_files/lev51/SAZ_1d_20100615_20141231_grid_T.nc'
infile2_51 = 'nc_files/lev51/SAZ_1d_20100615_20141231_grid_U.nc'
infile3_51 = 'nc_files/lev51/SAZ_1d_20100615_20141231_grid_V.nc'
infile4_51 = 'nc_files/lev51/SAZ_1d_20100615_20141231_grid_W.nc'
infile1_75 = 'nc_files/lev75/SAZL75_1d_20100615_20111214_grid_T.nc'
infile2_75 = 'nc_files/lev75/SAZL75_1d_20100615_20111214_grid_U.nc'
infile3_75 = 'nc_files/lev75/SAZL75_1d_20100615_20111214_grid_V.nc'
infile4_75 = 'nc_files/lev75/SAZL75_1d_20100615_20111214_grid_W.nc'
infile1_orig = 'nc_files/origdata/SAZ_1d_20100615_20111214_grid_T.nc'
infile2_orig = 'nc_files/origdata/SAZ_1d_20100615_20111214_grid_U.nc'
infile3_orig = 'nc_files/origdata/SAZ_1d_20100615_20111214_grid_V.nc'
infile4_orig = 'nc_files/origdata/SAZ_1d_20100615_20111214_grid_W.nc'


# create the file header
fh1_51 = netcdffile(infile1_51, mode='r')
fh2_51 = netcdffile(infile2_51, mode='r')
fh3_51 = netcdffile(infile3_51, mode='r')
fh4_51 = netcdffile(infile4_51, mode='r')
fh1_75 = netcdffile(infile1_75, mode='r')
fh2_75 = netcdffile(infile2_75, mode='r')
fh3_75 = netcdffile(infile3_75, mode='r')
fh4_75 = netcdffile(infile4_75, mode='r')
fh1_orig = netcdffile(infile1_orig,mode='r')
fh2_orig = netcdffile(infile2_orig,mode='r')
fh3_orig = netcdffile(infile3_orig,mode='r')
fh4_orig = netcdffile(infile4_orig,mode='r')

# print the headers
print(fh1_51)
print(fh2_51)
print(fh3_51)
print(fh4_51)
print(fh1_75)
print(fh2_75)
print(fh3_75)
print(fh4_75)
print(fh1_orig)
print(fh2_orig)
print(fh3_orig)
print(fh4_orig)


###############################################
# print the shape of variables to see whats going on
# different levels, in order of 51, 75, orig(not sure what number of levels yet)


# get the variables of interest for lev 51
lev51_long_lat_size = fh1_51.variables['nav_lon'][:] ; #print(lev51_long_lat_size.shape) # to make sure it is a 3x3
lev51_depth = fh1_51.variables['deptht'][:] ; #print("51dep:::"+str(lev51_depth.shape)) # depths
lev51_time = fh1_51.variables['time_counter'][:] ; #print("51:::"+str(lev51_time.shape)) # time counter
lev51_temp = fh1_51.variables['votemper'][:]; #print("51sal"+str(lev51_temp.shape)) # temp data
lev51_sal = fh1_51.variables['vosaline'][:]; #print("51sal"+str(lev51_sal.shape)) #salinity data
# use the middle column of the grid for the sdalinity and temperature
days = 365
lev51_time = lev51_time[0:days]
lev51_temp = lev51_temp[0:days,:,1,1]; print("51sal"+str(lev51_temp.shape))
lev51_sal = lev51_sal[0:days,:,1,1]; print("51sal"+str(lev51_sal.shape))
print("51:::"+str(lev51_time.shape))

### make a counter to indicate days rather than any other unit, netcdf gives wierd time step on x axis
time = []
for i in range(0,365):
    time.append(i)
time = np.array(time)

# now plot the data
lev51_salinity_plot = plt.figure() # create the figure
plt.pcolormesh(time,lev51_depth,lev51_sal.T) # need to transpose the matrix data! then all is good
lev51_salinity_plot.show()
cb = plt.colorbar()
plt.gca().invert_yaxis() # inverts the depth axis
pylab.ylim([220,0]) # set the y axis limits
plt.title('Salinity using SO conditions, 51 levels\n',fontsize = 35)
plt.clim([33.8,34.2]) # to set the colour bar limits
cb.ax.tick_params(labelsize = 35)
plt.tick_params(labelsize=35)
plt.xlabel('Time(days)',fontsize = 35)
plt.ylabel('Depth',fontsize = 35)
# plt.set_cmap('gray') # set the plot to grayscale for SASAS paper


lev51_temp_plot = plt.figure() # create the figure
plt.pcolormesh(time,lev51_depth,lev51_temp.T) # need to transpose the matrix data! then all is good
lev51_temp_plot.show()
cb = plt.colorbar()
plt.gca().invert_yaxis() # inverts the depth axis
pylab.ylim([220,0]) # set the y axis limits
plt.title('Temperature using SO conditions, 51 levels\n',fontsize = 35)
plt.clim(1,13)#8.5) # to set the colour bar limits
cb.ax.tick_params(labelsize = 35)
plt.tick_params(labelsize=35)
plt.xlabel('Time(days)',fontsize = 35)
plt.ylabel("Depth",fontsize = 35)
# plt.set_cmap('gray') # set the plot to grayscale for SASAS paper




# get the variables of interest for lev 75
lev75_long_lat_size = fh1_75.variables['nav_lon'][:] ; #print(lev75_long_lat_size.shape) # to make sure it is a 3x3
lev75_depth = fh1_75.variables['deptht'][:] ; #print(lev75_depth.shape) # depths
lev75_time = fh1_75.variables['time_counter'][:] ; #print(lev75_time.shape) # time counter
lev75_temp = fh1_75.variables['votemper'][:]; print(lev75_temp.shape) # temp data
lev75_sal = fh1_75.variables['vosaline'][:]; #print(lev75_sal.shape) #salinity data
# use the middle column of the grid for the sdalinity and temperature and make all the time steps the same at 545
lev51_time = lev51_time[0:days] ;# print(lev51_time.shape)
lev75_temp = lev75_temp[0:days,:,1,1]; print("75sal"+str(lev75_temp.shape))
lev75_sal = lev75_sal[0:days,:,1,1]; print("75temp"+str(lev75_sal.shape))
print("75:::"+str(lev75_time.shape))


# now plot the data
lev75_salinity_plot = plt.figure() # create the figure
plt.pcolormesh(time,lev75_depth,lev75_sal.T) # need to transpose the matrix data! then all is good
lev75_salinity_plot.show()
cb = plt.colorbar()
plt.gca().invert_yaxis() # inverts the depth axis
pylab.ylim([220,0]) # set the y axis limits
plt.title('Salinity using SO conditions, 75 levels\n',fontsize = 35)
# plt.clim([33.8,34.2]) # to set the colour bar limits
plt.clim([33.9,34.2]) # to set the colour bar limits
cb.ax.tick_params(labelsize = 35)
plt.tick_params(labelsize=35)
plt.xlabel('Time(days)',fontsize = 35)
plt.ylabel('Depth',fontsize = 35)
# plt.set_cmap('gray') # set the plot to grayscale for SASAS paper


lev75_temp_plot = plt.figure() # create the figure
plt.pcolormesh(time,lev75_depth,lev75_temp.T) # need to transpose the matrix data! then all is good
lev75_temp_plot.show()
cb = plt.colorbar()
plt.gca().invert_yaxis() # inverts the depth axis
pylab.ylim([220,0]) # set the y axis limits
plt.title('Temperature using SO conditions, 75 levels\n',fontsize = 35)
# plt.clim(1,8.5) # to set the colour bar limits
plt.clim(1,13) # to set the colour bar limits
cb.ax.tick_params(labelsize = 35)
plt.tick_params(labelsize=35)
plt.xlabel('Time(days)',fontsize = 35)
plt.ylabel('Depth',fontsize = 35)
# plt.set_cmap('gray') # set the plot to grayscale for SASAS paper

print(lev51_depth)


# dont use this block of comments
# # get the variables of interest for orig data; Turns out this is also 51 levels
# levorig_long_lat_size = fh1_orig.variables['nav_lon'][:] ; #print(levorig_long_lat_size.shape) # to make sure it is a 3x3
# levorig_depth = fh1_orig.variables['deptht'][:] ; print("depth: "+str(levorig_depth.shape)) # depths
# levorig_time = fh1_orig.variables['time_counter'][:] ; print(levorig_time.shape) # time counter
# levorig_temp = fh1_orig.variables['votemper'][:]; #print(levorig_temp.shape) # temp data
# levorig_sal = fh1_orig.variables['vosaline'][:]; #print(levorig_sal.shape) #salinity data
# # use the middle column of the grid for the sdalinity and temperature and make all the time steps the same at 545
# lev51_time = lev51_time[0:545]
# levorig_temp = levorig_temp[:,0:545,1,1]; print(levorig_temp.shape)
# levorig_sal = levorig_sal[:,0:545,1,1]; #print(levorig_sal.shape)
#
# # now plot the data
# levorig_salinity_plot = plt.figure() # create the figure
# plt.pcolormesh(levorig_time,levorig_depth,levorig_sal.T) # need to transpose the matrix data! then all is good
# levorig_salinity_plot.show()
# cb = plt.colorbar()
# plt.gca().invert_yaxis() # inverts the depth axis
# # pylab.ylim([4100,0]) # set the y axis limits
# plt.title('Salinity from model',fontsize = 30)
# # plt.clim(33.75,34.75) # to set the colour bar limits
# cb.ax.tick_params(labelsize = 35)
# plt.tick_params(labelsize=35)
# plt.xlabel('Time counter',fontsize = 20)
# plt.ylabel('Depth',fontsize = 20)
#
# levorig_temp_plot = plt.figure() # create the figure
# plt.pcolormesh(levorig_time,levorig_depth,levorig_temp.T) # need to transpose the matrix data! then all is good
# levorig_temp_plot.show()
# cb = plt.colorbar()
# plt.gca().invert_yaxis() # inverts the depth axis
# # pylab.ylim([4100,0]) # set the y axis limits
# plt.title('Temperature from model',fontsize = 30)
# # plt.clim(1,8.5) # to set the colour bar limits
# cb.ax.tick_params(labelsize = 35)
# plt.tick_params(labelsize=35)
# plt.xlabel('Time counter',fontsize = 20)
# plt.ylabel('Depth',fontsize = 20)



plt.show()
###############################################




# ##########################################################
# ### testing with variable salinity:
# # get the data
#
# # see the depth variable
# depth = fh4.variables['deptht'][:]
# #print(depth)
#
# ### was testing the inverting of a numpy array by making it a list and then converting it back to a numpy array.
# #transpose depth variable for plotting
# #depth = depth.tolist()
# #print(len(depth))
# #depth = depth[::-1] # reverses the data
# #depth = np.array(depth)
# # print(type(depth.shape))
# # print(depth.shape[0])
#
#
# # see the salinity variable
# salinity = fh4.variables['vosaline'][:]
#
# #print(salinity)         # all the data
# #print(type(salinity))   # type of data
# #print(salinity.shape)   # size of data, the four numbers are the absolute dimensions then the objects dimensions in the array
# #print(salinity[0,74,2,2])# the absolute last entry in the entire array(of arrays)
#
# # testing t plot multiple values at one point in time
# # get the data, first entry in every block
# salinity_data = salinity[0,:,0,0]
# #print(data)
# print(salinity_data.shape)
# print(depth.shape)
# fig1 = plt.figure()
# plt.gca().invert_yaxis() # inverts tha depth axis
# plt.plot(salinity_data[0:38],depth[0:38])
# # note that fig1.show will pop the figure and close it afterwards if there is no plt.show at the end of the code
# fig1.show()
#
# fig2 = plt.figure()
# plt.plot(salinity_data[0:50],depth[0:50])
# fig2.show()
#
# plt.show()
#
#
#
# ##########################################################

# ###############################
# #plot for the initial conditions
#
# # get the depth variable for the plots
# init_depth = fh4.variables['deptht'][:]
#
# ### temperature
# # get the temperature variable
# init_cond_temp = fh4.variables['votemper'][:]
# # get the data, being the first value of each matrix entry in the numpy array
# init_cond_temp_data = init_cond_temp[0,:,1,1]
#
# # for testing the dimensions, must be the same
# # print(init_cond_temp_data.shape)
# # print(init_depth.shape)
#
# init_temp_plot = plt.figure()
# plt.gca().invert_yaxis() # inverts tha depth axis
# plt.plot(init_cond_temp_data[0:39],init_depth[0:39])
# # note that fig1.show will pop the figure and close it afterwards if there is no plt.show at the end of the code
# plt.title('Temperature initial condition used in 1d_PAPA',fontsize = 30)
# plt.xlabel('Temperature',fontsize = 20)
# plt.ylabel('Depth',fontsize = 20)
#
# init_temp_plot.show()
#
# ### salinity
# # get the salinity variable
# init_cond_salinity = fh4.variables['vosaline'][:]
# # get the data, being the first value of each matrix entry in the numpy array
# init_cond_salinity_data = init_cond_salinity[0,:,1,1]
#
# # for testing the dimensions, must be the same
# # print(init_cond_salinity_data.shape)
# # print(init_depth.shape)
#
# init_salinity_plot = plt.figure()
# plt.gca().invert_yaxis() # inverts the depth axis
# plt.plot(init_cond_salinity_data[0:39],init_depth[0:39])
# # note that fig1.show will pop the figure and close it afterwards if there is no plt.show at the end of the code
# plt.title('Salinity initial condition used in 1d_PAPA',fontsize = 30)
# plt.xlabel('Salinity',fontsize = 20)
# plt.ylabel('Depth',fontsize = 20)
#
# init_salinity_plot.show()
#
# # to show all the plots
# # plt.show()
# ###############################
#
#
# # ##########################################################
# # # testing the data from NEMO T,U,V,W files
# # # create the temp and salinity variables
# # ttemp = fh5.variables['votemper'][:]
# # tsal = fh5.variables['vosaline'][:]
# # # print(ttemp)
# # time = fh8.variables['time_counter'][:]
# # # print(np.diff(time))
# # tke = fh8.variables['votkeavt'][:]
# # print(tke[2,1,:,:])
# # ##########################################################
#
# ###############################
# # figured out the code uses the k-eps CLOSURE scheme from the ocean.output and namelist_ref files, search for closure
# # plotting of the temeperature and salinity graphs using the k-eps closure scheme
#
# ke_time = fh5.variables['time_counter'][:]  # time steps(in seconds)
# ke_depth = fh5.variables['deptht'][:]       # depths
# ke_temp = fh5.variables['votemper'][:]      # temperature
# ke_s_temp = fh5.variables['sosstsst'][:]    # sea surface temperature
# ke_salinity = fh5.variables['vosaline'][:]  # salinity
# ke_s_salinity = fh5.variables['sosaline'][:]# sea surface salinity
#
# # testing variables
# # print(ke_depth)
# # print(ke_temp[0:3,:,1,1])
#
# # get the data needed (MAIN DATA FOR ALL CALCULATIONS)
# # take the middle value of the 3x3 matrix layer for all the 75 layers and for all the time stamps, now I have a huge array with each entry as a time step that has a 75 element array indicating the number of levels that hold the values of the middle element of the mesh per level.
# ke_temp_data = ke_temp[:,:,1,1]
# ke_salinity_data = ke_salinity[:,:,1,1]
#
# ke_salinity_plot = plt.figure() # create the figure
# # for some reason it wants all the dimensions to be square, so plot everything up to 75
# # plt.pcolormesh(ke_time[0:75],ke_depth[0:75],ke_salinity_data[0:75,:])
# plt.pcolormesh(ke_time,ke_depth,ke_salinity_data.T) # need to transpose the matrix data! then all is good
#
# ke_salinity_plot.show()
# plt.colorbar()
# plt.title('Salinity from model',fontsize = 30)
# plt.xlabel('Time',fontsize = 20)
# plt.ylabel('Depth',fontsize = 20)
# # print(ke_salinity_data[0:2,:])
# # plt.show()
# ###############################
#
#
# # # ##########################################################
# # # testing the observed data from PAPA
# # # get temp
# # ttemper = fh11.variables['T_20'][:]
# # # print(ttemper.shape)
# # # print(ttemper)
# # # print(fh10)
# #
# # # original data
# # tsali = fh10.variables['S_41'][:]
# # print('hello')
# # print(tsali.shape)
# # # print(tsali)
# # tdep = fh10.variables['depth'][:]
# # print(tdep.shape)
# # # print(tdep)
# # print(ke_depth.shape)
# # print(ke_salinity.shape)
# # # print(ke_depth)
# #
# # # try reconcile the data from real and observed for salinity...
# # # check to see dimensions
# #
# # print(ke_depth)
# # print(tdep)
# #
# #
# # # to match the values for the depths
# # mapindexsalinity = [1,8,11,13,14,15,17,19,22,24,25,28,30]
# # # mapindexsalinity = mapindexsalinity[::-1]
# # print(mapindexsalinity)
# # # now pull out the values for these indexes
# # # data for the computed case:
# # data_computed_salinity = ke_salinity_data[0:364,:]
# # print(data_computed_salinity.shape)
# # # keep the indexed values only
# #
# # # get the initial array and then make it bigger
# # the_data = np.take( data_computed_salinity[0,:], mapindexsalinity)
# # # # testing dimensions and concatenation
# # # print(the_data)
# # # print(the_data.shape)
# # # the_data = np.concatenate([[the_data],[the_data]])
# # # # print(the_data)
# # # print(the_data.shape)
# # # the_data = np.concatenate([[the_data],[the_data]])
# # # print(the_data.shape)
# #
# # use = []
# # for t in range(0,364):
# #     useme = np.take(data_computed_salinity[t,:],mapindexsalinity)
# #     # print('S',useme.shape)
# #     useme = useme.tolist()
# #
# #     use.append(useme)
# #
# #     if t ==363: print(use)
# # use = np.array(use)
# # print(use.shape)
# #
# # # to find the mapping index for the temperature
# # tdeptemp = fh11.variables['depth'][:]
# # # print(tdeptemp)
# # # print(ke_depth)
# # mapindextemperature = [1,4,8,9,10,11,13,14,15,17,19,21,24,25,27,29,30,34]
# # # ##########################################################
#
# ###############################
# # this is for the biases of salinity and temperature
# # this involves subtracting the observed and computed data
# # the computed data must first be resized to fit the observed data
# # then everything must be plotted
#
# # get the time variable:
# bias_time = fh10.variables['time'][:] # use the salinity time as it has 364 time points which is the same as dimensions needed
# # print(bias_time)
# # print(bias_time.shape)
#
# # get the depths for salinity and temperature that will be used for all calculations
# obs_s_depth = fh10.variables['depth'][:]
# obs_t_depth = fh11.variables['depth'][:]
# # print('obs_s_depth dim: ',obs_s_depth.shape)
# # print('obs_t_depth dim: ',obs_t_depth.shape)
#
# # after mapping the depths for the computed data and the observed data the closest values were compared to the depths of each and the indexes from the computed values were taken and are given:
# # print(ke_depth)
# # print(obs_s_depth)
# # print(obs_t_depth)
# mapindexsalinity = [1,8,11,13,14,15,17,19,22,24,25,28,30]
# mapindextemperature = [1,4,8,9,10,11,13,14,15,17,19,21,24,25,27,29,30,34]
#
# # get data and redimension to 364,15 for salinity and 364,18 for temperature
# # get the observed data
# obs_sal = fh10.variables['S_41'][:]
# obs_temp = fh11.variables['T_20'][:]
# # print('obs_sal dim: ',obs_sal.shape)
# # print('obs_temp dim: ',obs_temp.shape)
# # redimension and reshape because it will contain 4 dimensions if not reshaped and cause havoc when subtracting the computed values:
# obs_sal = obs_sal[0:364,:].reshape(364,13)
# obs_temp = obs_temp[0:364,:].reshape(364,18)
# # print('rdim sal data: ',obs_sal.shape)
# # print('rdim temp data: ',obs_temp.shape)
#
# # get the computed data
# com_sal_data = ke_salinity_data
# com_tem_data = ke_temp_data
# # print('com_sal_data dim: ',com_sal_data.shape)
# # print('com_tem_data dim: ',com_tem_data.shape)
#
# # resize the computed data
# # run through timesteps (up to 364) and then pull out the indexed values, convert to list and append on and reconvert to numpy array.
# usefortemp = []
# useforsal = []
# for t in range(0,364):
#     usemesal = np.take(com_sal_data[t,:],mapindexsalinity)
#     usemetemp = np.take(com_tem_data[t,:],mapindextemperature)
#     # print('dims: S:',usemesal.shape,'T: ',usemetemp.shape) # see if dimensions is right
#
#     usemesal = usemesal.tolist() # convert to list
#     usemetemp = usemetemp.tolist()
#
#     useforsal.append(usemesal)  # append on
#     usefortemp.append(usemetemp)
#     # if t == 363: print(usemesal,usemetemp) # testing last entry
# com_sal_data = np.array(useforsal) # reconvert to numpy array with the same name
# com_tem_data = np.array(usefortemp)
# # print('rdim com_sal_data: ',com_sal_data.shape)
# # print('rdim com_tem_data: ',com_tem_data.shape)
#
# #subtract the observed from the computed data
# biases_salinity = np.subtract(com_sal_data,obs_sal)
# biases_temperature = np.subtract(com_tem_data,obs_temp)
# # print('bias sal dim: ',biases_salinity.shape)
# # print('bias temp dim: ',biases_temperature.shape)
#
# #plot the data
# bias_salinity_plot = plt.figure()
# plt.pcolormesh(bias_time,obs_s_depth,biases_salinity.T) # need to transpose the matrix data! then all is good
# bias_salinity_plot.show()
# cb = plt.colorbar()
# cb.ax.tick_params(labelsize = 35)
# plt.clim(-.25,.25) # to set the colour bar limits
# plt.gca().invert_yaxis() # inverts the depth axis
# # plt.title('Salinity bias',fontsize = 30)
# plt.xlabel('Time(days)',fontsize = 35)
# plt.ylabel('Depth',fontsize = 35)
# pylab.ylim([150,0]) # set the y axis limits
# plt.tick_params(labelsize=35)
# plt.set_cmap('gray') # set the plot to grayscale for SASAS paper
#
#
# bias_temperature_plot = plt.figure()
# plt.pcolormesh(bias_time,obs_t_depth,biases_temperature.T) # need to transpose the matrix data! then all is good
# bias_temperature_plot.show()
# cb = plt.colorbar()
# cb.ax.tick_params(labelsize = 35)
# plt.clim(-2.5,2.5) # to set the colour bar limits
# plt.gca().invert_yaxis() # inverts the depth axis
# # plt.title('Temperature bias',fontsize = 30)
# plt.xlabel('Time(days)',fontsize = 35)
# plt.ylabel('Depth',fontsize = 35)
# pylab.ylim([150,0]) # set the y axis limits
# plt.tick_params(labelsize=35)
# plt.set_cmap('gray') # set the plot to grayscale for SASAS paper
#
#
# # a sentimental note, James and me were plotting these graphs together
# # plt.show()
# ###############################
#
# # # # ##########################################################
# #
# # # now testing the density equations fopund at:
# # # get the data
# # rho = fh9.variables['rhop'][:]
# # print(rho[0,0,1,1])
# # # print(ke_depth.shape)
# # print(rho.shape)
# # rho1 = fh12.variables['STH_71'][:]
# # print(rho1.shape)
# # print(rho1[0,0])
# # print(ke_temp_data[0,0],ke_salinity_data[0,0])
# # # the starting and ending period is from 15/06/2010  to 14/06/2011
# # # the observation point for the density is the 12/09/2010
# # # and so there is 89 days from the starting date
# # # now I just have to get out that index and plot it for all those values
# #
# #
# # a =ke_temp_data[88,0]
# # b = ke_salinity_data[88,0]
# # c = (.824493 - .0040899*a + .000076438*a**2 - .00000082467*a**3 + .0000000053875*a**4)*b + (-.00572466 + .00010227*a - .0000016546*a**2)*b**1.5 + (.00048314)*b
# # print(c)
# #
# # # test to see if I can multiply an array with constant to all elements
# # d = np.array([1,2,3])*3
# # print(d)
# # # # ##########################################################
#
#
# ###############################
# # this is for the density plots
# # there is original data and computed data.
# # the original is from PAPA
# # and the computed is from using a source from the internet: http://ocean.stanford.edu/courses/bomc/chem/lecture_03.pdf
# # this source uses temperature and salinity to calculate the densities.
#
# #using an online conversion tool for converting months into days I found that we need the 89 day for september and 119 for october. The indexes that correspond to these days are 88 and 118 respectively.
#
#
# # get the computed data: we use ke_salinity_data and ke_temp_data and ke_depth (for both sept and oct)
# # get the observed data
# obs_den_sept = fh12.variables['STH_71'][:]
# obs_den_oct = fh13.variables['STH_71'][:]
# obs_den_depth_sept = fh12.variables['depth'][:]
# obs_den_depth_oct = fh13.variables['depth'][:]
# # print('obs_den_sept: ',obs_den_sept.shape)
# # print('obs_den_oct: ',obs_den_oct.shape)
# # print('obs_den_depth_sept: ',obs_den_depth_sept.shape)
# # print('obs_den_depth_oct: ',obs_den_depth_oct.shape)
#
#
# ke_temp_data_sept = ke_temp_data[88,:]
# ke_temp_data_oct = ke_temp_data[118,:]
# ke_salinity_data_sept = ke_salinity_data[88,:]
# ke_salinity_data_oct = ke_salinity_data[118,:]
# # print('ke_temp_data_sept',ke_temp_data_sept.shape)
# # print('ke_temp_data_oct',ke_temp_data_oct.shape)
# # print('ke_salinity_data_sept',ke_salinity_data_sept.shape)
# # print('ke_salinity_data_oct',ke_salinity_data_oct.shape)
#
# # now calculate the densities:
# com_den_data_sept = (.824493 - .0040899*ke_temp_data_sept + .000076438*ke_temp_data_sept**2 - .00000082467*ke_temp_data_sept**3 + .0000000053875*ke_temp_data_sept**4)*ke_salinity_data_sept + (-.00572466 + .00010227*ke_temp_data_sept - .0000016546*ke_temp_data_sept**2)*ke_salinity_data_sept**1.5 + (.00048314)*ke_salinity_data_sept
# com_den_data_oct = (.824493 - .0040899*ke_temp_data_oct + .000076438*ke_temp_data_oct**2 - .00000082467*ke_temp_data_oct**3 + .0000000053875*ke_temp_data_oct**4)*ke_salinity_data_oct + (-.00572466 + .00010227*ke_temp_data_oct - .0000016546*ke_temp_data_oct**2)*ke_salinity_data_oct**1.5 + (.00048314)*ke_salinity_data_oct
# # print('com_den_data_sept: ',com_den_data_sept.shape)
# # print('com_den_data_oct: ',com_den_data_oct.shape)
# # print('ke_depth: ',ke_depth.shape)
# # print(com_den_data_sept)
# # print(ke_depth)
#
#
# # plot the figures
# # first plot
# density_sept_plot = plt.figure()
# # need to plot two plots and use the label keyword for the legend, also because the array obs_den_sept is a (1,13,1,1) you need to tell python to use the [0,:,0,0] array, or you get an error
# plt.plot(com_den_data_sept,ke_depth,'ro-',label='calculated density',linewidth = 2.5,mew = 2,ms=10)
# plt.plot(obs_den_sept[0,:,0,0], obs_den_depth_sept,'b-',label='observed density',linewidth = 2.5)
# density_sept_plot.show()
# plt.legend(fontsize=25) # to show the legend
# plt.gca().invert_yaxis() # inverts the depth axis
# # plt.title('Density for September',fontsize = 30)
# plt.xlabel('Density',fontsize = 35)
# plt.ylabel('Depth',fontsize = 35)
# pylab.ylim([125,0]) # set the y axis limits
# pylab.xlim([24,27])
# plt.tick_params(labelsize=35)
#
# # second plot
# density_oct_plot = plt.figure()
# # need to plot two plots and use the label keyword for the legend, also because the array obs_den_sept is a (1,13,1,1) you need to tell python to use the [0,:,0,0] array, or you get an error
# plt.plot(com_den_data_oct,ke_depth,'ro-',label='calculated density',linewidth = 2.5,mew = 2,ms = 10)
# plt.plot(obs_den_oct[0,:,0,0], obs_den_depth_oct,'b-',label='observed density',linewidth = 2.5)
# density_oct_plot.show()
# plt.legend(fontsize=25) # to show the legend
# plt.gca().invert_yaxis() # inverts the depth axis
# # plt.title('Density for October',fontsize = 30)
# plt.xlabel('Density',fontsize = 35)
# plt.ylabel('Depth',fontsize = 35)
# pylab.ylim([150,0]) # set the y axis limits
# pylab.xlim([24,27])
# plt.tick_params(labelsize=35) # change the size of axes
#
#
# # plt.show()
# ###############################
#
# # # # ##########################################################
# # this id for testing the RMSE calculations
#
# # # # ##########################################################
#
#
# ###############################
# # this part is to calculate the RMSE values
# # this is the link I used to calculate the RMSE's: http://stackoverflow.com/questions/26237688/rmse-root-mean-square-deviation-calculation-in-r
# # the formula is: RMSE = sqrt(mean((computed-observed)**2))
# # can only do this for the temperatures, as there is only a graph for temperatures
#
# # print('obs_temp dim: ',obs_temp.shape,'com_tem_data dim: ',com_tem_data.shape) # see the dimensions
#
# # get the difference and then square it:
# RMSE = (obs_temp-com_tem_data)**2
# # print(RMSE)
# print(RMSE.shape)
#
# # from the above data, the forth value for each time step seems to be blowing up, I am omitting this line further more
# # delete the entries:
# trmse = []
# for t in range(RMSE.shape[0]):
#     toappend = np.delete(RMSE[t,:],3,axis=0)
#     trmse.append(toappend)
# RMSE = np.array(trmse)
# # print(RMSE.shape)
# # print(RMSE[0,:]) # test to see if there are still large vales:
#
# # get the means:
# RMSE = np.mean(RMSE,axis=1)
# # print(RMSE)
# # print(RMSE.shape)
#
# # now get sqrt:
# RMSE = RMSE**(.5)
# # print(RMSE.shape)
#
#
# # now plot the data:
# temp_RMSE_plot = plt.figure()
# # Use the bias time because of dimensions, which are the same as RMSE dimensions
# plt.plot(bias_time[0:350],RMSE[0:350],'r-',label='computed',linewidth = 2.5)
# temp_RMSE_plot.show()
# # plt.title('RMSE for temperture k-eps',fontsize = 30)
# plt.xlabel('Time(days)',fontsize = 35)
# plt.ylabel('Temperature RMSE',fontsize = 35)
# # pylab.ylim([0,0.5]) # set the y axis limits
# plt.tick_params(labelsize=35)
# plt.axhline(y=0.15,linewidth = 2.5) # to draw the horizontal line
#
#
# plt.show() # show all plots
# ###############################
