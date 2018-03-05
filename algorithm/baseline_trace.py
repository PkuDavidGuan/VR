import pickle
import random


def formated_test(experiment):
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
        
        ret = []
        for line in total[0]:
            timestamp = line[0] / 20
            ret.append([line[0], bar[timestamp][0], bar[timestamp][1]])
        with open('/home/gys/VR/traces/baseline/' + str(experiment) + '_' + str(video) + '.pkl', 'wb') as outfile:
            pickle.dump(ret, outfile)
        


if __name__ == '__main__':
    #formated_test(1)
    formated_test(2)