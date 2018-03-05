import tensorflow as tf
import pickle
import random
import math
from time import time
import numpy as np

def distance(j1, w1, j2, w2, dis_dic):
    if j1 < -180:
        j1 = -180
    if j1 > 180:
        j1 = 180
    if w1 < -90:
        w1 = -90
    if w1 > 90:
        w1 = 90
    if j2 < -180:
        j2 = -180
    if j2 > 180:
        j2 = 180
    if w2 < -90:
        w2 = -90
    if w2 > 90:
        w2 = 90
    [x1, y1, z1] = dis_dic[int(j1+180)][int(w1+90)]
    [x2, y2, z2] = dis_dic[int(j2+180)][int(w2+90)]
    return abs(x1 - x2) + abs(y1 - y2) + abs(z1 - z2)

def knn(val, total, dis_dic):
    bar = {}
    
    for i in val:
        pred = [[0, 0]]
        real = total[i-1][1:]
        len_of_real = len(real)
        prev = [0 for j in range(48)]
        for j in range(len_of_real-1):
            jing = None
            wei = None
            min_dis = None
            for k in range(1, 49):
                if k in val:
                    continue
                # candidate = total[k-1]
                # len_of_candidate = len(candidate)
                # for m in range(prev[k-1], len_of_candidate):
                #     line = candidate[m]
                #     if line[0] > real[j][0]:
                #         prev[k-1] = m
                #         break
                #     if line[0] == real[j][0]:
                #         tmp_dis = distance(line[1], line[2], real[j][1], real[j][2], dis_dic)
                #         if min_dis != None and tmp_dis < min_dis and m < len_of_candidate - 1:
                #             min_dis = tmp_dis
                #             jing = candidate[m+1][1]
                #             wei = candidate[m+1][2]
                #         prev[k-1] = m + 1
                #         break
                timestamp = real[j][0] / 20
                if timestamp >= len(total[k-1]):
                    continue
                tmp_dis = distance(total[k-1][timestamp][1], total[k-1][timestamp][2], real[j][1], real[j][2], dis_dic)
                if min_dis != None and tmp_dis < min_dis and m < len_of_candidate - 1:
                    min_dis = tmp_dis
                    jing = total[k-1][timestamp][1]
                    wei = total[k-1][timestamp][2]

            if min_dis == None:
                jing = wei = 0
            pred.append([jing, wei])
        bar[i] = pred
    return bar

def jing_wei_formated(jing, wei):
    if jing < -180:
        jing = -180
    if jing > 180:
        jing = 180
    if wei < -90:
        wei = -90
    if wei > 90:
        wei = 90
    return int(jing+180), int(wei+90)

def metric(total, val, bar, dic):
    precision = 0
    recall = 0
    count = 0
    for i in val:
        data = total[i-1][1:]
        pred = bar[i]
        count += len(data)
        for j in range(len(data)):
            row, col = jing_wei_formated(data[j][1], data[j][2])
            t1 = dic[row][col]
            row, col = jing_wei_formated(pred[j][0], pred[j][1])
            t2 = dic[row][col]
            i1 = 0
            i2 = 0
            len1 = len(t1)
            len2 = len(t2)
            same_tile = 0
            while True:
                if i1 >= len1 or i2 >= len2:
                    break
                if t1[i1] < t2[i2]:
                    i1 += 1
                elif t1[i1] > t2[i2]:
                    i2 += 1
                else:
                    i1 += 1
                    i2 += 1
                    same_tile += 1
            precision += same_tile * 1.0 / len2
            recall += same_tile * 1.0 / len1
    return precision / count, recall / count, count

def formated_test(experiment):
    print(experiment)
    with open('/home/gys/VR/interest_graph.pkl', 'rb') as infile:
        dic = pickle.load(infile)
    with open('/home/gys/VR/spherical2Rectangular.pkl', 'rb') as infile:
        dis_dic = pickle.load(infile)
    video_num = 9
    for video in range(0, video_num):
        total = []
        for client in range(1, 49):
            filename = '/home/gys/fineVR/formated/interpolation/'+str(experiment)+'_'+str(client)+'_'+str(video)+'.pkl'
            with open(filename, 'rb') as infile:
                data = pickle.load(infile)
            total.append(data)

        seq = [i for i in range(1, 49)]
        random.shuffle(seq)
        a1 = 0
        a2 = 0
        a3 = 0
        a4 = 0
        for t in range(0, 8):
            begin = t*6
            end = (t+1)*6
            start_t = time()
            bar = knn(seq[begin:end], total, dis_dic)
            stop_t = time()

            precision, recall, total_view_point = metric(total, seq[begin:end], bar, dic)
            a1 += precision
            a2 += recall
            a4 += (stop_t - start_t) / total_view_point
        a1 = a1 / 8
        a2 = a2 / 8
        a3 = 2 * a1 * a2 / (a1 + a2)
        a4 = a4 / 8
        print('%d\t%f\t%f\t%f\t%f' %(video, a1, a2, a3, a4))

if __name__ == '__main__':
    formated_test(1)
    formated_test(2)