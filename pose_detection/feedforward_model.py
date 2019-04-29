import tensorflow as tf
import numpy as np
import time
from augment import Generator
import matplotlib.pyplot as plt
from tensorflow.python.tools import inspect_checkpoint as chkp

"""
This object is a feedforward neural network using tensorflow and a generator
with data autmentation. The object initializes with scalars input size, 
output size, learning rate, and l2 regularization. It also has a list of ints 
as the units for the hidden layers. There is another list of floats for the
keep probability values for each hidden layer. These two lists must be of the
same length. Finally, there is the activation function, which stays consistent
across all layers (except for the output layer). The network takes data with 
input_size number of features, puts it through hidden layers with sizes denoted
by hidden_layer_size, and outputs output_size number of outputs.
It takes batches of any size but must be an NxM matrix input. Using the train 
function, users can train on presplit data and can alter the parameters of 
batch size, number of epochs, translation, flips, rotations, and added noise. 
This trained network is automatically saved under the given name and can be 
loaded for further training.
"""

class feedforward(object):
    # Initializes the network for training/prediction
    def __init__(self, input_size, output_size, hidden_layer_size=[64], 
                 learning_rate=0.001, lambda_l2_reg=.001, c_r='classification',
                 train_keep_prob=[.7], activation=tf.nn.relu):
        # Ensures that the hidden layers have corresponding keep probs
        assert(len(hidden_layer_size) == len(train_keep_prob))

        # Sets variables for later use
        self.input_size = input_size
        self.output_size = output_size
        self.hidden_layer_size = hidden_layer_size
        self.learning_rate = learning_rate
        self.lambda_l2_reg = lambda_l2_reg
        self.c_r = c_r
        self.train_keep_prob = train_keep_prob
        self.activation = activation

        # Creates NN using private functions
        self.__input_layer()
        self.__hidden_layers()
        self.__output_layer()
        self.__loss()
        self.__optimizer()
        self.saver = tf.train.Saver()

    # Creates the input layer for data using placeholders
    def __input_layer(self):
        self.inputs = tf.placeholder(tf.float32,shape=(None,self.input_size),name="input_ph")
        self.targets = tf.placeholder(tf.int64,shape=(None,self.output_size),name="target_ph")

    # Takes inputs and puts them through hidden layers with dropout
    def __hidden_layers(self):
        self.hidden = tf.layers.dense(self.inputs,self.hidden_layer_size[0],
                                      activation=self.activation)
        self.hidden = tf.layers.dropout(self.hidden,
                                        rate=self.train_keep_prob[0])

        for i in range(1,len(self.hidden_layer_size)):
            self.hidden=tf.layers.dense(self.hidden,self.hidden_layer_size[i],
                                        activation=self.activation,name="hl_{}".format(i),reuse=True)
            self.hidden=tf.layers.dropout(self.hidden,
                                          rate=self.train_keep_prob[i+1],name="do_{}".format(i),reuse=True)

    # Takes output of previous hidden layer and creates an output of output_size
    # (This does not have dropout because it is the output layer)
    def __output_layer(self):
        self.output = tf.layers.dense(self.hidden,self.output_size)

    # Defines loss based on if the output is a regression or classification. If 
    # classification, use softmax, if regression, use mean squared error
    def __loss(self):
        if self.c_r == 'regression':
            self.loss = tf.losses.mean_squared_error(self.targets,self.output)
        elif self.c_r == 'classification':
            self.loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(
                                       labels=self.targets,logits=self.output))
            self.pred = tf.argmax(input=self.output,axis=1,name='pred')
        else:
            raise ValueError('Not regresson or classification')

    # Minimizes the loss using an Adam optimizer
    def __optimizer(self):
        self.optimizer = tf.train.AdamOptimizer(
                         learning_rate=self.learning_rate).minimize(self.loss)

    # Trains the network based on the test inputs given and uses the test set
    # to test accuracy on a non training set
    def train(self,train_x,train_y,test_x,test_y,epochs=20,batch_size=64,
              translate=[0,0],flip=[0,0],rotate=0,noise=0,model_name=None,
              pre_trained_model=None):

        # Create the generator to output batches of data with given transforms
        gen = Generator(train_x,train_y,translate=translate,flip=flip,
                        rotate=rotate,noise=noise)
        next_batch = gen.gen_batch(batch_size)

        # Set number of iterations (SIZE CAN BE CHANGED BECAUSE OF GENERATOR)
        aug_size = gen.aug_size()
        iters = int(aug_size / batch_size)
        print('number of batches for training: {}'.format(iters))
        
        # Set base levels and model name
        iter_tot = 0
        best_acc = 0
        self.losses = []
        if model_name == None:
            cur_model_name = 'basic_model'

        # Start session, initialize variables, and load pretrained model if any
        self.session = tf.Session()
        with self.session as sess:
            merge = tf.summary.merge_all()
            writer = tf.summary.FileWriter("log/{}".format('model'),
                                           self.session.graph)
            sess.run(tf.global_variables_initializer())
            if pre_trained_model != None:
                try:
                    print("Loading model from: {}".format(pre_trained_model))
                    self.saver.restore(sess,'model/{}'.format(pre_trained_model))
                except Exception:
                    raise ValueError("Failed Loading Model")

            # Set up loops for epochs and iterations per epochs
            for epoch in range(epochs):
                print("epoch {}".format(epoch + 1))

                for itr in range(iters):
                    merge = tf.summary.merge_all()
                    iter_tot += 1

                    # Create feed values using the generator
                    (feed_x,feed_y) = next(next_batch)
                    feed = {self.inputs: feed_x, self.targets: feed_y}

                    # Feed values to optimizer and output loss (for printing)
                    _, cur_loss = sess.run([self.optimizer,self.loss],
                                           feed_dict=feed)
                    self.losses.append(cur_loss)

                    # After 25 iterations, check if test accuracy has increased
                    if iter_tot % 25 == 0:
                        pred = sess.run([self.pred],feed_dict={self.inputs:
                                            test_x, self.targets: test_y})
                        act = np.argmax(test_y,axis=1)
                        val_acc = np.mean(np.argmax(test_y,axis=1)==pred)*100
                        if val_acc > best_acc:
                            print('Best validation accuracy! iteration:'
                                  '{} accuracy: {}%'.format(iter_tot, val_acc))
                            best_acc = val_acc
                            self.saver.save(sess,'model/{}'.format(
                                            cur_model_name))

        print("Traning ends. The best valid accuracy is {}." \
               " Model named {}.".format(best_acc, cur_model_name))

    # Plot training losses from most recent session
    def plot(self):
        plt.plot(self.losses)

    def predict(self,x,pre_trained_model=None):
        self.session = tf.Session()
        with self.session as sess:
            if pre_trained_model != None:
                try:
                    print("Loading model from: {}".format(pre_trained_model))
                    self.saver.restore(sess,'model/{}'.format(pre_trained_model))
                except Exception:
                    raise ValueError("Failed Loading Model")
            else:
                self.saver.restore(sess,tf.train.latest_checkpoint('model/'))
            pred = sess.run([self.pred],feed_dict={self.inputs: x})
            return pred




