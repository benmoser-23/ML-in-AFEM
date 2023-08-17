import numpy as np

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

def create_model(dim):
	estimator_model = tf.keras.Sequential([
			tf.keras.layers.Dense(1000, input_shape=(dim,), activation='relu'),
			tf.keras.layers.Dense(100, activation='relu'),
			tf.keras.layers.Dense(10, activation='relu'),
			tf.keras.layers.Dense(1)
			])
	class Mean_Relative_Error(tf.keras.losses.Loss):
		def __init__(self):
			super().__init__()
		def call(self, y_true, y_pred):
			loss = tf.math.square(tf.divide(tf.math.abs(y_pred - y_true), tf.math.abs(y_true)))
			return tf.reduce_mean(loss)
	estimator_model.compile(optimizer = 'adam',
							loss = Mean_Relative_Error(),
							metrics=[tf.keras.metrics.MeanSquaredError()])
	return estimator_model

def create_learn_predict(data):
	train_meshes = data[0]
	train_estimates = data[1]
	test_meshes = data[2]
	test_estimates = data[3]
	estimator_model = create_model(np.shape(train_meshes)[1])

	estimator_model.fit(train_meshes, train_estimates, epochs = 10)

	test_loss, test_acc = estimator_model.evaluate(test_meshes, test_estimates, verbose=2)
	print("-------------------------------------------")
	print("final loss: ", test_loss)
	print("-------------------------------------------")
	return test_loss, test_acc
