import pickle
from os.path import exists
import copy
import numpy as np

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

from functions import h1seminorm_loss_partitioned_meshes

#--------------------------------
#parameters for the learning algorithm
#--------------------------------
numiterations = 20
numdirections = 30

#--------------------------------
#load model data
#--------------------------------
if exists("model_data"):
	file_model_data = open("model_data", "rb")
	model_data = pickle.load(file_model_data)
	file_model_data.close
	model = model_data[0]
	maxnumelements = model_data[1]
	print("model data loaded")
else:
	print(
		"no model data found. to learn the model " + 
		"first run 'setup_model.py'"
		)
	quit()

#--------------------------------
#load learning data
#--------------------------------
#meshes
if exists("learning_data"):
	file_learning_data = open("learning_data", "rb")
	learning_data = pickle.load(file_learning_data)
	file_learning_data.close
	meshes = learning_data[0]
	partitions = learning_data[1]
	righthandsides = learning_data[3]
	solutions = learning_data[4]
	print("learning data loaded")
else:
	print(
		"no learning data found. to learn the model " + 
		"first run 'create_learning_data.py'"
		)
	quit()

#--------------------------------
#calculate initial loss
#--------------------------------
current_loss = h1seminorm_loss_partitioned_meshes(model, meshes, partitions, maxnumelements,
													righthandsides, solutions)
current_weights = copy.deepcopy(model.get_weights())
print("initial loss:", current_loss)

#--------------------------------
#learning loop
#--------------------------------
for i in range(numiterations):
	tmp_weights = copy.deepcopy(current_weights)
	for j in range(numdirections):
		for k, weight in enumerate(tmp_weights):
			if k % 2 == 0:
				rand_array = np.reshape(np.random.rand(np.size(weight)), np.shape(weight))
				weight += 2 * (rand_array - 0.5)
		model.set_weights(tmp_weights)
		loss = h1seminorm_loss_partitioned_meshes(model, meshes, partitions, maxnumelements,
													righthandsides, solutions)
		print("iteration:", i+1, ", direction:", j+1 ,", loss:", loss)
		if loss < current_loss:
			print("-----------------------------------------------")
			print("WEIGHTS UPDATED")
			print("    iteration number:", i+1)
			print("    direction number:", j+1)
			print("    old loss: ", current_loss)
			print("    new loss:", loss)

			current_loss = copy.deepcopy(loss)
			current_weights = copy.deepcopy(model.get_weights())

			model_data = [model, maxnumelements]
			file_model_data = open("model_data", "wb")
			pickle.dump(model_data, file_model_data)
			file_model_data.close
			print("model saved in file")

print("learning done. final loss:", current_loss)