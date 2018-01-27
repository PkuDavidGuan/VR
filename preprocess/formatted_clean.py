import numpy as np
import pickle
import math

def clean(data):
    min_t = float(data[0][0])
    index = 0
    for i in range(1, len(data)):
        tmp = float(data[i][0])
        if tmp < min_t:
            min_t = tmp
            index = i
    
    inc = [data[index]]
    prev = min_t
    for i in range(index+1, len(data)):
        if float(data[i][0]) < prev:
            continue
        inc.append(data[i])
        prev = float(data[i][0])
    return inc

def map(data):
    flag = False
    ret = []
    for line in data:
        qx = line[1]
        qy = line[2]
        qz = line[3]
        qw = line[4]
        x = 2*qx*qz + 2*qy*qw
        y = 2*qy*qz - 2*qx*qw
        z = 1 - 2*qx*qx - 2*qy*qy
        if not flag:
            base_j = math.acos(x/math.sqrt(x*x+z*z))*180/math.pi
            flag = True
        jing = math.acos(x/math.sqrt(x*x+z*z))*180/math.pi - base_j
        wei = math.asin(y/math.sqrt(x*x+y*y+z*z))*180/math.pi
        ret.append([line[0], jing, wei])
    return ret

def clean2(raw):
    data = []
    begin = 0
    for i in range(0, len(raw)):
        if raw[i][0] != raw[begin][0]:
            tmp = [raw[begin][0], 0, 0]
            for j in range(begin, i):
                for k in range(0, 2):
                    tmp[k+1] += float(raw[j][1+k])
            for k in range(0, 2):
                tmp[k+1] = tmp[k+1]*1.0/(i-begin)
            data.append(tmp)
            begin = i

    tmp = [raw[begin][0], 0, 0]
    for j in range(begin, len(raw)):
        for k in range(0, 2):
            tmp[k+1] += float(raw[j][1+k])
    for k in range(0, 2):
        tmp[k+1] = tmp[k+1]*1.0/(len(raw)-begin)
    data.append(tmp)
    return data

def read_file(filename, experiment, client, video):
    raw = np.loadtxt(filename, dtype='string', delimiter=',')
    data = []
    begin = 1
    for i in range(1, len(raw)):
        if raw[i][1] != raw[begin][1]:
            tmp = [raw[begin][1], 0, 0, 0, 0]
            for j in range(begin, i):
                for k in range(0, 4):
                    tmp[k+1] += float(raw[j][2+k])
            for k in range(0, 4):
                tmp[k+1] = tmp[k+1]*1.0/(i-begin)
            data.append(tmp)
            begin = i

    tmp = [raw[begin][1], 0, 0, 0, 0]
    for j in range(begin, len(raw)):
        for k in range(0, 4):
            tmp[k+1] += float(raw[j][2+k])
    for k in range(0, 4):
        tmp[k+1] = tmp[k+1]*1.0/(len(raw)-begin)
    data.append(tmp)
    
    data = clean(data)
    data = map(data)
    data = clean2(data)
    filename = str(experiment) + '_' + str(client) + '_' + str(video) + '.pkl'
    with open('/home/gys/fineVR/formated/'+filename, 'wb') as outfile:
        pickle.dump(data, outfile)
            
            
    return

if __name__ == '__main__':
    tmp_str = '/home/netlab-ml/workspace/IQIYI/Formated_Data/Experiment_'
    for experiment in range(1,3):
        for client in range(1, 49):
            for video in range(0, 9):
                filename = tmp_str + str(experiment) + '/' + str(client) + '/video_' + str(video) + '.csv'
                print('%d %d %d' % (experiment, client, video))
                read_file(filename, experiment, client, video)
                
                