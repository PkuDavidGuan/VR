import matplotlib  
matplotlib.use('Agg')
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import math
import os
import sys
import pickle
import random
import pandas as pd

'''
with open("/home/gys/VR/distribution.pkl", 'rb') as infile:
    distribution = pickle.load(infile)

x = [i*1000 for i in range(10)]
plt.boxplot(distribution, labels = x)
plt.savefig('freeze2.png')
'''
with open("rebuffer.pkl", 'rb') as infile:
    rebuffer = pickle.load(infile)

for i in range(48):
    if i not in rebuffer.keys():
        rebuffer[i] = 0
for i in range(47):
    rebuffer[i+1] += rebuffer[i]
for i in range(48):
    rebuffer[i] = rebuffer[i] * 1.0 / rebuffer[47]

x = [i for i in range(48)]
y = []
for i in range(48):
    y.append(rebuffer[i])
plt.plot(x, y)
plt.savefig('freeze2.png')