import numpy as np
import copy
import math
import pickle
import multiprocessing

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

import ngsolve as ng
from netgen.geom2d import SplineGeometry

from loss import h1seminorm_loss

order = 1
rhs = ng.x * ng.y
maxh = 0.1
maxnum_marked_ratio = 1/3

numiterations = 40
numdirections = 30

#---------------------------------------------
#create L-shape geometry
#---------------------------------------------
geo = SplineGeometry()
p1 = geo.AppendPoint(0,0)
p2 = geo.AppendPoint(2,0)
p3 = geo.AppendPoint(2,1)
p4 = geo.AppendPoint(1,1)
p5 = geo.AppendPoint(1,2)
p6 = geo.AppendPoint(0,2)
geo.Append(["line", p1, p2])
geo.Append(["line", p2, p3])
geo.Append(["line", p3, p4])
geo.Append(["line", p4, p5])
geo.Append(["line", p5, p6])
geo.Append(["line", p6, p1])

#---------------------------------------------
#initial mesh
#---------------------------------------------
mesh = ng.Mesh(geo.GenerateMesh(maxh=maxh))
fes = ng.H1(mesh, order = order, dirichlet=".*")
numelements = mesh.ne
maxnum_marked = math.floor(numelements * maxnum_marked_ratio)

#---------------------------------------------
#solve poisson on intital mesh
#---------------------------------------------
u, v = fes.TnT()
gfu = ng.GridFunction(fes)
a = ng.BilinearForm(fes, symmetric=True)
a += ng.grad(u)*ng.grad(v)*ng.dx
f = rhs
f_lf = ng.LinearForm(fes)
f_lf += f*v*ng.dx
a.Assemble()
f_lf.Assemble()
gfu.vec.data = a.mat.Inverse(freedofs=fes.FreeDofs()) * f_lf.vec

#---------------------------------------------
#save initial mesh and solution to file
#---------------------------------------------
file_initial_mesh = open("initial_mesh", "wb")
pickle.dump([mesh, gfu], file_initial_mesh)
file_initial_mesh.close()
print("initial mesh and solution saved to file")

#---------------------------------------------
#create input data for model
#---------------------------------------------
input_data = []
for el in mesh.Elements(ng.VOL):
	for vertex in el.vertices:
		for coord in mesh[ng.NodeId(ng.VERTEX,vertex.nr)].point:
			input_data.append(coord)
		u_vertex = gfu(input_data[-2],input_data[-1])
		input_data.append(u_vertex)  
input_data = np.array(input_data)
datalength = len(input_data)
input_data = np.reshape(input_data, (1,datalength))

#---------------------------------------------
#setup of model
#---------------------------------------------
# create modell
refinement_model = tf.keras.Sequential()
# add input layer
refinement_model.add(tf.keras.layers.Input(shape=(datalength,)))
# add dense layer
refinement_model.add(tf.keras.layers.Dense(datalength/6, activation='relu'))
# add output layer
refinement_model.add(tf.keras.layers.Dense(datalength/9, activation='softmax'))
# copy initial weights
current_weights = copy.deepcopy(refinement_model.get_weights())

#---------------------------------------------
#calculate initial loss
#---------------------------------------------
current_loss = h1seminorm_loss(refinement_model, input_data, mesh, order, rhs, maxnum_marked)
print("initial loss:", current_loss)

#---------------------------------------------
#optimizing loop
#---------------------------------------------
for i in range(numiterations):
	tmp_weights = copy.deepcopy(current_weights)

	for j in range(numdirections):
		print("iteration:", i + 1, "direction", j + 1)

		for k, weight in enumerate(tmp_weights):
			if k % 2 == 0:
				rand_array = np.reshape(np.random.rand(np.size(weight)), np.shape(weight))
				weight += 2 * (rand_array - 0.5)
		refinement_model.set_weights(tmp_weights)

		loss = h1seminorm_loss(refinement_model, input_data, mesh, order, rhs, maxnum_marked)
		print("loss:", loss)

		if loss < current_loss:
			print("-----------------------------------------------")
			print("WEIGHTS UPDATED")
			print("    iteration number: ",i+1)
			print("    direction number: ",j+1)
			
			print("    old loss: ",current_loss)
			current_loss = copy.deepcopy(loss)
			print("    new loss: ",current_loss)
			current_weights = copy.deepcopy(refinement_model.get_weights())

refinement_model.set_weights(current_weights)
print("final loss: ", h1seminorm_loss(refinement_model, input_data, mesh, order, rhs, maxnum_marked))

#---------------------------------------------
#determine marked elements from NN model
#---------------------------------------------
nppred = refinement_model(input_data).numpy()
indices = np.argpartition(nppred,-maxnum_marked)[0][-maxnum_marked:]
M = [False for j in range(mesh.ne)]
for index in indices:
	M[index] = True

#---------------------------------------------
#refine elements according to marked elements
#---------------------------------------------
mesh_m = copy.deepcopy(mesh)
for k, el in enumerate(mesh_m.Elements()):
	mesh_m.SetRefinementFlag(el, M[k])
mesh_m.Refine()
fes_m = ng.H1(mesh_m, order = order, dirichlet=".*")

#---------------------------------------------
#solve poisson on refined mesh
#---------------------------------------------
u_m, v_m = fes_m.TnT()
gfu_m = ng.GridFunction(fes_m)
a_m = ng.BilinearForm(fes_m, symmetric=True)
a_m += ng.grad(u_m)*ng.grad(v_m)*ng.dx
f_m = rhs
f_lf_m = ng.LinearForm(fes_m)
f_lf_m += f_m*v_m*ng.dx
a_m.Assemble()
f_lf_m.Assemble()
gfu_m.vec.data = a_m.mat.Inverse(freedofs=fes_m.FreeDofs()) * f_lf_m.vec

#---------------------------------------------
#save final mesh and solution to file
#---------------------------------------------
file_final_mesh = open("final_mesh", "wb")
pickle.dump([mesh_m, gfu_m], file_final_mesh)
file_final_mesh.close()
print("final mesh and solution saved to file")