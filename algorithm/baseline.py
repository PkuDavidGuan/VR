import pickle
import random
from time import time

def average(val, experiment, video, total):
    bar = {}
    count = {}

    bar = [[0, 0] for i in range(50000)]
    count = [0 for i in range(50000)]
    for i in range(1, 49):
        if i in val:
            continue
        data = total[i-1]
        for line in data:
            timestamp = line[0]/20
            bar[timestamp][0] += line[1]
            bar[timestamp][1] += line[2]
            count[timestamp] += 1
    for timestamp in range(len(count)):
        if not count[timestamp]:
            continue
        bar[timestamp][0] = bar[timestamp][0]*1.0/count[timestamp]
        bar[timestamp][1] = bar[timestamp][1]*1.0/count[timestamp]
    
    return bar

def map2block(jing, wei):
    if jing < -180:
        jing = -180
    if jing > 180:
        jing = 180
    if wei < -90:
        wei = -90
    if wei > 90:
        wei = 90
    row = (int(wei+90))/30
    if row > 5:
        row = 5
    col = (int(jing+180))/30
    if col > 11:
        col = 11
    return row, col

def score1(data, bar):
    score = 0
    for line in data:
        timestamp = line[0]/20
        r1, c1 = map2block(line[1], line[2])
        r2, c2 = map2block(bar[timestamp][0], bar[timestamp][1])
        if r1==r2 and c1==c2:
            score += 1
    return score*1.0/len(data)

def score2(data, bar):
    score = 0
    tmp = {0:9, 1:6, 2:4, 4:3, 5:2, 8:1}
    for line in data:
        timestamp = line[0]/20

        r1, c1 = map2block(line[1], line[2])
        r2, c2 = map2block(bar[timestamp][0], bar[timestamp][1])

        dis = (r1-r2)*(r1-r2) + (c1-c2)*(c1-c2)
        if dis <= 8:
            score += tmp[dis]
    return score*1.0/len(data)

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
def metric(data, bar, dic):
    precision = 0
    recall = 0
    for line in data:
        timestamp = line[0]/20
        row, col = jing_wei_formated(line[1], line[2])
        t1 = dic[row][col]
        row, col = jing_wei_formated(bar[timestamp][0], bar[timestamp][1])
        t2 = dic[row][col]
        i1 = 0
        i2 = 0
        len1 = len(t1)
        len2 = len(t2)
        count = 0
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
                count += 1
        precision += count * 1.0 / len2
        recall += count * 1.0 / len1
    precision = precision * 1.0 / len(data)
    recall = recall * 1.0 / len(data)
    F1 = 2 * precision * recall / (precision + recall)
    return F1, precision, recall


def formated_test(experiment):
    with open('/home/gys/VR/interest_graph.pkl', 'rb') as infile:
        dic = pickle.load(infile)
    print(experiment)
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
        average_t = 0
        for t in range(0, 8):
            begin = t*6
            end = (t+1)*6
            start_t = time()
            bar = average(seq[begin:end], experiment, video, total)
            stop_t = time()
            average_view_point = 0
            for client in seq[begin:end]:
                data = total[client-1]
                average_view_point += len(data[1:])

                F1, precision, recall =  metric(data[1:], bar, dic)
                a1 += F1
                a2 += precision
                a3 += recall
            average_t += (stop_t - start_t) / (average_view_point / 6)
        a1 = a1*1.0/48
        a2 = a2*1.0/48
        a3 = a3*1.0/48
        average_t = average_t/8
        print('%d\t%f\t%f\t%f\t%f' %(video, a1, a2, a3, average_t))

if __name__ == '__main__':
    formated_test(1)
    formated_test(2)