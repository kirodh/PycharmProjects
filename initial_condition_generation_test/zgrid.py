# 21 July 2016 Kirodh Boodhraj
# this function creates the grid, z-levels, for the C1D_PAPA case, This code was translated from Marcello's Matlab code.

# imports:
import math
import numpy as np

# testing, ignore this
# how to assign nan 2x ways
# x = float('nan')
# print(math.isnan(x))
# y = np.nan
# print(math.isnan(y))

# how to use function
# Some variables explained:
# ppkth shifts the point of concavity to the number of leves you want it to be at
# ppacr horizontally stretches the tanh function which causes more or less levels in the initial depth of ocean
# jpk is the number of levels, make it odd because NEMO doesnt use the last level which is in the ground.
# ppdzmin is the minimum spacing you can have n=between levels, keep this at 1
# pphmax is the maximum depth you have (depth of your ocean at that point)
# ldbletanh is to turn on/off the double hyperbolic tangent function (used for refining mesh near the floor of the ocean)
# ppa2,ppkth2,ppacr2 are associated with the double hyperbolic tangent functionality


# default parameters for C1D_PAPA are in the function definition input parameters
def zgrid(jpk=75, ppsur=-3958.951371276829, ppa0=103.9530096000000, ppa1=2.415951269000000, ppkth=15.3510137, ppacr=7.0,
          ppdzmin=np.nan, pphmax=np.nan, ldbletanh=1, ppa2=100.7609285, ppkth2=48.02989372, ppacr2=13.0):
    #  ----------------------------------------------------------------------
    #                     ***  ROUTINE zgr_z  ***
    #  
    #   ** Purpose :   set the depth of model levels and the resulting
    #        vertical scale factors.
    #  
    #   ** Method  :   z-coordinate system (use in all type of coordinate)
    #          The depth of model levels is defined from an analytical
    #        function the derivative of which gives the scale factors.
    #          both depth and scale factors only depend on k (1d arrays).
    #                w-level: gdepw_1d  = gdep(k)
    #                         e3w_1d(k) = dk(gdep)(k)     = e3(k)
    #                t-level: gdept_1d  = gdep(k+0.5)
    #                         e3t_1d(k) = dk(gdep)(k+0.5) = e3(k+0.5)
    #  
    #   ** Action  : - gdept_1d, gdepw_1d : depth of T- and W-point (m)
    #                - e3t_1d  , e3w_1d   : scale factors at T- and W-levels (m)
    #  
    #   Reference : Marti, Madec & Delecluse, 1992, JGR, 97, No8, 12,763-12,766.
    #               Marcello, translated their fortran code into Matlab code
    #  ----------------------------------------------------------------------

    # initialize
    gdept_1d = np.empty((jpk, 1));  # make the arrays, set them all to the same values: nan's
    gdept_1d[:] = np.NAN
    e3t_1d = gdept_1d;
    gdepw_1d = gdept_1d;
    e3w_1d = gdept_1d;

    zkth = ppkth;
    zacr = ppacr; # amount of stretching
    zdzmin = ppdzmin;
    zhmax = pphmax;
    zkth2 = ppkth2;
    zacr2 = ppacr2;  # optional double tanh parameters
    jpkm1 = jpk - 1;

    # If ppa1 and ppa0 and ppsur are equal to pp_to_be_computed
    #  za0, za1, zsur are computed from ppdzmin , pphmax, ppkth, ppacr
    if (np.isnan(ppa1) and np.isnan(ppa0) and np.isnan(ppsur)):
        za1 = (ppdzmin - pphmax / float(jpkm1)) / (math.tanh((1 - ppkth) / ppacr) - ppacr / float(jpk - 1) * (
            math.log(math.cosh((jpk - ppkth) / ppacr)) - math.log(math.cosh((1 - ppkth) / ppacr))));
        za0 = ppdzmin - za1 * math.tanh((1 - ppkth) / ppacr);
        zsur = - za0 - za1 * ppacr * math.log(math.cosh((1 - ppkth) / ppacr));
        print("came in here\n")
    else:
        za1 = ppa1; #
        za0 = ppa0;
        zsur = ppsur; # z at surface
        za2 = ppa2;  # optional (ldbletanh=T) double tanh parameter

    print('    zgr_z   : Reference vertical z-coordinates')
    print('    ~~~~~~~')
    if (ppkth == 0):
        print("            Uniform grid with " + str(jpk - 1) + " layers")
        print("            Total depth    :" + str(zhmax))
        print("            Layer thickness:" + str(zhmax / (jpk - 1)))
    else:
        if (ppa1 == 0 and ppa0 == 0 and ppsur == 0):
            print("         zsur, za0, za1 computed from ")
            print("                 zdzmin = " + str(zdzmin))
            print("                 zhmax  = " + str(zhmax))

        print('           Value of coefficients for vertical mesh:')
        print(['                 zsur = ', str(zsur)])
        print(['                 za0  = ', str(za0)])
        print(['                 za1  = ', str(za1)])
        print(['                 zkth = ', str(zkth)])
        print(['                 zacr = ', str(zacr)])
        if (ldbletanh):
            print(" (Double tanh    za2  = " + str(za2))
            print("  parameters)    zkth2= " + str(zkth2))
            print("                 zacr2= " + str(zacr2))

    # Reference z-coordinate (depth - scale factor at T- and W-points)
    #  ======================
    if (ppkth == 0):  # uniform vertical grid
        za1 = zhmax / float(jpk - 1);
        for jk in range(0, jpk):
            zw = float(jk);
            zt = float(jk) + 0.5;
            gdepw_1d[jk] = (zw - 1) * za1;
            gdept_1d[jk] = (zt - 1) * za1;
            e3w_1d[jk] = za1;
            e3t_1d[jk] = za1;

    else:  # Madec & Imbard 1996 function
        if (not ldbletanh):
            for jk in range(0, jpk):
                zw = float(jk);
                zt = float(jk) + 0.5;
                gdepw_1d[jk] = (zsur + za0 * zw + za1 * zacr * math.log(math.cosh((zw - zkth) / zacr)));
                gdept_1d[jk] = (zsur + za0 * zt + za1 * zacr * math.log(math.cosh((zt - zkth) / zacr)));
                e3w_1d[jk] = za0 + za1 * math.tanh((zw - zkth) / zacr);
                e3t_1d[jk] = za0 + za1 * math.tanh((zt - zkth) / zacr);

        else:
            for jk in range(0, jpk):
                zw = float(jk);
                zt = float(jk) + 0.5;
                # Double tanh function
                gdepw_1d[jk] = (
                    zsur + za0 * zw + za1 * zacr * math.log(math.cosh((zw - zkth) / zacr)) + za2 * zacr2 * math.log(
                        math.cosh((zw - zkth2) / zacr2)));
                gdept_1d[jk] = (
                    zsur + za0 * zt + za1 * zacr * math.log(math.cosh((zt - zkth) / zacr)) + za2 * zacr2 * math.log(
                        math.cosh((zt - zkth2) / zacr2)));
                e3w_1d[jk] = za0 + za1 * math.tanh((zw - zkth) / zacr) + za2 * math.tanh((zw - zkth2) / zacr2);
                e3t_1d[jk] = za0 + za1 * math.tanh((zt - zkth) / zacr) + za2 * math.tanh((zt - zkth2) / zacr2);

        gdepw_1d[0] = 5.14695644e-01;  # force first w-level to be exactly at zero

    return [gdept_1d, e3t_1d, gdepw_1d, e3w_1d]  # dep is actualspace between depths depths, and e3 denotes the spacing between levels
