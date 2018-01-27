import os
import pickle

def interpolation(infile_path, outfile_path, filename, size):
    infile = open(infile_path+filename, 'r')
    

    data = []
    final_dir = {}
    flag = False
    first_point = None
    last_point = None
    while True:
        line = infile.readline().strip()
        if not line:
            last_point = int(p[0])
            break
        p = line.split('\t')
        
        if(int(p[0])%size == 0):
            final_dir[int(p[0])] = [float(p[1]), float(p[2])]
        if not flag:
            first_point = int(p[0])
            flag = True
        data.append(p)

    first_point = (first_point-1)/size + 1
    last_point = last_point/size

    begin = 0
    end = 0

    for i in range(first_point, last_point+1):
        point = i * size
        if point in final_dir.keys():
            continue
            
        while True:
            if int(data[end][0]) < point:
                begin = end
                end += 1
            else:
                break
        jing = (float(data[begin][1]) + float(data[end][1])) / 2
        wei = (float(data[begin][2]) + float(data[end][2])) / 2
        final_dir[point] = [jing, wei]

    
    data = []
    for i in range(first_point, last_point+1):
        point = i * size
        data.append([point, final_dir[point][0], final_dir[point][1]])
    with open(outfile_path+filename[0:-4]+'.pkl', 'wb') as outfile:
        pickle.dump(data, outfile)

    infile.close()
    return

def interpolation_pkl(infile_path, outfile_path, filename, size):
    with open(infile_path+filename, 'rb') as infile:
        data = pickle.load(infile)
    
    final_dir = {}
    
    for p in data:
        timestamp = int(float(p[0])*1000)    
        if(timestamp%size == 0):
            final_dir[timestamp] = [p[1], p[2]]

    first_point = (int(float(data[0][0])*1000)-1)/size + 1
    last_point = int(float(data[-1][0])*1000) /size

    begin = 0
    end = 0

    for i in range(first_point, last_point+1):
        point = i * size
        if point in final_dir.keys():
            continue
            
        while True:
            if int(float(data[end][0])*1000) < point:
                begin = end
                end += 1
            else:
                break
        jing = (data[begin][1] + data[end][1]) / 2
        wei = (data[begin][2] + data[end][2]) / 2
        final_dir[point] = [jing, wei]

    data = []
    for i in range(first_point, last_point+1):
        point = i * size
        data.append([point, final_dir[point][0], final_dir[point][1]])
    print('begin: %d; end: %d' % (data[0][0], data[-1][0]))
    with open(outfile_path+filename, 'wb') as outfile:
        pickle.dump(data, outfile)
    
    return

if __name__ == '__main__':
    files = os.listdir('/home/gys/fineVR/video/regular')
    files.sort()
    for f in files:
        print(f)
        interpolation('/home/gys/fineVR/video/regular/', '/home/gys/fineVR/video/interpolation/', f, 200)
        
# if __name__ == '__main__':
#     for video in range(0, 9):
#         for experiment in range(1,3):
#             for client in range(1, 49):
#                 print('%d %d %d' % (experiment, client, video))
#                 filename = str(experiment) + '_' + str(client) + '_' + str(video) + '.pkl'
#                 interpolation_pkl('/home/gys/fineVR/formated/', '/home/gys/fineVR/formated/interpolation/', filename, 20)