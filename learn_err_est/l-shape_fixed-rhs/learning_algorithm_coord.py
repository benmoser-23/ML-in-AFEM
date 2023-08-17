import numpy as np
import multiprocessing
import os
import sys
sys.path.append('..')

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

from estimator_model import create_learn_predict

#set number of iterations
numiterations = 20

#load data
train_meshes_whole = np.load("train_meshes.npy")
train_estimates = np.load("train_estimates.npy")
test_meshes_whole = np.load("test_meshes.npy")
test_estimates = np.load("test_estimates.npy")
print("train and test data loaded")

#generate input for this case
train_meshes = []
for mesh_whole in train_meshes_whole:
	mesh = []
	for k, entry in enumerate(mesh_whole):
		if (k+2)%4 != 0 and (k+1)%4 != 0:
			mesh.append(entry)
	train_meshes.append(mesh)
train_meshes = np.array(train_meshes)
test_meshes = []
for mesh_whole in test_meshes_whole:
	mesh = []
	for k, entry in enumerate(mesh_whole):
		if (k+2)%4 != 0 and (k+1)%4 != 0:
			mesh.append(entry)
	test_meshes.append(mesh)
test_meshes = np.array(test_meshes)
print("right input for this case generated")

#calculate losses parallel
result = []
data = [[train_meshes, train_estimates, test_meshes, test_estimates]] * numiterations
pool_obj = multiprocessing.Pool()
result  = pool_obj.map(create_learn_predict, data)
pool_obj.close()
pool_obj.join()
losses = []
accuracies = []
for res in result:
    losses.append(res[0])
    accuracies.append(res[1])
print("----------------------------------------------------------------")
print("losses: ")
print(losses)
print("mean loss :", sum(losses)/len(losses))
print("accuracies:")
print(accuracies)
print("mean accuracy :", sum(accuracies)/len(accuracies))
np.save('losses_coord',np.array(losses))
np.save('accuracies_coord',np.array(accuracies))
print("losses and accuracies saved to file")
print("\007")
