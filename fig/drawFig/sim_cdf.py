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

dic = {}
max_c = -1
with open('/home/gys/VR/analysis.pkl', 'rb') as infile:
    analysis = pickle.load(infile)
    # for experiment in range(1,3):
    for video in range(0, 9):
        video_analysis = analysis[0][video]
    
        for line in video_analysis:
            tmp = int(line[1])
            if tmp not in dic.keys():
                dic[tmp] = 1
            else:
                dic[tmp] += 1
            if max_c < tmp:
                max_c = tmp
for i in range(35):
    if i not in dic.keys():
        dic[i] = 0
for i in range(34):
    dic[i+1] += dic[i]
y = []
for i in range(35):
    y.append(dic[i] * 1.0 / dic[34])
plt.plot([i for i in range(35)], y)
plt.savefig('agg3.png')