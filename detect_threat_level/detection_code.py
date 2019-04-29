import tensorflow as tf
from feedforward_model import *

def prediction(skele,model_name='basic_model'):
    session = tf.Session()
    with session as sess:
        new_saver = tf.train.import_meta_graph('model/{}.meta'.format(model_name))
        new_saver.restore(sess, 'model/{}'.format(model_name))
        graph = tf.get_default_graph()
        input_ph = graph.get_tensor_by_name("input_ph:0")
        pred = graph.get_tensor_by_name("pred:0")

        predictions = pred = sess.run([pred],feed_dict={input_ph: skele})
