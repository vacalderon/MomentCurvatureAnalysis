
from openseespy.opensees import *
import math
import numpy as np
import matplotlib.pyplot as plt

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
    
    recorder('Node','-file','Mphi.out','-closeOnWrite','-time','-node',2,'-dof',3,'disp')
    recorder('Element','-file','bar01.txt','-closeOnWrite','-time','-ele', 1,'section', '2', 'fiber', '9','stressStrain')
    recorder('Element','-file','ConcreteStrain21.txt','-closeOnWrite','-time','-ele', 1, 'section', '1', 'fiber', [-12.0, 0.0], 'stressStrain'); #21
    recorder('Element','-file','ConcreteStrain22.txt','-closeOnWrite','-time','-ele', 1, 'section', '1', 'fiber', '12.0, 0.0', 'stressStrain'); #22
    
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


wipe()

print("Start MomentCurvature.py example")

from LibUnitsMUS import *
import ManderCC

# Define model builder
# --------------------
model('basic','-ndm',2,'-ndf',3)

# Structure GEOMETRY -------------------------------------------------------------
DCol=2.0*ft         # Column Diameter

# Define materials for nonlinear columns
# ------------------------------------------
#Longitudinal steel properties
Fy=60.0*ksi        # STEEL yield stress
Es=29000.0*ksi     # modulus of steel
Bs=0.01          # strain-hardening ratio 
R0=18.0            # control the transition from elastic to plastic branches
cR1=0.925        # control the transition from elastic to plastic branches
cR2=0.15         # control the transition from elastic to plastic branches
c=3.0*inch         # Column cover to reinforcing steel NA.
numBarsSec= 16   # number of uniformly-distributed longitudinal-reinforcement bars
barAreaSec= 0.44*in2  # area of longitudinal-reinforcement bars
dbl=0.75*inch    

# Transverse Steel Properties
fyt=60.0*ksi                 # Yield Stress of Transverse Steel
Ast=0.11*in2               # Area of transverse steel
dbt=0.375*inch             # Diameter of transverse steel
st=2.0*inch                  # Spacing of spiral
Dprime=DCol-2*c-dbt        # Inner core diameter
Rbl=Dprime*0.5-dbt-dbl*0.5 # Location of longitudinal bar

# nominal concrete compressive strength
fpc= 5.0*ksi       # CONCRETE Compressive Strength, ksi   (+Tension, -Compression)
Ec=57.0*ksi*math.sqrt(fpc/psi) # Concrete Elastic Modulus

# unconfined concrete
fc1U=-fpc;                 # UNCONFINED concrete (todeschini parabolic model), maximum stress
eps1U=-0.003               # strain at maximum strength of unconfined concrete
fc2U=0.2*fc1U              # ultimate stress
eps2U=-0.01                # strain at ultimate stress
lambdac=0.1                # ratio between unloading slope at $eps2 and initial slope $Ec


mand=ManderCC.ManderCC(fpc,Ast,fyt,Dprime,st)

fc=mand[0]
eps1=mand[1]
fc2=mand[2]
eps2=mand[3]

# CONCRETE                  tag   f'c        ec0   f'cu        ecu
# Core concrete (confined)
uniaxialMaterial('Concrete01',1, fc, eps1,fc2,eps2)

# Cover concrete (unconfined)
uniaxialMaterial('Concrete01',2, fc1U,eps1U,fc2U,eps2U)

# STEEL
# Reinforcing steel 
params=[R0,cR1,cR2]
#                        tag  fy E0    b
uniaxialMaterial('Steel02', 3, Fy, Es, Bs,R0,cR1,cR2)

# Define cross-section for nonlinear columns
# ------------------------------------------

# set some paramaters
SecTag1=1
ri=0.0
ro=DCol/2.0
nfCoreR=8
nfCoreT=8
nfCoverR=2
nfCoverT=8
rc=ro-c
theta=360.0/numBarsSec

section('Fiber', SecTag1)

# Create the concrete fibers
patch('circ',1,nfCoreT,nfCoreR,0.0,0.0,ri,rc,0.0,360.0) # Define the core patch
patch('circ',2,nfCoverT,nfCoverR,0.0,0.0,rc,ro,0.0,360.0) #Define Cover Patch

# Create the reinforcing fibers
layer('circ',3,numBarsSec,barAreaSec,0.0,0.0,rc,theta,360.0)

# Estimate yield curvature
# (Assuming no axial load and only top and bottom steel)
# d -- from cover to rebar
# steel yield strain
epsy = Fy/Es
Ky = 2.2*epsy/(DCol)

# Print estimate to standard output
print("Estimated yield curvature: ", Ky)

# Set axial load 
P = -170.0

# Target ductility for analysis
mu = 15.0

# Number of analysis increments
numIncr = 100

# Call the section analysis procedure
MomentCurvature(SecTag1, P, Ky*mu, numIncr)

Mc=open('Mphi.out')
lines = Mc.readlines()
x = [line.split()[1] for line in lines]
y = [line.split()[0] for line in lines]

X=[float(i) for i in x]
Y=[float(i) for i in y]


    
plt.plot(X,Y)
plt.xlim(0, 0.003)
plt.ylim(0, max(Y)*1.05)
plt.xlabel('Curvature (1/in)')
plt.ylabel('Moment (kip-in)')
plt.grid()
plt.show()

# Reading Stress Strain
# Steel Bar

es_Stl=open('bar01.txt')
stllines = es_Stl.readlines() 

xs = [line.split()[2] for line in stllines]
ys = [line.split()[1] for line in stllines]
Xs=[float(i) for i in xs]
Ys=[float(i) for i in ys]

plt.figure()

plt.plot(Xs,Ys)

# Concrete Fiber

es_Conc=open('ConcreteStrain21.txt')
Conclines = es_Conc.readlines() 

xc = [line.split()[2] for line in Conclines]
yc = [line.split()[1] for line in Conclines]
Xc=[float(i) for i in xc]
Yc=[float(i) for i in yc]

plt.figure()

plt.plot(Xc,Yc)


#results = open('results.out','a+')

#u = nodeDisp(2,3)
#if abs(u-0.00190476190476190541)<1e-12:
#    results.write('PASSED : MomentCurvature.py\n');
#    print("Passed!")
#else:
#    results.write('FAILED : MomentCurvature.py\n');
#    print("Failed!")
#
#results.close()

print("==========================")
