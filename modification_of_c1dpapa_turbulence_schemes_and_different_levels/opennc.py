# import the necessary modules:
from netCDF4 import Dataset as netcdffile

# this function reads a netcdf file (and prints the file header if wanted), use a 1 or 0 to print the header
# template to use:
# fh_temp = opennc("nc file name go here",1)
def opennc(nc_filename,disp):
    fh = netcdffile(nc_filename, mode='r')
    if disp:
        print(fh)
    return fh
