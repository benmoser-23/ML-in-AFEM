from ngsolve import *
import pickle

filename = "initial_mesh"

file_mesh = open(filename, "rb")
mesh, gfu = pickle.load(file_mesh)
file_mesh.close

Draw(mesh)