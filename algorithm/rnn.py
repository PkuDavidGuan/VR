import tensorflow as tf
import pickle
import random
from time import time
import numpy as np

with tf.name_scope('input'):
    x = tf.placeholder(tf.float32, [1, None, 2])
    y = tf.placeholder(tf.float32, [None, 2])

with tf.name_scope('LSTM'):
    lstm = tf.nn.rnn_cell.LSTMCell(32)
    lstm_output, _ = tf.nn.dynamic_rnn(lstm, x, dtype=tf.float32)

with tf.name_scope('MLP'):
    W1 = tf.Variable(tf.truncated_normal([32, 32]))
    b1 = tf.Variable(tf.truncated_normal([1, 32]))
    W2 = tf.Variable(tf.truncated_normal([32, 2]))
    b2 = tf.Variable(tf.truncated_normal([1, 2]))

    dense1_output = tf.matmul(lstm_output[0], W1) + b1
    dense2_output = tf.matmul(dense1_output, W2) + b2

with tf.name_scope('loss'):
    loss = tf.reduce_mean(tf.square(dense2_output-y))
with tf.name_scope('optimizer'):
    optim = tf.train.AdamOptimizer(1e-4).minimize(loss)

def rnn(val, experiment, video, total):
    sess = tf.Session()
    sess.run(tf.global_variables_initializer())
    bar = {}
    
    for i in range(1, 49):
        if i in val:
            continue
        data = total[i-1]
        data = np.array(data)
        data_len = len(data) / 32 * 32
        batch_num = data_len / 32

        train_x = data[:data_len, 1:3]
        train_y = np.zeros([data_len, 2])
        train_y[:data_len-1, :] = data[1:data_len, 1:3]
        if(data_len < len(data)):
            train_y[data_len-1] = data[data_len, 1:3]
        else:
            train_y[data_len-1] = data[-1, 1:3]
        
        for iter in range(batch_num):
            optim.run(feed_dict = {x:np.reshape(train_x[iter*32:(iter+1)*32], [1, 32, 2]), y:train_y[iter*32:(iter+1)*32]}, session=sess)
    
    for i in val:
        test_x = np.array(total[i-1])
        pred = sess.run(dense2_output, feed_dict = {x:np.reshape(test_x[:-1, 1:3], [1, len(test_x) - 1, 2]), y:test_x[1:, 1:3]})
        bar[i] = pred
    sess.close()
    return bar

def map2block(jing, wei):
    if jing < -180:
        jing = -180
    if jing > 180:
        jing = 180
    if wei < -90:
        wei = -90
    if wei > 90:
        wei = 90
    row = (int(wei+90))/30
    if row > 5:
        row = 5
    col = (int(jing+180))/30
    if col > 11:
        col = 11
    return row, col

def score1(total, val, bar):
    score = 0
    count = 0
    for i in val:
        data = total[i-1][1:]
        pred = bar[i]
        count += len(data)
        for j in range(len(data)):
            r1, c1 = map2block(data[j][1], data[j][2])
            r2, c2 = map2block(pred[j][0], pred[j][1])
            if r1==r2 and c1==c2:
                score += 1
    return score*1.0/count

def score2(total, val, bar):
    score = 0
    count = 0
    tmp = {0:9, 1:6, 2:4, 4:3, 5:2, 8:1}

    for i in val:
        data = total[i-1][1:]
        pred = bar[i]
        count += len(data)
        for j in range(len(data)):
            r1, c1 = map2block(data[j][1], data[j][2])
            r2, c2 = map2block(pred[j][0], pred[j][1])
            dis = (r1-r2)*(r1-r2) + (c1-c2)*(c1-c2)
            if dis <= 8:
                score += tmp[dis]
    
    return score*1.0/count

def jing_wei_formated(jing, wei):
    if jing < -180:
        jing = -180
    if jing > 180:
        jing = 180
    if wei < -90:
        wei = -90
    if wei > 90:
        wei = 90
    return int(jing+180), int(wei+90)
def metric(total, val, bar, dic):
    precision = 0
    recall = 0
    count = 0
    for i in val:
        data = total[i-1][1:]
        pred = bar[i]
        count += len(data)
        for j in range(len(data)):
            row, col = jing_wei_formated(data[j][1], data[j][2])
            t1 = dic[row][col]
            row, col = jing_wei_formated(pred[j][0], pred[j][1])
            t2 = dic[row][col]
            i1 = 0
            i2 = 0
            len1 = len(t1)
            len2 = len(t2)
            same_tile = 0
            while True:
                if i1 >= len1 or i2 >= len2:
                    break
                if t1[i1] < t2[i2]:
                    i1 += 1
                elif t1[i1] > t2[i2]:
                    i2 += 1
                else:
                    i1 += 1
                    i2 += 1
                    same_tile += 1
            precision += same_tile * 1.0 / len2
            recall += same_tile * 1.0 / len1
    return precision / count, recall / count, count

def formated_test(experiment):
    print(experiment)
    with open('/home/gys/VR/interest_graph.pkl', 'rb') as infile:
        dic = pickle.load(infile)
    video_num = 9
    for video in range(0, video_num):
        total = []
        for client in range(1, 49):
            filename = '/home/gys/fineVR/formated/interpolation/'+str(experiment)+'_'+str(client)+'_'+str(video)+'.pkl'
            with open(filename, 'rb') as infile:
                data = pickle.load(infile)
            total.append(data)

        seq = [i for i in range(1, 49)]
        random.shuffle(seq)
        a1 = 0
        a2 = 0
        a3 = 0
        a4 = 0
        for t in range(0, 8):
            begin = t*6
            end = (t+1)*6
            start_t = time()
            bar = rnn(seq[begin:end], experiment, video, total)
            stop_t = time()

            precision, recall, total_view_point = metric(total, seq[begin:end], bar, dic)
            a1 += precision
            a2 += recall
            a4 += (stop_t - start_t) / total_view_point
        a1 = a1 / 8
        a2 = a2 / 8
        a3 = 2 * a1 * a2 / (a1 + a2)
        a4 = a4 / 8
        print('%d\t%f\t%f\t%f\t%f' %(video, a1, a2, a3, a4))

if __name__ == '__main__':
    formated_test(1)
    formated_test(2)


# sess = tf.Session()
# sess.run(tf.global_variables_initializer())

# with open('/home/gys/fineVR/formated/interpolation/2_48_0.pkl', 'rb') as infile:
#     test_x = pickle.load(infile)
#     test_x = np.array(test_x)

# for client in range(1, 2):
#     filename = '/home/gys/fineVR/formated/interpolation/2_'+str(client)+'_0.pkl'
#     with open(filename, 'rb') as infile:
#         data = pickle.load(infile)
#         data = np.array(data)

#     data_len = len(data) / 32 * 32
#     batch_num = data_len / 32

#     train_x = data[:data_len, 1:3]
#     train_y = np.zeros([data_len, 2])
#     train_y[:data_len-1, :] = data[1:data_len, 1:3]
#     if(data_len < len(data)):
#         train_y[data_len-1] = data[data_len, 1:3]
#     else:
#         train_y[data_len-1] = data[-1, 1:3]
    
#     for iter in range(batch_num):
#         optim.run(feed_dict = {x:np.reshape(train_x[iter*32:(iter+1)*32], [1, 32, 2]), y:train_y[iter*32:(iter+1)*32]}, session=sess)
#     unk = sess.run(dense2_output, feed_dict = {x:np.reshape(test_x[:-1, 1:3], [1, len(test_x) - 1, 2]), y:test_x[1:, 1:3]})
#     print(len(test_x))
#     print(unk.shape)
# sess.close()