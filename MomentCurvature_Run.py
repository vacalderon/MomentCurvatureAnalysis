# -*- coding: utf-8 -*-
"""
Created on Fri May 17 15:43:48 2019

@author: VACALDER
"""
from openseespy.opensees import *    
def MomentCurvature(secTag, axialLoad, maxK, numIncr=100):

    # Define two nodes at (0,0)
    node(1, 0.0, 0.0)
    node(2, 0.0, 0.0)

    # Fix all degrees of freedom except axial and bending
    fix(1, 1, 1, 1)
    fix(2, 0, 1, 0)
    
    # Define element
    #                             tag ndI ndJ  secTag
    element('zeroLengthSection',  1,   1,   2,  secTag)
    # Create recorder
    
    recorder('Node','-file','Mphi.out','-time','-node',2,'-dof',3,'disp')
    recorder('Element','-file','bar01.txt','-time','-ele', 1,'section','fiber', -9, 0.0,'stressStrain')
    recorder('Element','-file','ConcreteStrain21.txt','-time','-ele', 1, 'section', 'fiber', -12, 0.0, 'stressStrain'); #21
    recorder('Element','-file','ConcreteStrain22.txt','-time','-ele', 1, 'section', 'fiber', 12,  0.0 ,'stressStrain'); #21
    
    # Define constant axial load
    timeSeries('Constant', 1)
    pattern('Plain', 1, 1)
    load(2, axialLoad, 0.0, 0.0)

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
    pattern('Plain',2, 2)
    load(2, 0.0, 0.0, 1.0)

    # Compute curvature increment
    dK = maxK / numIncr

    # Use displacement control at node 2 for section analysis
    integrator('DisplacementControl', 2,3,dK,1,dK,dK)

    # Do the section analysis
    analyze(numIncr)