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

with open('/home/gys/fineVR/formated/1_1_0.pkl', 'rb') as infile:
    data = pickle.load(infile)
x = []
y = []
begin_count = 1000
end_count = 5000
count = 0
for d in data:
    count += 1
    if count > begin_count and count < end_count:
        x.append(d[1])
        y.append(d[2])
plt.scatter(x, y, s = 1)
with open('/home/gys/fineVR/formated/1_2_0.pkl', 'rb') as infile:
    data = pickle.load(infile)
x = []
y = []
count = 0
for d in data:
    count += 1
    if count > begin_count and count < end_count:
        x.append(d[1])
        y.append(d[2])
plt.scatter(x, y, s = 1)
with open('/home/gys/fineVR/formated/1_3_0.pkl', 'rb') as infile:
    data = pickle.load(infile)
x = []
y = []
count = 0
for d in data:
    count += 1
    if count > begin_count and count < end_count:
        x.append(d[1])
        y.append(d[2])
plt.scatter(x, y, s = 1)
with open('/home/gys/fineVR/formated/1_5_0.pkl', 'rb') as infile:
    data = pickle.load(infile)
x = []
y = []
count = 0
for d in data:
    count += 1
    if count > begin_count and count < end_count:
        x.append(d[1])
        y.append(d[2])
plt.scatter(x, y, s = 1)
plt.savefig('agg2.png')