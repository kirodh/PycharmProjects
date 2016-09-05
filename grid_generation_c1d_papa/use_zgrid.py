# this script is to get a specific config for the spacing between the levels and then use these parameters in
# the nemo configuration namelist file to set the values of the grid variables and then run the simulation for
# different number of levels
from zgrid import zgrid
from pvert_grid import pvert_grid
import math
import numpy as np
from netCDF4 import Dataset as netcdffile
import matplotlib.pyplot as plt
import pylab



# what reffray used, use this to see the corresopndence between the depths and the spacings
# [a,b,c,d] = zgrid(75,-3958.951371276829, 103.9530096000000, 2.415951269000000, 15.3510137, 7.0,np.nan, np.nan, 1, 100.7609285, 48.02989372, 13.0)
# [a,b,c,d] = zgrid(51,np.nan,np.nan,np.nan,30.0,10.0,1.0,4000,0,np.nan,np.nan,np.nan)#,-3958.951371276829, 103.9530096000000, 2.415951269000000, 15.3510137, 7.0,np.nan, np.nan, 1, 100.7609285, 48.02989372, 13.0)


# # testing on 51 levels(use these values)
# [a,b,c,d] = zgrid(51,np.nan,np.nan,np.nan,30.0,6.0,1.0,4200,0,np.nan,np.nan,np.nan)#,-3958.951371276829, 103.9530096000000, 2.415951269000000, 15.3510137, 7.0,np.nan, np.nan, 1, 100.7609285, 48.02989372, 13.0)
# testing on 21 levels(use these values)
# [a,b,c,d] = zgrid(151,np.nan,np.nan,np.nan,100.0,20.0,1.0,4200,0,np.nan,np.nan,np.nan)#,-3958.951371276829, 103.9530096000000, 2.415951269000000, 15.3510137, 7.0,np.nan, np.nan, 1, 100.7609285, 48.02989372, 13.0)


# [a,b,c,d] = zgrid(151,np.nan,np.nan,np.nan,100.0,20.0,1.0,4200,0,np.nan,np.nan,np.nan)
[a,b,c,d] = zgrid(75,-3958.951371276829, 103.9530096000000, 2.415951269000000, 15.3510137, 7.0,np.nan, np.nan, 1, 100.7609285, 48.02989372, 13.0)
# plot the data:
# pvert_grid(a,0)


# pvert_grid(b,1)
# pvert_grid(c,0)
# pvert_grid(d,1)

# [A,B,C,D] = zgrid(75,np.nan,np.nan,np.nan,55.0,10.0,1.0,4200,0,np.nan,np.nan,np.nan)
# [A,B,C,D] = zgrid(51,np.nan,np.nan,np.nan,30,5,1.0,4200,0,np.nan,np.nan,np.nan)
# [A,B,C,D] = zgrid(101,np.nan,np.nan,np.nan,75,22,1.0,4200,0,np.nan,np.nan,np.nan)
[A,B,C,D] = zgrid(151,np.nan,np.nan,np.nan,116,36,1.0,4200,0,np.nan,np.nan,np.nan)
# plot the data:

pvert_grid(A,0)



plt.show()


# print(np.sum(a))
# print(a)

# print the depth values i.e. the cumalative sum
summ = 5.05760014e-01
for i in range(0,len(b)):
    print(summ)
    summ += a[i]

# print(c)


# data collection to 'try' fit a curve to the data got from changing levels
levels = [51,75,101,151]
concavity = [30,55,75,116]
stretch = [5,10,22,36]

plt.plot(concavity,stretch,"ro-")

plt.show()

