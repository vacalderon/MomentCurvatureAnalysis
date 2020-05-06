# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

"credits"

import math
import numpy as np
import matplotlib.pyplot as plt

# ------------------------------------------------
#           RESULTS
# -------------------------------------------------


Mc = open('Mphi.out')
lines = Mc.readlines()
x = [line.split()[1] for line in lines]
y = [line.split()[0] for line in lines]

X = [float(i) for i in x]
Y = [float(i) for i in y]

plt.plot(X, Y)
plt.xlim(0, 0.003)
plt.ylim(0, max(Y) * 1.05)
plt.xlabel('Curvature (1/in)')
plt.ylabel('Moment (kip-in)')
plt.grid()
plt.show()

# Reading Stress Strain
# Steel Bar

es_Stl = open('bar01.txt')
stllines = es_Stl.readlines()

xs = [line.split()[2] for line in stllines]
ys = [line.split()[1] for line in stllines]
Xs = [float(i) for i in xs]
Ys = [float(i) for i in ys]

plt.figure()

plt.plot(Xs, Ys)

# Concrete Fiber

es_Conc = open('ConcreteStrain21.txt')
Conclines = es_Conc.readlines()

xc = [line.split()[2] for line in Conclines]
yc = [line.split()[1] for line in Conclines]
Xc = [float(i) for i in xc]
Yc = [float(i) for i in yc]

plt.figure()

plt.plot(Xc, Yc)

# results = open('results.out','a+')

# u = nodeDisp(2,3)
# if abs(u-0.00190476190476190541)<1e-12:
#    results.write('PASSED : MomentCurvature.py\n');
#    print("Passed!")
# else:
#    results.write('FAILED : MomentCurvature.py\n');
#    print("Failed!")
#
# results.close()