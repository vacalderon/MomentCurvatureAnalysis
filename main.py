# -*- coding: utf-8 -*-
"""
Created on Wed Aug 14 16:32:05 2019

@author: VACALDER
"""

# ------------------------------------------------------------------------------
# |     PROGRAM TO PERFORM TIME DEPENDENT PROPERTIES EFFECTS ON STRUCTURES     |
# |
# |
# |          Victor A Calderon
# |          PhD Student/ Research Assistant
# |          NC STATE UNIVERSITY
# |          2020 (c)
# |
# |
# ------------------------------------------------------------------------------


# ----------------------------------------------------------------------------
# |                             IMPORTS
# ----------------------------------------------------------------------------

# import the os module
import time

start_time = time.time()
import os
import math
import numpy as np
from LibUnitsMUS import *
import math
import MomentCurvature_RC_Column

# ----------------------------------------------------------------------------
# | VARIABLES THAT CHANGE WITH TIME
# ----------------------------------------------------------------------------
#
#
# *cover = Cover of concrete in cm
# *Tcorr = Time to corrosion in yrs
# *Time  = Different times that are being analyzed
# *wcr   = Water to cement ratio
# *dbi   = Initial longitudinal bar diameter
# *dti   = Initial transverse steel diameter
# *ALR   = Axial load ratio
# *rho_li= initial longitudinal steel ratio
# *tho_vi= initial transverse steel ratio

concrete_strength = 5.0 * ksi
steel_yield_strength = 60 * ksi
DCol = 2 * ft
Ag = 0.25*math.pi * DCol**2
iALR = [0.05, 0.1, 0.15, 0.20]
icover = [4., 5., 7.5]  # [4]  #
iTcorr = [1.1307, 1.7667, 3.975]  # [1.1307]  #
iTime = [5, 25, 50., 75.]
iwcr = [0.36, 0.42, 0.45, 0.50, 0.55] # [0.40]  #
dbi = 0.75
dti = 0.375

rootdir = r'C:\ConditionDepedentPBEE\Results\MomentCurvature_Results'

# ----------------------------------------------------------------------------
# |                             BATCH RUN
# ----------------------------------------------------------------------------
for ALR in iALR:
    PCol=Ag*concrete_strength*ALR
    i=-1
    for cover in icover:
        i = i + 1
        for Time in iTime:
            for wcr in iwcr:
                # set Functions for Fiber Model and NLTHA

                print ('cover is: ', cover, ' and Time is:', Time, 'and w/c: ', wcr)
                Tcorr = iTcorr[i]

                dblc = dbi * 25.4 - (((1.0508 * (1 - wcr) ** (-1.64)) / (cover * 10)) * (Time - Tcorr) ** 0.71)
                Ablc = 0.25 * math.pi * dblc ** 2
                Ablcm = Ablc / (1000. ** 2)
                Mcorr = Ablcm * 7800.
                CL_Longitudinal_Steel = (1 - Ablcm * 7800. / 2.223179) * 100
                yield_strength_reduction_Longitudinal= (1 - 0.021 * CL_Longitudinal_Steel)
                reduced_yield_Longitudinal=steel_yield_strength*yield_strength_reduction_Longitudinal

                dbtc = dti * 25.4 - (((1.0508 * (1 - wcr) ** (-1.64)) / (cover * 10)) * (Time - Tcorr) ** 0.71)
                Atc = 0.25 * math.pi * dbtc ** 2
                Atcm = Atc / (1000. ** 2)
                CL_Transverse_Steel = ((0.55795 - Atcm * 7800.) / 0.55795) * 100
                yield_strength_reduction_Transverse = (1 - 0.021 * CL_Transverse_Steel)
                reduced_yield_Transverse=steel_yield_strength*yield_strength_reduction_Transverse
                
                datadir = rootdir + "\\" + "data" + "\\ALR_" + str(int(ALR*100)) + "\\" + str(cover) + \
                          "\\" + str(wcr) + "\\" + str(Time)
                          
                if not os.path.exists(datadir):
                    os.makedirs(datadir)

                MomentCurvature_RC_Column.MomentCurvature_RC_Column(dbi, dti, reduced_yield_Longitudinal, dblc, cover, Ablc, 
                                          reduced_yield_Transverse, Atc, dbtc, datadir, PCol, DCol, concrete_strength)
                with open(datadir + "\\Conditions.out", 'w') as f:
                    f.write("%s %s %s %s %s %s \n" % (ALR, cover, Time, wcr, CL_Longitudinal_Steel,
                                                      CL_Transverse_Steel))
                f.close

print("ALL ANALYSIS COMPLETE")
print("--- %s minutes ---" % ((time.time() - start_time) / 60))

#                print('Tcorr = ',Tcorr)
#                print('Ablc  = ',Ablc)
#                print('Ablcm = ',Ablcm)
#                print('Mcorr = ',Mcorr)
#                print('CL_Longitudinal_Steel   = ',CL_Longitudinal_Steel )
#                print('dbtc  = ',dbtc)
#                print('Atc  = ',Atc)
#                print('Atcm = ',Atcm)
#                print('CL_Transverse_Steel   = ',CL_Transverse_Steel)