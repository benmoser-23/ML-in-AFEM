import random
import pickle
import math
import numpy as np
from os.path import exists

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

import ngsolve as ng
from netgen.geom2d import SplineGeometry
from netgen.geom2d import unit_square

from functions import partition_mesh, calculate_predictions_partitioned_mesh

#--------------------------------
#parameters for the adaptive algorithm
#--------------------------------
accuracy = 0.0000001
maxnumndofs = 3000

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
		"no model data found. to use AFEM with NN " + 
		"first run learn a model with" + 
		"'setup_model.py', 'create_learning_data.py' and 'learn_refinement_model.py'"
		)
	quit()

#--------------------------------
#create 'random' geometry and mesh it
#--------------------------------
geo = SplineGeometry()
p1 = geo.AppendPoint(0+random.choice([-0.5,0.5])*random.random(),0+random.choice([-0.5,0.5])*random.random())
p2 = geo.AppendPoint(1+random.choice([-0.5,0.5])*random.random(),0+random.choice([-0.5,0.5])*random.random())
p3 = geo.AppendPoint(2+random.choice([-0.5,0.5])*random.random(),0+random.choice([-0.5,0.5])*random.random())
p4 = geo.AppendPoint(2+random.choice([-0.5,0.5])*random.random(),1+random.choice([-0.5,0.5])*random.random())
p5 = geo.AppendPoint(2+random.choice([-0.5,0.5])*random.random(),2+random.choice([-0.5,0.5])*random.random())
p6 = geo.AppendPoint(1+random.choice([-0.5,0.5])*random.random(),2+random.choice([-0.5,0.5])*random.random())
p7 = geo.AppendPoint(0+random.choice([-0.5,0.5])*random.random(),2+random.choice([-0.5,0.5])*random.random())
p8 = geo.AppendPoint(0+random.choice([-0.5,0.5])*random.random(),1+random.choice([-0.5,0.5])*random.random())
geo.Append(["line", p1, p2])
geo.Append(["line", p2, p3])
geo.Append(["line", p3, p4])
geo.Append(["line", p4, p5])
geo.Append(["line", p5, p6])
geo.Append(["line", p6, p7])
geo.Append(["line", p7, p8])
geo.Append(["line", p8, p1])
mesh = ng.Mesh(geo.GenerateMesh(maxh=0.5))
#mesh = ng.Mesh(unit_square.GenerateMesh(maxh=0.2))
print("initial mesh generated. number of elements:", mesh.ne)

#--------------------------------
#define space, functions, forms
#--------------------------------
#FE Space
fes = ng.H1(mesh, order=1, dirichlet=".*")
#trial and test function
u, v = fes.TnT()
#numeric solution function
gfu = ng.GridFunction(fes)
#bilinearform
a = ng.BilinearForm(fes, symmetric=True)
a += ng.grad(u) * ng.grad(v) * ng.dx
#right hand side
#rhs = 32*(ng.y*(1-ng.y)+ng.x*(1-ng.x))
rhs = ng.x
f = ng.LinearForm(fes)
f += rhs * v * ng.dx

#--------------------------------
#calculate initial solution
#--------------------------------
a.Assemble()
f.Assemble()
gfu.vec.data = a.mat.Inverse(fes.FreeDofs(), inverse="sparsecholesky") * f.vec
#save initial mesh and solution to file
file_initial_mesh = open("initial_mesh", "wb")
pickle.dump([mesh, gfu], file_initial_mesh)
file_initial_mesh.close
print("initial mesh and solution saved to file")

#--------------------------------
#adaptive algorithm
#--------------------------------
iteration = 0
while fes.ndof < maxnumndofs:
	iteration += 1
	print('-------------------------------')
	print('iteration', iteration)

	#partition the mesh
	partition, rectangle = partition_mesh(mesh, maxnumelements)
	print('mesh partitioned. number of partitions:', len(partition))
	
	#determine marking set with ml model
	pred = calculate_predictions_partitioned_mesh(model, mesh, partition, maxnumelements, gfu)
	maxnum_marked = math.floor(mesh.ne/3)
	indices = np.argpartition(pred,-maxnum_marked)[0][-maxnum_marked:]
	marking_set = [False for j in range(mesh.ne)]
	for index in indices:
		marking_set[index] = True
	print('marking set determined. number of marked elements:', len(indices))

	#refine mesh according to marking set
	for count, el in enumerate(mesh.Elements()):
		mesh.SetRefinementFlag(el, marking_set[count])
	mesh.Refine()
	print("mesh refined. new number of elements:", mesh.ne)

	#calculate solution
	fes.Update()
	print("fes updated. new ndof:", fes.ndof)
	gfu.Update()
	a.Assemble()
	f.Assemble()
	gfu.vec.data = a.mat.Inverse(fes.FreeDofs(), inverse="sparsecholesky") * f.vec
print('-------------------------------')

#save final mesh and solution to file
file_final_mesh = open("final_mesh", "wb")
pickle.dump([mesh, gfu], file_final_mesh)
file_final_mesh.close
print("final mesh and solution saved to file")