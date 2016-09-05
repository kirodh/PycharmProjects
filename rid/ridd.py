from netCDF4 import Dataset as netcdffile
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.basemap import Basemap
import pylab
from scipy import interpolate
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import griddata



a = np.mgrid[0:2,0:10:6j]

# print(a)

b = np.mgrid[0:1:100j, 0:1:200j]
# print(b)

c = np.mgrid[0:100:101j,0:200:201j]
# print(c)


# x = np.array([0,0])
# y = np.array([0,0])
# d = np.mgrid[0:2:3j,0:2:3j]
# print(d)
# def func(x, y):
#     return x*(1-x)*np.cos(4*np.pi*x) * np.sin(4*np.pi*y**2)**2

# z = np.array([20,30,40,50])


# f = interpolate.interp2d(x,y,z,kind="cubic")
x = [0,1,2,0,1,2];  y = [0,0,0,3,3,3]; z = [1,2,3,4,5,6]

f = interpolate.interp2d(x,y,z,kind="linear")

X = np.linspace(1,5,5)
Y = np.linspace(1,2,5)

aaa = griddata(X,Y,f(X,Y))

print(f(X,Y))

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X,Y,f(X,Y).T)
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')
print(aaa)

plt.show()
