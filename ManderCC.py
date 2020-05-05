# -*- coding: utf-8 -*-
"""
Created on Thu May 16 17:35:29 2019

@author: VACALDER
"""

def ManderCC(fpc,Ah,fyh,Dprime,S):
    import LibUnitsMUS
    import math
    roV=4*Ah/(Dprime*S)    #   Volumetric ratio of steel
    fl=2*fyh*Ah/(Dprime*S) #   Lateral confining pressure of steel
    
    # Determine Peak Stress and Strain Parameters
    fcc=fpc*(2.254*math.sqrt(1.+7.94*fl/fpc)-2*fl/fpc-1.254)  #   Maximum confined concrete stress
    ecc=0.002*(1 + 5*(fcc/fpc - 1))   #   Strain at maximum stress
    # Determine Ultimate Stress and Strain Parameters
    # Assume ultimate tensile strain in steel = 0.09
    Esec=fcc/ecc                         #   Secant Stiffness
    Ec=60000*math.sqrt(fpc/LibUnitsMUS.psi)*LibUnitsMUS.psi;         #   Modulus of concrete
    r=Ec/(Ec - Esec)
    ecu=0.004 + 1.4*roV*fyh*0.09/fcc  #   Strain at rupture of steel
    fcu=(fcc*(ecu/ecc))*r /(r - 1 + (ecu/ecc)**r)  #   Stress at rupture of steel
    # Set all of the calculated values to negative
    FCC=-fcc
    ECC=-ecc
    FCU=-fcu
    ECU=-ecu
       
    return FCC, ECC, FCU, ECU;