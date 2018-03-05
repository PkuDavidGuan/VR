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

        sess = tf.Session()
        sess.run(tf.global_variables_initializer())
        saver = tf.train.Saver() 
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
            
            
        test_x = np.array(total[val[0]-1])
        pred = sess.run(dense2_output, feed_dict = {x:np.reshape(test_x[:-1, 1:3], [1, len(test_x) - 1, 2]), y:test_x[1:, 1:3]})
        saver.save(sess, '/home/gys/VR/rnn_models/' + str(experiment) + '_' + str(video) + '.ckpt')
        sess.close()
        with open('/home/gys/VR/traces/rnn/' + str(experiment) + '_' + str(video) + '.pkl', 'wb') as outfile:
            pickle.dump(pred, outfile)

if __name__ == '__main__':
    formated_test(1)
    formated_test(2)
