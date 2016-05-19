import tensorflow as tf
import numpy as np


def run_training(x_images, y_labels, x_val, y_val, x_test, y_test):

    x = tf.placeholder(tf.float32, shape=[None, 90])
    y = tf.placeholder(tf.int32, shape=[None, ])  # TODO: ??
    keep_hidden = tf.placeholder("float")
    neurons = 4096
    lr = 1e-3

    logits = inference(x, keep_hidden, neurons)
    loss_ = loss(logits, y)
    train = training(loss_, lr)
    accuracy = evaluation(logits, y)

    sess = tf.Session()
    init = tf.initialize_all_variables()
    sess.run(init)
    batch_size = 200

    for steps in range(100000):
        rand = np.random.randint(0, x_images.shape[0], batch_size)
        x_batch = x_images[rand]
        y_batch = y_labels[rand]

        feed_dict = {x: x_batch, y: y_batch, keep_hidden: 0.5}

        _, loss_val = sess.run([train, loss_], feed_dict=feed_dict)

        if (steps+1) % 200 == 0:
            corr = sess.run(accuracy, feed_dict={x: x_val, y:y_val, keep_hidden: 1.0})
            acc = float(corr)/y_val.shape[0] * 100.0
            print "Step ", steps, "  - Validation accuracy: ", acc
            print "Training loss: ", loss_val
        if (steps+1) % 5000 == 0 :
            corr = sess.run(accuracy, feed_dict={x: x_test, y: y_test, keep_hidden: 1.0})
            acc = float(corr) / y_test.shape[0] * 100.0
            print "Step ", steps, "  - Test accuracy: ", acc



def evaluate():

    pass


def weight_variable(shape):
    return tf.Variable(tf.truncated_normal(shape, stddev=0.1))


def bias_variable(shape):
    return tf.Variable(tf.constant(0.1, shape=shape))


def inference(x, keep_hidden, neurons):

    # Fully connected layer 1
    with tf.name_scope('hidden1'):
        W1 = weight_variable([90, neurons])
        b1 = bias_variable([])
        activation1 = tf.nn.relu(tf.matmul(x, W1) + b1)
        activation1 = tf.nn.dropout(activation1, keep_hidden)

    # # #Output layer
    with tf.name_scope('softmax_layer'):
        W2 = weight_variable([neurons, 90])
        b2 = bias_variable([90])
        #softmax = tf.nn.softmax(tf.matmul(activation2, weights) + bias)
        logits = tf.matmul(activation1, W2) + b2

    return logits


def loss(logits, labels):
    labels = tf.to_int64(labels)
    cross_entropy = tf.nn.sparse_softmax_cross_entropy_with_logits(
        logits, labels, name='xentropy')
    loss_value = tf.reduce_mean(cross_entropy, name='xentropy_mean')
    return loss_value


def training(loss_value, learning_rate):
    train = tf.train.AdamOptimizer(learning_rate).minimize(loss_value)
    return train


def evaluation(logits, labels):
    correct = tf.nn.in_top_k(logits, labels, 1)
    accuracy = tf.reduce_sum(tf.cast(correct, tf.int32)) # reduce_sum instead?
    return accuracy
