import pickle
import random
from os.path import exists

import ngsolve as ng
from netgen.geom2d import SplineGeometry

from functions import partition_mesh, random_rhs

#--------------------------------
#number of meshes in the learning data
#--------------------------------
nummeshes = None
while not nummeshes:
	inputnummeshes = input("What should be the number of meshes " + 
								"in the training data? ")
	try:
		nummeshes = int(inputnummeshes)
		print("number of meshes in training data:", nummeshes)
	except ValueError:
		print("Input has to be an integer!")

#--------------------------------
#load maximum number of elements per part from model data
#--------------------------------
if exists("model_data"):
	file_model_data = open("model_data", "rb")
	model_data = pickle.load(file_model_data)
	file_model_data.close
	print(model_data)
	maxnumelements = model_data[1]
	print("model data loaded")
else:
	print(
		"no model data found. to create learning data " + 
		"first run 'setup_model.py'"
		)
	quit()

#--------------------------------
#create learning data
#--------------------------------
meshes = []
partitions = []
rectangles = []
righthandsides = []
solutions = []
totalnumparts = 0
for k in range(nummeshes):
	print('-----------------')
	print('mesh nr: ', k + 1, '/', nummeshes)
	#create 'random' geometry
	geo = SplineGeometry()
	p1 = geo.AppendPoint(0+random.choice([-2,2])*random.random(),0+random.choice([-2,2])*random.random())
	p2 = geo.AppendPoint(4+random.choice([-2,2])*random.random(),0+random.choice([-2,2])*random.random())
	p3 = geo.AppendPoint(8+random.choice([-2,2])*random.random(),0+random.choice([-2,2])*random.random())
	p4 = geo.AppendPoint(8+random.choice([-2,2])*random.random(),4+random.choice([-2,2])*random.random())
	p5 = geo.AppendPoint(8+random.choice([-2,2])*random.random(),8+random.choice([-2,2])*random.random())
	p6 = geo.AppendPoint(4+random.choice([-2,2])*random.random(),8+random.choice([-2,2])*random.random())
	p7 = geo.AppendPoint(0+random.choice([-2,2])*random.random(),8+random.choice([-2,2])*random.random())
	p8 = geo.AppendPoint(0+random.choice([-2,2])*random.random(),4+random.choice([-2,2])*random.random())
	geo.Append(["line", p1, p2])
	geo.Append(["line", p2, p3])
	geo.Append(["line", p3, p4])
	geo.Append(["line", p4, p5])
	geo.Append(["line", p5, p6])
	geo.Append(["line", p6, p7])
	geo.Append(["line", p7, p8])
	geo.Append(["line", p8, p1])
	mesh = ng.Mesh(geo.GenerateMesh(maxh=0.7))
	fes = ng.H1(mesh, order = 1, dirichlet=".*")

	#refine mesh 'randomly'
	for i in range(random.choice([0,1,2])):
		M = [random.choice([True, False, False]) for j in range(mesh.ne)]
		for k, el in enumerate(mesh.Elements()):
		    mesh.SetRefinementFlag(el, M[k])
		mesh.Refine()
	fes.Update()
	print("mesh generated. number of elements: ", mesh.ne)

	#partition the mesh
	partition, rectangle = partition_mesh(mesh, maxnumelements)
	totalnumparts += len(partition)
	print("number of parts: ", len(partition))

	#right hand side (uncomment the desired option)
	rhs = ng.x * ng.y #fixed
	#rhs = random_rhs(fes) #random

	#solve poisson
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

	meshes.append(mesh)
	partitions.append(partition)
	rectangles.append(rectangle)
	righthandsides.append(rhs)
	solutions.append(gfu)
print("learning data generated. total number of parts:", totalnumparts)

#--------------------------------
#save learning data to file
#--------------------------------
learning_data = [meshes, partitions, rectangles, righthandsides, solutions]
file_learning_data = open("learning_data", "wb")
pickle.dump(learning_data, file_learning_data)
file_learning_data.close
print("learning data saved to file")