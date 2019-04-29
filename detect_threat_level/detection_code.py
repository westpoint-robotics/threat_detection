import tensorflow as tf
from feedforward_model import *

def prediction(skele):
	labels = np.array(['high','med','low'])
	model = feedforward(skele.shape[0],3,hidden_layer_size=[8],learning_rate=.0025,train_keep_prob=[.5])
	prediction = model.predict(skele)
	print("Predicted label is ", labels[prediction[0][0]])
