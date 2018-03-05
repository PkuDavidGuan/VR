import pickle
import random
import math

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

def formated_test(experiment):
    with open('/home/gys/VR/spherical2Rectangular.pkl', 'rb') as infile:
        dis_dic = pickle.load(infile)
    video_num = 9
    for video in range(0, video_num):
        print(video)
        total = []
        for client in range(1, 49):
            filename = '/home/gys/fineVR/formated/interpolation/'+str(experiment)+'_'+str(client)+'_'+str(video)+'.pkl'
            with open(filename, 'rb') as infile:
                data = pickle.load(infile)
            total.append(data)

        seq = [i for i in range(1, 49)]
        random.shuffle(seq)
        val = seq[:6]

        pred = [[0, 0]]
        real = total[0][1:]
        len_of_real = len(real)
        prev = [0 for j in range(48)]
        for j in range(len_of_real-1):
            jing = None
            wei = None
            min_dis = None
            for k in range(1, 49):
                if k in val:
                    continue
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
        with open('/home/gys/VR/traces/1nn/' + str(experiment) + '_' + str(video) + '.pkl', 'wb') as outfile:
            pickle.dump(pred, outfile)

if __name__ == '__main__':
    formated_test(1)
    formated_test(2)