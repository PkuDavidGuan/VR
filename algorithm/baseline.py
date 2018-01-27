import pickle
import random

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
    row = (int(wei+90))/30
    if row > 5:
        row = 5
    col = (int(jing+180))/45
    if col > 7:
        col = 7
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
        

def formated_test(experiment):
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
        for t in range(0, 8):
            begin = t*6
            end = (t+1)*6
            bar = average(seq[begin:end], experiment, video, total)
            for client in seq[begin:end]:
                data = total[client-1]
                
                a1 += score1(data[1:], bar)
                a2 += score2(data[1:], bar)
        a1 = a1*1.0/48
        a2 = a2*1.0/48/9
        print('video:%d\tscore1:%f\tscore2:%f' %(video, a1, a2))

if __name__ == '__main__':
    formated_test(1)
    formated_test(2)