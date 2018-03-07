import pickle
import random
from time import time

def average(val, video, total, IMTVR_meta):
    bar = {}
    count = {}

    bar = [[0, 0] for i in range(50000)]
    count = [0 for i in range(50000)]
    for i in range(59):
        if i in val:
            continue
        if IMTVR_meta[i][video] == 0:
            continue
        data = total[i]
        for line in data:
            timestamp = line[0]
            bar[timestamp][0] += line[1]
            bar[timestamp][1] += line[2]
            count[timestamp] += 1
    for timestamp in range(len(count)):
        if not count[timestamp]:
            continue
        bar[timestamp][0] = bar[timestamp][0] * 1.0 / count[timestamp]
        bar[timestamp][1] = bar[timestamp][1] * 1.0 / count[timestamp]
    
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
def metric(data, bar, dic):
    precision = 0
    recall = 0
    for line in data:
        timestamp = line[0]
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


def formated_test():
    with open('/home/gys/VR/interest_graph.pkl', 'rb') as infile:
        dic = pickle.load(infile)
    with open('/home/gys/VR/IMTVR_meta.pkl', 'rb') as infile:
        IMTVR_meta = pickle.load(infile)
    video_num = 7
    for video in range(video_num):
        total = []
        for client in range(59):
            if IMTVR_meta[client][video] < 1:
                total.append([])
            else:
                filename = '/home/gys/fineVR/IMTVR/'+str(client)+'_'+str(video)+'.pkl'
                with open(filename, 'rb') as infile:
                    data = pickle.load(infile)
                total.append(data)

        seq = [i for i in range(59)]
        random.shuffle(seq)
        a1 = 0
        a2 = 0
        a3 = 0
        average_t = 0
        total_test_client_num = 0
        for t in range(0, 8):
            begin = t*6
            end = (t+1)*6
            start_t = time()
            bar = average(seq[begin:end], video, total, IMTVR_meta)
            stop_t = time()
            average_view_point = 0
            test_client_num = 0
            for client in seq[begin:end]:
                if IMTVR_meta[client][video] == 0:
                    continue
                test_client_num += 1
                data = total[client]
                average_view_point += len(data[1:])

                F1, precision, recall =  metric(data[1:], bar, dic)
                a1 += F1
                a2 += precision
                a3 += recall
            if test_client_num != 0:
                average_t += (stop_t - start_t) / (average_view_point / test_client_num)
            total_test_client_num += test_client_num
        a1 = a1*1.0/total_test_client_num
        a2 = a2*1.0/total_test_client_num
        a3 = a3*1.0/total_test_client_num
        average_t = average_t/8
        print('%d\t%f\t%f\t%f\t%f' %(video, a1, a2, a3, average_t))

if __name__ == '__main__':
    formated_test()