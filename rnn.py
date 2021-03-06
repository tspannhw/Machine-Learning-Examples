## MNIST DATASET with RNN
# We are considering the timesteps to be the rows in the image
# therefore the input vector is of the form 28*28 where 28 in the num_input and the other 28 is the timesteeps.
# Since we are using static images in our case it happens to be the dimensiona of the image as well.


from __future__ import print_function
print(1)
import tensorflow as tf
from tensorflow.contrib import rnn
from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets('/tmp/data/',one_hot=True)

# Training Parameters
learning_rate = 0.001
training_steps = 10000
batch_size = 128
display_step = 200

# Network Parameters
num_input = 28 # MNIST data input (img shape: 28*28)
# Number of time samples the RNN has to be unfolded over.
timesteps = 28 # timesteps
num_hidden = 128 # hidden layer num of features
num_classes = 10 # MNIST total classes (0-9 digits)

# tf Graph input
X = tf.placeholder("float", [None, timesteps, num_input])
Y = tf.placeholder("float", [None, num_classes])


# Define weights
weights = {
    'out': tf.Variable(tf.random_normal([num_hidden, num_classes]))
}
biases = {
    'out': tf.Variable(tf.random_normal([num_classes]))
}

def RNN(x, wieghts, biases):
    # Unroll the data
    x = tf.unstack(x,timesteps,1)

    # Define a LSTM cell
    # the bias to be added to the cell.
    lstm = rnn.BasicLSTMCell(num_hidden,forget_bias=1.0)

    outputs,states = rnn.static_rnn(lstm, x,dtype=tf.float32)

    # Activation
    return tf.matmul(outputs[-1],weights['out']) + biases['out']


logits = RNN(X,weights,biases)
prediction = tf.nn.softmax(logits)

loss_op = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=logits,labels=Y))
optimizer = tf.train.GradientDescentOptimizer(learning_rate)
train_op = optimizer.minimize(loss_op)

correct_pred = tf.equal(tf.argmax(prediction,1),tf.argmax(Y,1))
accuracy = tf.reduce_mean(tf.cast(correct_pred,tf.float32))

init = tf.global_variables_initializer()

with tf.Session() as sess:
    sess.run(init)

    for step in range(1,training_steps):
        batch_x, batch_y = mnist.train.next_batch(batch_size)
        batch_x = batch_x.reshape((batch_size,timesteps,num_input))
        sess.run(train_op,feed_dict={X:batch_x,Y:batch_y})
        if step%display_step == 0 or step == 1:
            loss,acc = sess.run([loss_op,accuracy],feed_dict={X:batch_x,Y:batch_y})

            print("Step " + str(step) + ", Minibatch Loss= " + "{:.4f}".format(loss) + ", Training Accuracy= " + "{:.3f}".format(acc))

    print("Optimization Finished!")
