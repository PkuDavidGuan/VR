'''
Filter out videos that are too short or too rare.
'''
import os
import pickle

def too_small(f):
    '''Less than 25 points in the file'''
    filename = '/home/gys/VRdata/'+f
    infile = open(filename, 'r')
    count = 0
    while True:
        line = infile.readline()
        if not line:
            break
        count += 1
    infile.close()

    if count < 25:
        return True
    else:
        return False

def too_rare(f, refcount):
    '''Less than 4 people have watched the video'''
    video = f.split('_')[1]
    if video not in refcount.keys():
        return True
    elif refcount[video] < 4:
        return True
    else:
        return False

def is_live(f):
    filename = '/home/gys/VRdata/'+f
    infile = open(filename, 'r')
    flag = False
    while True:
        line = infile.readline()
        if not line:
            break
        timestamp = line.split('\t')[0]
        if int(timestamp) > 86400000:
            flag = True
            break
    infile.close()
    
    return flag

def file_type(f):
    filename = '/home/gys/VRdata/'+f
    infile = open(filename, 'r')
    type = [False, False]
    prev = -1
    
    while True:
        line = infile.readline()
        if not line:
            break
        
        timestamp = line.split('\t')[0]
        timestamp = int(timestamp)
        if timestamp < prev or timestamp-prev > 60000:
            type[1] = True
        elif timestamp == prev:
            type[0] = True
        
        if type[0] and type[1]:
            break
        prev = timestamp
    
    
    infile.close()

    return type

def classify(f, live, type):
    origin = '/home/gys/VRdata/'+f
    filepath = ''
    if live:
        filepath = '/home/gys/fineVR/live/'
    else:
        filepath = '/home/gys/fineVR/video/'
    
    if (type[0]==False) and (type[1]==False):
        filepath += 'regular/'+f
        cmd = 'mv ' + origin + ' ' + filepath
        os.system(cmd)
    else:
        if type[0]:
            dest = filepath + 'rebuffer/'+ f
            cmd = 'cp ' + origin + ' ' + dest
            os.system(cmd)
        if type[1]:
            dest = filepath+'FR_FF/'+f
            cmd = 'cp ' + origin + ' ' + dest
            os.system(cmd)

    

if __name__ == '__main__':
    files = os.listdir('/home/gys/VRdata')
    files.sort()
    with open('refcount.pkl', 'rb') as infile:
        refcount = pickle.load(infile)

    for f in files:
        if too_small(f):
            continue
        if too_rare(f, refcount):
            continue
        classify(f, is_live(f), file_type(f))

# if __name__ == '__main__':
#     files = os.listdir('/home/gys/VRdata')
#     files.sort()

#     refcount = {}
#     for f in files:
#         video = f.split('_')[1]
#         if video not in refcount.keys():
#             refcount[video] = 1
#         else:
#             refcount[video] += 1
#     with open('refcount.pkl', 'wb') as infile:
#         pickle.dump(refcount, infile)
    
#     sorted_video = sorted(refcount.items(), key=lambda d:d[1], reverse=True)
#     with open('video_list.txt', 'w') as infile:
#         for v in sorted_video:
#             infile.write(str(v[0])+'\t'+str(v[1])+'\n')
