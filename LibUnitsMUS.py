# -*- coding: utf-8 -*-
"""
Created on Thu May 16 17:26:23 2019

@author: VACALDER
"""

# Define Units
#-------------------------------------------
import math
inch=1.0                          # define basic units
sec=1.0
kip=1.0
rad=1.0
LunitTXT="Inches"              # define basic-unit text for output
FunitTXT="Kips"                  
TunitTXT="Seconds"                 

ft=inch*12.0             # define dependent units
lbf=kip/1000.0
ksi=kip/(inch**2)
psi=lbf/(inch**2)
in2=inch*inch

m=inch*39.3701           # define metric basic units
N=kip*2.2481e-4

mm=m/1000.0            # define dependent units
cm=m/100.0
MPa=N/(mm**2.0)
Pa=MPa/1000.0
GPa=MPa*1000.0
kN=N*1000.0
mm2=mm**2.0;                          # define basic units
m2=m*m
PI=2*math.asin(1.0)         # define constants
g=9.81*m/(sec**2.0)
deg=rad/180.0*PI

U=1e10                        # a really large number
u=1/U                 # a really small number mm];