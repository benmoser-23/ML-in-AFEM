import numpy as np

accuracies_coord = np.load("accuracies_coord.npy")
accuracies_rhs = np.load("accuracies_coord+rhs.npy")
accuracies_sol = np.load("accuracies_coord+sol.npy")
accuracies_rhs_sol = np.load("accuracies_coord+sol+rhs.npy")

mean_coord = sum(accuracies_coord)/len(accuracies_coord)
mean_rhs = sum(accuracies_rhs)/len(accuracies_rhs)
mean_sol = sum(accuracies_sol)/len(accuracies_sol)
mean_rhs_sol = sum(accuracies_rhs_sol)/len(accuracies_rhs_sol)

#header of the table
output =  "\\begin{tabular}{|l|l|l|l|l|l|c|}\n"
output += "\\hline\n"
output += "input & \\multicolumn{5}{c|}{accuracies} & mean accuracy \\\\\n"
output += "\\hline\n"
#row for coordinates
output += "\\multirow{2}{4.9em}{\\small coordinates} & \\footnotesize "
output += "{:.5f}".format(accuracies_coord[0])
output += " & \\footnotesize "
output += "{:.5f}".format(accuracies_coord[1])
output += " & \\footnotesize "
output += "{:.5f}".format(accuracies_coord[2])
output += " & \\footnotesize "
output += "{:.5f}".format(accuracies_coord[3])
output += " & \\footnotesize "
output += "{:.5f}".format(accuracies_coord[4])
output += " & \\multirow{2}{3.5em}{"
output += "{:.5f}".format(mean_coord)
output += "} \\\\\n"
output += "\\cline{2-6}\n"
output += "& \\footnotesize "
output += "{:.5f}".format(accuracies_coord[5])
output += " & \\footnotesize "
output += "{:.5f}".format(accuracies_coord[6])
output += " & \\footnotesize "
output += "{:.5f}".format(accuracies_coord[7])
output += " & \\footnotesize "
output += "{:.5f}".format(accuracies_coord[8])
output += " & \\footnotesize "
output += "{:.5f}".format(accuracies_coord[9])
output += " & \\\\\n"
output += "\\hline\n"
#row for +rhs
output += "\\multirow{2}{4.9em}{\\small + RHS} & \\footnotesize "
output += "{:.5f}".format(accuracies_rhs[0])
output += " & \\footnotesize "
output += "{:.5f}".format(accuracies_rhs[1])
output += " & \\footnotesize "
output += "{:.5f}".format(accuracies_rhs[2])
output += " & \\footnotesize "
output += "{:.5f}".format(accuracies_rhs[3])
output += " & \\footnotesize "
output += "{:.5f}".format(accuracies_rhs[4])
output += " & \\multirow{2}{3.5em}{"
output += "{:.5f}".format(mean_rhs)
output += "} \\\\\n"
output += "\\cline{2-6}\n"
output += "& \\footnotesize "
output += "{:.5f}".format(accuracies_rhs[5])
output += " & \\footnotesize "
output += "{:.5f}".format(accuracies_rhs[6])
output += " & \\footnotesize "
output += "{:.5f}".format(accuracies_rhs[7])
output += " & \\footnotesize "
output += "{:.5f}".format(accuracies_rhs[8])
output += " & \\footnotesize "
output += "{:.5f}".format(accuracies_rhs[9])
output += " & \\\\\n"
output += "\\hline\n"
#row for +sol
output += "\\multirow{2}{4.9em}{\\small + solution} & \\footnotesize "
output += "{:.5f}".format(accuracies_sol[0])
output += " & \\footnotesize "
output += "{:.5f}".format(accuracies_sol[1])
output += " & \\footnotesize "
output += "{:.5f}".format(accuracies_sol[2])
output += " & \\footnotesize "
output += "{:.5f}".format(accuracies_sol[3])
output += " & \\footnotesize "
output += "{:.5f}".format(accuracies_sol[4])
output += " & \\multirow{2}{3.5em}{"
output += "{:.5f}".format(mean_sol)
output += "} \\\\\n"
output += "\\cline{2-6}\n"
output += "& \\footnotesize "
output += "{:.5f}".format(accuracies_sol[5])
output += " & \\footnotesize "
output += "{:.5f}".format(accuracies_sol[6])
output += " & \\footnotesize "
output += "{:.5f}".format(accuracies_sol[7])
output += " & \\footnotesize "
output += "{:.5f}".format(accuracies_sol[8])
output += " & \\footnotesize "
output += "{:.5f}".format(accuracies_sol[9])
output += " & \\\\\n"
output += "\\hline\n"
#row for +sol+rhs
output += "\\multirow{2}{4.9em}{\\small + RHS and solution} & \\footnotesize "
output += "{:.5f}".format(accuracies_rhs_sol[0])
output += " & \\footnotesize "
output += "{:.5f}".format(accuracies_rhs_sol[1])
output += " & \\footnotesize "
output += "{:.5f}".format(accuracies_rhs_sol[2])
output += " & \\footnotesize "
output += "{:.5f}".format(accuracies_rhs_sol[3])
output += " & \\footnotesize "
output += "{:.5f}".format(accuracies_rhs_sol[4])
output += " & \\multirow{2}{3.5em}{"
output += "{:.5f}".format(mean_rhs_sol)
output += "} \\\\\n"
output += "\\cline{2-6}\n"
output += "& \\footnotesize "
output += "{:.5f}".format(accuracies_rhs_sol[5])
output += " & \\footnotesize "
output += "{:.5f}".format(accuracies_rhs_sol[6])
output += " & \\footnotesize "
output += "{:.5f}".format(accuracies_rhs_sol[7])
output += " & \\footnotesize "
output += "{:.5f}".format(accuracies_rhs_sol[8])
output += " & \\footnotesize "
output += "{:.5f}".format(accuracies_rhs_sol[9])
output += " & \\\\\n"
output += "\\hline\n"
output += "\\end{tabular}"

table = open("table.txt","w")
table.write(output)
table.close()

print("------------------------------------------------------------------------------------")
print("coordinates:")
print(accuracies_coord)
print("mean:")
print(mean_coord)
print("------------------------------------------------------------------------------------")
print("+rhs:")
print(accuracies_rhs)
print("mean:")
print(mean_rhs)
print("------------------------------------------------------------------------------------")
print("+sol:")
print(accuracies_sol)
print("mean:")
print(mean_sol)
print("------------------------------------------------------------------------------------")
print("+rhs+sol:")
print(accuracies_rhs_sol)
print("mean:")
print(mean_rhs_sol)
print("------------------------------------------------------------------------------------")