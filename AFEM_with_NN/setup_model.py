import pickle
from os.path import exists

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

#check wether a model is already existing
if exists("model_data"):
	yesno = input("There is already a model existing. Do you want to overwrite it? (Y/N): ")
	if yesno in ["y", "Y"]:
		print("Existing model will be overwritten.")
	else:
		print("Setup cancelled.")
		quit()

#maximum number of element per part
maxnumelements = None
while not maxnumelements:
	inputmaxnumelements = input("What should be the maximum number of elements per part" + 
								" in the partition of the mesh? ")
	try:
		maxnumelements = int(inputmaxnumelements)
		print("maximum number of elements per part:", maxnumelements)
	except ValueError:
		print("Input has to be an integer!")

# create modell
model = tf.keras.Sequential()
# add input layer
model.add(tf.keras.layers.Input(shape=(9*maxnumelements,)))
# add dense layer
model.add(tf.keras.layers.Dense(9*maxnumelements/6, activation='relu'))
# add output layer
model.add(tf.keras.layers.Dense(maxnumelements, activation='softmax'))

model_data = [model, maxnumelements]

file_model_data = open("model_data", "wb")
pickle.dump(model_data, file_model_data)
file_model_data.close
print("model created and saved to file")