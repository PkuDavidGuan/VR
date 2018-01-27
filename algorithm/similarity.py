import sys
import math
import numpy as np
import pickle

def line_distance(a, b):
    if len(a) != len(b):
        print('vector a and b does not match.')
        sys.exit(1)
    
    ret = 0
    for i in range(0, len(a)):
        ret += math.sqrt((a[i][0]-b[i][0])*(a[i][0]-b[i][0]) + (a[i][1]-b[i][1])*(a[i][1]-b[i][1]))
        
    return ret*1.0/len(a)

def knn(distance, k):
    if len(distance) < k+1:
        print('Less than k clients.')
        sys.exit(1)
    sorted_d = sorted(distance)
    ret = 0
    for i in range(1, k+1):
        ret += sorted_d[i]
    return ret

def similarity(data, k):
    distance = np.zeros([len(data), len(data)])
    for i in range(0, len(data)):
        for j in range(i+1, len(data)):
            distance[i][j] = distance[j][i] = line_distance(data[i], data[j])
    
    total = 0
    for i in range(0, len(data)):
        total += knn(distance[i], k)
    return total*1.0/(k*len(data))

def filter(client, begin, end):
    if client[0][0] > begin:
        return False
    if client[-1][0] < end:
        return False
    return True

def window(raw, begin, end, size):
    ret = []
    for i in range(0, len(raw)):
        if not filter(raw[i], begin*size, end*size):
            continue

        tmp = []
        for line in raw[i]:
            if line[0] >= begin*size and line[0] <= end*size:
                tmp.append([line[1], line[2]])
            if line[0] > end*size:
                break
        ret.append(tmp)
    return ret


if __name__ == '__main__':
    analysis = []
    for experiment in range(1,3):
        experiment_analysis = []
        for video in range(0, 9):
            raw = []
            for client in range(1, 49):
                filename = str(experiment) + '_' + str(client) + '_' + str(video) + '.pkl'
                with open('/home/gys/fineVR/formated/interpolation/'+filename, 'rb') as infile:
                    tmp = pickle.load(infile)
                raw.append(tmp)
            
            foot = 50
            last = raw[0][-1][0]/20
            begin = 0
            video_analysis = []
            while begin <= last:
                end = begin+foot-1
                if end > last:
                    end = last
                sim = similarity(window(raw, begin, end, 20), 6)
                video_analysis.append([begin, sim])
                begin = end+1
            
            experiment_analysis.append(video_analysis)
        
        analysis.append(experiment_analysis)
    with open('analysis.pkl', 'wb') as outfile:
        pickle.dump(analysis, outfile)
    