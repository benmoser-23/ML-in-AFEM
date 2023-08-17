import copy
import numpy as np
import math
from numpy import random as rd

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

import ngsolve as ng
from netgen.geom2d import SplineGeometry

def h1seminorm_loss_partitioned_meshes(model, meshes, partitions, maxnumelements, righthandsides, solutions):
	#calculates the mean of the squared losses of the meshes
	losses = []
	for count, mesh in enumerate(meshes):
		losses.append(h1seminorm_loss_partitioned_mesh(model, mesh, partitions[count], maxnumelements,
														righthandsides[count], solutions[count]))
	return np.square(np.array(losses).mean())

def h1seminorm_loss_partitioned_mesh(model, mesh, partition, maxnumelements, rhs, solution):
	#calculates the h1 seminorm loss for a partitioned mesh
	pred = calculate_predictions_partitioned_mesh(model, mesh, partition, maxnumelements, solution)
	maxnum_marked = math.floor(mesh.ne/3)
	indices = np.argpartition(pred,-maxnum_marked)[0][-maxnum_marked:]
	marking_set = [False for j in range(mesh.ne)]
	for index in indices:
		marking_set[index] = True
	return h1seminorm_loss(mesh, marking_set, rhs)

def calculate_predictions_partitioned_mesh(model, mesh, partition, maxnumelements, solution):
	#calculates the predictions for a partitioned mesh
	predictions = [0] * mesh.ne
	counter = [0] * mesh.ne
	for part in partition:
		#determine coordinates of elements in part and corresponding value of solution
		input_data = []
		for elnr in part:
			el = mesh[ng.ElementId(ng.VOL,elnr)]
			for vertex in el.vertices:
				for coord in mesh[ng.NodeId(ng.VERTEX,vertex.nr)].point:
					input_data.append(coord)
				input_data.append(solution(input_data[-2],input_data[-1]))
		input_data.extend([0] * (9*maxnumelements-len(input_data)))
		input_data = np.array(input_data)
		input_data = tf.reshape(input_data,shape=(1,len(input_data)))

		#calculate predictions of part
		pred_part = model(input_data).numpy()

		#add predictions of part to predictions
		#if an element is in more than one part than the prediction for this
		#element is the arithmetic means of all the part predictions
		for count, elnr in enumerate(part):
			counter[elnr] += 1
			predictions[elnr] = ((counter[elnr] - 1) * predictions[elnr]
								  + pred_part[0][count]) / counter[elnr]
	return np.array([predictions])

def h1seminorm_loss(mesh, marking_set, rhs):
	#calculates h1 seminorm loss for a mesh , a marking set and a right hand side
	#uniformally refined mesh
	mesh_u = copy.deepcopy(mesh)
	fes_u = ng.H1(mesh_u, order = 1, dirichlet=".*")
	u, v = fes_u.TnT()
	gfu_u = ng.GridFunction(fes_u)
	a = ng.BilinearForm(fes_u, symmetric=True)
	a += ng.grad(u)*ng.grad(v)*ng.dx
	f = rhs
	f_lf = ng.LinearForm(fes_u)
	f_lf += f*v*ng.dx
	mesh_u.Refine()
	fes_u.Update()
	gfu_u.Update()

	#solve poisson on uniformally refined mesh
	a.Assemble()
	#print(a.mat)
	f_lf.Assemble()
	#print(f_lf.vec)
	gfu_u.vec.data = a.mat.Inverse(freedofs=fes_u.FreeDofs()) * f_lf.vec
	#print(gfu_u.vec)

	#refine elements according to marked elements and calculate solution on this mesh
	mesh_m = copy.deepcopy(mesh)
	for k, el in enumerate(mesh_m.Elements()):
		mesh_m.SetRefinementFlag(el, marking_set[k])
	mesh_m.Refine()
	fes_m = ng.H1(mesh_m, order = 1, dirichlet=".*")
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

	#return squared h1-seminorm of the difference
	return ng.Integrate(ng.grad(gf_diff)*ng.grad(gf_diff),mesh_u)

def partition_mesh(mesh, maxnumelements):
	#partitions the mesh
    partition = []
    rectangles = []
    elements = list(range(mesh.ne))

    #determine bounding rectangle of mesh
    xcoordinates = []
    ycoordinates = []
    for vertex in mesh.vertices:
        xcoordinates.append(vertex.point[0])
        ycoordinates.append(vertex.point[1])
    minx=min(xcoordinates)
    miny=min(ycoordinates)
    maxx=max(xcoordinates)
    maxy=max(ycoordinates)
    rectangle = [[minx, miny], [maxx, miny], [maxx, maxy], [minx, maxy]]

    #split the mesh
    split_mesh(elements, rectangle, maxnumelements, mesh, partition, rectangles)

    return partition, rectangles

def split_mesh(elements, rectangle, maxnumelements, mesh, partition, rectangles):
    #splits the mesh recursively
    if len(elements) <= maxnumelements:
        partition.append(elements)
        rectangles.append(rectangle)
    else:
        #determine minium, maximum and midpoint
        #of x and y coordinates of rectangle
        xs, ys = zip(*rectangle)
        minx = min(xs)
        maxx = max(xs)
        midx = (minx+maxx)/2
        miny = min(ys)
        maxy = max(ys)
        midy = (miny+maxy)/2
        
        #assign elements to the 4 subrectangles
        elements1 = []
        elements2 = []
        elements3 = []
        elements4 = []
        for elnr in elements:
            el = mesh[ng.ElementId(ng.VOL,elnr)]
            for vertex in el.vertices:
                xcoord = mesh[ng.NodeId(ng.VERTEX,vertex.nr)].point[0]
                ycoord = mesh[ng.NodeId(ng.VERTEX,vertex.nr)].point[1]
                #rectangle 1 bottom left
                if xcoord <= midx and ycoord <= midy:
                    elements1.append(elnr)
                #rectangle 2 bottom right
                if xcoord >= midx and ycoord <= midy:
                    elements2.append(elnr)
                #rectangle 3 top right
                if xcoord >= midx and ycoord >= midy:
                    elements3.append(elnr)
                #rectangle 4 top left
                if xcoord <= midx and ycoord >= midy:
                    elements4.append(elnr)
        elements1 = list(set(elements1))
        elements2 = list(set(elements2))
        elements3 = list(set(elements3))
        elements4 = list(set(elements4))
        
        rec1 = [[minx, miny], [midx, miny], [midx, midy], [minx, midy]]
        rec2 = [[midx, miny], [maxx, miny], [maxx, midy], [midx, midy]]
        rec3 = [[midx, midy], [maxx, midy], [maxx, maxy], [midx, maxy]]
        rec4 = [[minx, midy], [midx, midy], [midx, maxy], [minx, maxy]]
        
        split_mesh(elements1, rec1, maxnumelements, mesh, partition, rectangles)
        split_mesh(elements2, rec2, maxnumelements, mesh, partition, rectangles)
        split_mesh(elements3, rec3, maxnumelements, mesh, partition, rectangles)
        split_mesh(elements4, rec4, maxnumelements, mesh, partition, rectangles)

def print_partitioning(mesh, rectangles, figname):
    #prints the mesh with partitioning and saves the figure to figname
    fig = plt.figure(figsize=(20, 20))
    ax = fig.add_subplot()
    for elnr in list(range(mesh.ne)):
        xs = []
        ys = []
        el = mesh[ng.ElementId(ng.VOL,elnr)]
        for vertex in el.vertices:
            xs.append(mesh[ng.NodeId(ng.VERTEX,vertex.nr)].point[0])
            ys.append(mesh[ng.NodeId(ng.VERTEX,vertex.nr)].point[1])
        xs.append(xs[0])
        ys.append(ys[0])
        #ax.text((xs[0]+xs[1]+xs[2])/3-.02,(ys[0]+ys[1]+ys[2])/3,str(elnr))
        ax.plot(xs,ys)
    #add the rectangles in which the number of elements is <= maxnumelements
    for rec in rectangles:
        rec.append(rec[0])
        xs, ys = zip(*rec)
        ax.plot(xs, ys, color='black')
    plt.savefig(figname+'.png')
    print("plot generated")

def random_rhs(fes):
	rhs = ng.GridFunction(fes)
	randvec = rhs.vec.CreateVector()
	randvec.FV().NumPy()[:] = rd.rand(fes.ndof) * 2
	rhs.vec.data = randvec
	return rhs