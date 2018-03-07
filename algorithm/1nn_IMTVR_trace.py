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

def formated_test():
    with open('/home/gys/VR/spherical2Rectangular.pkl', 'rb') as infile:
        dis_dic = pickle.load(infile)
    with open('/home/gys/VR/IMTVR_meta.pkl', 'rb') as infile:
        IMTVR_meta = pickle.load(infile)
    video_num = 7
    for video in range(0, video_num):
        print(video)
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
        val = seq[:6]

        pred = [[0, 0]]
        client_no = 0
        for client_no in seq:
            if IMTVR_meta[client_no][video] == 1:
                break
        real = total[client_no][1:]
        len_of_real = len(real)
        for j in range(len_of_real-1):
            jing = None
            wei = None
            min_dis = None
            for k in range(59):
                if k in val:
                    continue
                if IMTVR_meta[k][video] == 0:
                    continue
                timestamp = real[j][0]
                if timestamp >= len(total[k]):
                    continue
                tmp_dis = distance(total[k][timestamp][1], total[k][timestamp][2], real[j][1], real[j][2], dis_dic)
                if min_dis != None and tmp_dis < min_dis and m < len_of_candidate - 1:
                    min_dis = tmp_dis
                    jing = total[k][timestamp][1]
                    wei = total[k][timestamp][2]

            if min_dis == None:
                jing = wei = 0
            pred.append([jing, wei])
        with open('/home/gys/VR/traces/1nn/IMTVR_' + str(client_no) + '_' + str(video) + '.pkl', 'wb') as outfile:
            pickle.dump(pred, outfile)

if __name__ == '__main__':
    formated_test()