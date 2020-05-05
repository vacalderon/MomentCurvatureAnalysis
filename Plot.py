# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

"credits"

import math
import numpy as np
import matplotlib.pyplot as plt
Mc=open('Mphi.out')
lines = Mc.readlines()
x = [line.split()[1] for line in lines]
y = [line.split()[0] for line in lines]
    
plt.plot(x,y,'-o')
plt.xlabel('Curvature')
plt.ylabel('Moment')
plt.grid()
plt.show()