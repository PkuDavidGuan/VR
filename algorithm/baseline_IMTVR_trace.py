import pickle
import random


def formated_test():
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
            bar[timestamp][0] = bar[timestamp][0]*1.0/count[timestamp]
            bar[timestamp][1] = bar[timestamp][1]*1.0/count[timestamp]
        
        ret = []
        for i in seq:
            if IMTVR_meta[i][video] == 0:
                continue
            else:
                for line in total[i]:
                    timestamp = line[0]
                    ret.append([line[0], bar[timestamp][0], bar[timestamp][1]])
                with open('/home/gys/VR/traces/baseline/IMTVR_'  + str(i) + '_' + str(video) + '.pkl', 'wb') as outfile:
                    pickle.dump(ret, outfile)
                break
        


if __name__ == '__main__':
    formated_test()