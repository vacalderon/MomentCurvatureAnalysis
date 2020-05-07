# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 15:12:06 2019

@author: pchi893
"""

from openseespy.opensees import *
import math
import numpy as np
import matplotlib.pyplot as plt
from LibUnitsMUS import *
import ManderCC
from __main__ import *


def MomentCurvature_RC_Column(dbi, dti, reduced_yield_Longitudinal, dblc, cover, Ablc, reduced_yield_Transverse, Atc, dbtc, datadir, PCol, DCol, concrete_strength):
    wipe()

    # Define model builder
    # --------------------
    model('basic', '-ndm', 2, '-ndf', 3)

    # Structure GEOMETRY -------------------------------------------------------------
    # Define two nodes at (0,0)
    node(1, 0.0, 0.0)
    node(2, 0.0, 0.0)

    # Fix all degrees of freedom except axial and bending
    fix(1, 1, 1, 1)
    fix(2, 0, 1, 0)

    # MATERIAL parameters
    IDconcC = 1  # material ID tag -- confined cover concrete
    IDconcU = 2  # material ID tag -- unconfined cover concrete
    IDreinf = 3  # material ID tag -- reinforcement

    # ------------------------------------------
    # Define materials for nonlinear columns
    # ------------------------------------------
    # Longitudinal steel properties
    Fy = reduced_yield_Longitudinal  # STEEL yield stress
    Fu = 1.375 * Fy  # Steel Ultimate Stress
    Es = 29000.0 * ksi  # modulus of steel
    Bs = 0.012  # strain-hardening ratio
    R0 = 20.0  # control the transition from elastic to plastic branches
    cR1 = 0.90  # control the transition from elastic to plastic branches
    cR2 = 0.08  # control the transition from elastic to plastic branches
    a1 = 0.039
    a2 = 1
    a3 = 0.029
    a4 = 1.0
    c = cover * cm  # Column cover to reinforcing steel NA.
    numBarsSec = 16  # number of uniformly-distributed longitudinal-reinforcement bars
    barAreaSec = Ablc * mm2  # area of longitudinal-reinforcement bars
    dbl = dblc * mm

    # Transverse Steel Properties
    fyt = reduced_yield_Transverse  # Yield Stress of Transverse Steel
    Ast = Atc * mm2  # Area of transverse steel
    dbt = dbtc * mm  # Diameter of transverse steel
    st = 2.0 * inch  # Spacing of spiral
    Dprime = DCol - 2 * c - dti * 0.5  # Inner core diameter
    # print('Dprime= ',Dprime)
    Rbl = Dprime * 0.5 - dti * 0.5 - dbi * 0.5  # Location of longitudinal bar
    # print('Rbl =', Rbl)

    # nominal concrete compressive strength
    fpc = concrete_strength  # CONCRETE Compressive Strength, ksi   (+Tension, -Compression)
    Ec = 57.0 * ksi * math.sqrt(fpc / psi)  # Concrete Elastic Modulus

    # unconfined concrete
    fc1U = -fpc;  # UNCONFINED concrete (todeschini parabolic model), maximum stress
    eps1U = -0.003  # strain at maximum strength of unconfined concrete
    fc2U = 0.2 * fc1U  # ultimate stress
    eps2U = -0.01  # strain at ultimate stress
    lambdac = 0.1  # ratio between unloading slope at $eps2 and initial slope $Ec

    mand = ManderCC.ManderCC(fpc, Ast, fyt, Dprime, st)

    fc = mand[0]
    eps1 = mand[1]
    fc2 = mand[2]
    eps2 = mand[3]

    # CONCRETE                  tag   f'c        ec0   f'cu        ecu
    # Core concrete (confined)
    uniaxialMaterial('Concrete01', IDconcC, fc, eps1, fc2, eps2)

    # Cover concrete (unconfined)
    uniaxialMaterial('Concrete01', IDconcU, fc1U, eps1U, fc2U, eps2U)

    # STEEL
    # Reinforcing steel
    params = [R0, cR1, cR2]
    #                        tag  fy E0    b
    uniaxialMaterial('Steel02', IDreinf, Fy, Es, Bs, R0, cR1, cR2)

    # Define cross-section for nonlinear columns
    # ------------------------------------------

    # set some paramaters
    SecTag1 = 1
    ri = 0.0
    ro = DCol / 2.0
    nfCoreR = 8
    nfCoreT = 8
    nfCoverR = 2
    nfCoverT = 8
    rc = ro - c
    theta = 360.0 / numBarsSec

    section('Fiber', SecTag1)

    # Create the concrete fibers
    patch('circ', 1, nfCoreT, nfCoreR, 0.0, 0.0, ri, rc, 0.0, 360.0)  # Define the core patch
    patch('circ', 2, nfCoverT, nfCoverR, 0.0, 0.0, rc, ro, 0.0, 360.0)  # Define Cover Patch

    # Create the reinforcing fibers
    layer('circ', 3, numBarsSec, barAreaSec, 0.0, 0.0, rc, theta, 360.0)

    # Define element
    #                             tag ndI ndJ  secTag
    element('zeroLengthSection', 1, 1, 2, SecTag1)

    # Create recorders

    recorder('Node', '-file', datadir + '/Mphi.out', '-time', '-node', 2, '-dof', 3, 'disp')
    recorder('Element', '-file', datadir + '/SteelStrain.out', '-time', '-ele', 1, 'section', 
             'fiber', str(Rbl) + ', 0.0', 'mat', '3', 'stressStrain')  # Rbl,0, IDreinf
    recorder('Element', '-file', datadir + '/CConcStrain.out', '-time', '-ele', 1, 'section', 
             'fiber', str(-Dprime) + ', 0.0', 'mat', '1', 'stressStrain')  # Rbl,0, IDreinf
    recorder('Element', '-file', datadir +'/UCConcStrain.out', '-time', '-ele', 1, 'section', 
             'fiber', str(-DCol) + '0.0', 'mat', '2', 'stressStrain')

    # Estimate yield curvature
    # (Assuming no axial load and only top and bottom steel)
    # d -- from cover to rebar
    # steel yield strain
    epsy = Fy / Es
    Ky = 2.25 * epsy / (DCol)

    # Print estimate to standard output
    print("Stimated yield curvature: ", Ky)

    # Target ductility for analysis
    mu = 15.0
    maxK =15*Ky
    # Number of analysis increments
    numIncr = 100

    # Define constant axial load
    timeSeries('Constant', 1)
    pattern('Plain', 1, 1)
    load(2, PCol, 0.0, 0.0)

    # Define analysis parameters
    integrator('LoadControl', 0.0)
    system('SparseGeneral', '-piv')
    test('NormUnbalance', 1e-9, 10)
    numberer('Plain')
    constraints('Plain')
    algorithm('Newton')
    analysis('Static')

    # Do one analysis for constant axial load
    analyze(1)

    # Define reference moment
    timeSeries('Linear', 2)
    pattern('Plain', 2, 2)
    load(2, 0.0, 0.0, 1.0)

    # Compute curvature increment
    dK = maxK / numIncr

    # Use displacement control at node 2 for section analysis
    integrator('DisplacementControl', 2, 3, dK, 1, dK, dK)

    # Do the section analysis
    analyze(numIncr)
