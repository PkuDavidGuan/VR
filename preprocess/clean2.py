import os
def clean(f):
    filename = '/home/gys/VRdata/' + f
    infile = open(filename, 'r')

    data = []
    prev = -1
    while True:
        line = infile.readline()
        if not line:
            break

        triple = line.split('\t')
        if int(triple[0]) > prev:
            prev = int(triple[0])
            data.append(line)
    infile.close()

    outfile = open(filename, 'w')
    for i in data:
        outfile.write(i)
    outfile.close()

if __name__ == '__main__':
    clean('2VR__862084036461698_1506408676346.txt')
    # files = os.listdir('/home/gys/VRdata')
    # files.sort()
    # for f in files:
    #     print(f)
    #     clean(f)