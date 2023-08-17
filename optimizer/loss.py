import numpy as np
import copy
import math
import pickle

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

import ngsolve as ng
from netgen.geom2d import SplineGeometry

def h1seminorm_loss(refinement_model, input_data, mesh, order, rhs, maxnum_marked):
	#uniformally refined mesh
	mesh_u = copy.deepcopy(mesh)
	fes_u = ng.H1(mesh_u, order = order, dirichlet=".*")
	u_u, v_u = fes_u.TnT()
	gfu_u = ng.GridFunction(fes_u)
	a_u = ng.BilinearForm(fes_u, symmetric=True)
	a_u += ng.grad(u_u)*ng.grad(v_u)*ng.dx
	f_u = rhs
	f_lf_u= ng.LinearForm(fes_u)
	f_lf_u += f_u*v_u*ng.dx
	mesh_u.Refine()
	fes_u.Update()
	gfu_u.Update()
	#print(gfu_u.vec)

	#solve poisson on uniformally refined mesh
	a_u.Assemble()
	f_lf_u.Assemble()
	gfu_u.vec.data = a_u.mat.Inverse(freedofs=fes_u.FreeDofs()) * f_lf_u.vec

	#determine marked elements from NN model
	nppred = refinement_model.predict(input_data)
	indices = np.argpartition(nppred,-maxnum_marked)[0][-maxnum_marked:]
	M = [False for j in range(mesh.ne)]
	for index in indices:
		M[index] = True

	#refine elements according to marked elements and calculate solution on this mesh
	mesh_m = copy.deepcopy(mesh)
	for k, el in enumerate(mesh_m.Elements()):
		mesh_m.SetRefinementFlag(el, M[k])
	mesh_m.Refine()
	fes_m = ng.H1(mesh_m, order = order, dirichlet=".*")
	u_m, v_m = fes_m.TnT()
	gfu_m = ng.GridFunction(fes_m)
	a_m = ng.BilinearForm(fes_m, symmetric=True)
	a_m += ng.grad(u_m)*ng.grad(v_m)*ng.dx
	f_m = rhs
	f_lf_m= ng.LinearForm(fes_m)
	f_lf_m += f_m*v_m*ng.dx
	a_m.Assemble()
	f_lf_m.Assemble()
	gfu_m.vec.data = a_m.mat.Inverse(freedofs=fes_m.FreeDofs()) * f_lf_m.vec

	#interpolate solution on 'markedrefined' mesh on uniformally refined mesh (L2-projection)
	gfu_mu = ng.GridFunction(fes_u)
	gfu_mu.Set(gfu_m)

	#calculate difference between the two solutions
	gf_diff = ng.GridFunction(fes_u)
	gf_diff.Set(gfu_u-gfu_mu)

	#return h1-seminorm of the difference
	return ng.Integrate(ng.grad(gf_diff)*ng.grad(gf_diff),mesh_u)

