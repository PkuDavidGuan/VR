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

with open("/home/gys/VR/total.pkl", 'rb') as infile:
    total = pickle.load(infile)
with open("/home/gys/VR/freeze.pkl", 'rb') as infile:
    freeze = pickle.load(infile)

a1 = [0 for i in range(10)]
a2 = [0 for i in range(10)]
for k in total:
    tmp = int(k / 200)
    if tmp > 9:
        tmp = 9
    a1[tmp] += total[k]
for k in freeze:
    tmp = int(k / 200)
    if tmp > 9:
        tmp = 9
    a2[tmp] += freeze[k]
a3 = [a2[i]*1.0/a1[i] for i in range(10)]
print(a1)
print(a2)
print(a3)
x = [i*40 for i in range(10)]
plt.bar(x, a3, width = 35)
plt.savefig('freeze1.png')