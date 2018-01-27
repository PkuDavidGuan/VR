'''
Clean the raw data from IQIYI, 
and each line has the format: "timestamp jing wei"
'''
import re
import math
import os
import numpy as np


def clean(filename):
    infile_path = '/home/netlab-ml/workspace/IQIYI/VRdata2/' + filename
    outfile_path = '/home/gys/VRdata/'
    tmp_str = filename.split('_')
    outfile_path += '_'.join(tmp_str[:-1])
    outfile_path += '.txt'

    infile = open(infile_path, 'r')

    base = np.array([0, 0, -1, 1]).transpose()
    try:
        line = infile.readline()
    except:
        infile.close()
        return
    outfile = open(outfile_path, 'a')
    flag = False
    base_j = 0

    while True:
        try:
            start = line.index('[')
        except:
            break

        try:
            num = int(line[0:start])
        except:
            infile.close()
            outfile.close()
            return

        try:
            end = line.index(']')
        except:
            infile.close()
            outfile.close()
            return

        a = line[start + 1:end].split(',')
        matrix = []
        for i in a:
            try:
                matrix.append(float(i))
            except:
                infile.close()
                outfile.close()
                return
        matrix = np.array(matrix).reshape((4, 4))
        line = line[end + 1:]
        point = np.dot(matrix, base)

        if not flag:
            flag = True
            try:
                base_j = math.acos(point[0] / math.sqrt(point[0] * point[0] + point[2] * point[2])) * 180 / math.pi
            except:
                infile.close()
                outfile.close()
                return

        try:
            jing = math.acos(point[0] / math.sqrt(point[0] * point[0] + point[2] * point[2])) * 180 / math.pi - base_j
            wei = math.asin(
                point[1] / math.sqrt(point[0] * point[0] + point[1] * point[1] + point[2] * point[2])) * 180 / math.pi
        except:
            continue

        outfile.write(str(num) + '\t' + str(jing) + '\t' + str(wei) + '\n')

    infile.close()
    outfile.close()


if __name__ == '__main__':
    # clean('VR_987343709_A000004FEB8331_1505966244277_0.txt')
    files = os.listdir('/home/netlab-ml/workspace/IQIYI/VRdata2')
    files.sort()
    count = 0
    flag = False
    for f in files:
        # if not flag:
        #     if f == 'VR_380435222_4234DDFF-2511-47CC-BB00-ED34B9AE80BA_1506694458764_25.txt':
        #         flag = True
        #     continue
        if f[-4:] == '.txt':
            count += 1
            print(f)
            clean(f)
