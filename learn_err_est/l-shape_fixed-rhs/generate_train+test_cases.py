from ngsolve import *
from netgen.geom2d import SplineGeometry
import random
import numpy as np
import os

#create L-shape geometry
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

#function for calculating elementwise error estimator
def ResidualEstimator():
    print("+++++++++++++++++++++++++++++++++++")
    print("CALCULATING ERROR ESTIMATOR")

    V2 = L2(mesh, order=order-1)

    gradu_x = GridFunction(V2)
    gradu_y = GridFunction(V2)

    Sigma = HDiv(mesh, order=order-1)
    X = FESpace([fes,Sigma])

    u2, sigma = X.TrialFunction()
    v2, tau = X.TestFunction()
    n = specialcf.normal(2)

    asig = BilinearForm(X)
    asig += SymbolicBFI (u2*v2)
    asig += SymbolicBFI (1e-4 * sigma*tau)
    asig += SymbolicBFI ( 0.5*(sigma*n)*(tau*n), element_boundary=True)

    amixed = BilinearForm(X)
    amixed += SymbolicBFI ((tau*n) * (n* (grad(u2)-grad(u2).Other())), VOL, skeleton=True)
    sigma = GridFunction(X, name="lifted_jumps")

    gradu_x.Set(gfu.Deriv()[0])
    gradu_y.Set(gfu.Deriv()[1])

    h = specialcf.mesh_size

    laplace_u = gradu_x.Deriv()[0] + gradu_y.Deriv()[1]

    eta_vol_element = Integrate(h*h * (f + laplace_u)*(f + laplace_u), mesh, element_wise=True)

    asig.Assemble()

    hv1 = sigma.vec.CreateVector()
    hv2 = sigma.vec.CreateVector()

    hv1[:] = 0
    hv1[X.Range(0)] = gfu.vec
    amixed.Apply (hv1, hv2)
    sigma.vec.data = asig.mat.Inverse() * hv2

    sigma2 = sigma.components[1]
    eta_edge_element = Integrate (sigma2*sigma2, mesh, element_wise=True)

    return eta_vol_element + eta_edge_element

#function for calculating fem solution 
def SolvePoisson():
    fes.Update()
    print("###################################")
    print("SOLVING POISSON")
    print("###################################")
    gfu.Update()
    a.Assemble()
    f_lf.Assemble()
    gfu.vec.data = a.mat.Inverse(freedofs=fes.FreeDofs()) * f_lf.vec

#some numbers
numTrainMeshes = 4000
numTestMeshes = 1000
maxNumElements = 1000
train_meshes = []
train_estimates = []
test_meshes = []
test_estimates = []

#set seed to make it replicable
random.seed(12345)

#loop to generate train cases
while len(train_meshes) < numTrainMeshes:
    mesh = Mesh(geo.GenerateMesh(maxh=0.9))

    for i in range(random.choice([1,2,3])):
        M = [random.choice([True, False, False]) for k in range(mesh.ne)]
        for k, el in enumerate(mesh.Elements()):
            mesh.SetRefinementFlag(el, M[k])
        mesh.Refine()

    order = 1
    fes = H1(mesh, order=order, dirichlet=".*")
    u, v = fes.TnT()
    gfu = GridFunction(fes)

    a = BilinearForm(fes, symmetric=True)
    a += grad(u)*grad(v)*dx

    f = x
    f_lf = LinearForm(fes)
    f_lf += f*v*dx

    coordinates = []
    
    if mesh.ne <= maxNumElements:

        SolvePoisson()

        for el in mesh.Elements(VOL):
            for vertex in el.vertices:
                for coord in mesh[NodeId(VERTEX,vertex.nr)].point:
                    coordinates.append(coord)
                coordinates.append(f(mesh(coordinates[-2],coordinates[-1])))
                coordinates.append(gfu(coordinates[-3],coordinates[-2]))  

        coordinates.extend([0] * (12*maxNumElements-len(coordinates)))
        train_meshes.append(coordinates)

        eta_element = ResidualEstimator()
        eta = sqrt(sum(eta_element))
        print("error estimator: ", eta)
        print("+++++++++++++++++++++++++++++++++++")
        train_estimates.append(eta)

        print("----------------------------------------------------------------------")
        print("----------------------------------------------------------------------")
        print('generating training data, current number of train meshes: ', len(train_meshes), '/', numTrainMeshes)
        print('number of elements: ', mesh.ne)
        print("----------------------------------------------------------------------")
        print("----------------------------------------------------------------------")
    else:
        print("xxxxxxxxxxxxxxxx")
        print('too many elements')
        print('number of elements: ', mesh.ne)
        print("xxxxxxxxxxxxxxxx")
        Draw(mesh)

#loop to generate test cases
while len(test_meshes) < numTestMeshes:
    mesh = Mesh(geo.GenerateMesh(maxh=0.9))

    for i in range(random.choice([1,2,3])):
        M = [random.choice([True, False, False]) for k in range(mesh.ne)]
        for k, el in enumerate(mesh.Elements()):
            mesh.SetRefinementFlag(el, M[k])
        mesh.Refine()

    order = 1
    fes = H1(mesh, order=order, dirichlet=".*")
    u, v = fes.TnT()
    gfu = GridFunction(fes)

    a = BilinearForm(fes, symmetric=True)
    a += grad(u)*grad(v)*dx

    f = x
    f_lf = LinearForm(fes)
    f_lf += f*v*dx

    coordinates = []
    
    if mesh.ne <= maxNumElements:

        SolvePoisson()

        for el in mesh.Elements(VOL):
            for vertex in el.vertices:
                for coord in mesh[NodeId(VERTEX,vertex.nr)].point:
                    coordinates.append(coord)
                coordinates.append(f(mesh(coordinates[-2],coordinates[-1])))
                coordinates.append(gfu(coordinates[-3],coordinates[-2]))     

        coordinates.extend([0] * (12*maxNumElements-len(coordinates)))
        test_meshes.append(coordinates)

        eta_element = ResidualEstimator()
        eta = sqrt(sum(eta_element))
        print("error estimator: ", eta)
        print("+++++++++++++++++++++++++++++++++++")
        test_estimates.append(eta)

        print("----------------------------------------------------------------------")
        print("----------------------------------------------------------------------")
        print('generating test data, current number of test meshes: ', len(test_meshes), '/', numTestMeshes)
        print('number of elements: ', mesh.ne)
        print("----------------------------------------------------------------------")
        print("----------------------------------------------------------------------")
    else:
        print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
        print('too many elements')
        print('number of elements: ', mesh.ne)
        print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
        Draw(mesh)

print("")
print("saving training and test data into file...")
print("mean value of train estimates:", sum(train_estimates)/len(train_estimates))
print("mean value of test estimates:", sum(test_estimates)/len(test_estimates))
np.save('train_meshes',np.array(train_meshes))
np.save('train_estimates',np.array(train_estimates))
np.save('test_meshes',np.array(test_meshes))
np.save('test_estimates',np.array(test_estimates))
print("DONE")
print('\007')