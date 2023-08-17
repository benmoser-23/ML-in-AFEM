import numpy as np

accuracies_coord = np.load("accuracies_coord.npy")
accuracies_rhs = np.load("accuracies_coord+rhs.npy")
accuracies_sol = np.load("accuracies_coord+sol.npy")
accuracies_rhs_sol = np.load("accuracies_coord+sol+rhs.npy")

mean_accuracies_coord = sum(accuracies_coord)/len(accuracies_coord)
mean_accuracies_rhs = sum(accuracies_rhs)/len(accuracies_rhs)
mean_accuracies_sol = sum(accuracies_sol)/len(accuracies_sol)
mean_accuracies_rhs_sol = sum(accuracies_rhs_sol)/len(accuracies_rhs_sol)


#header of the table
output =  "\\begin{tabular}{|l|l|l|l|l|c|}\n"
output += "\\hline\n"
output += "input & \\multicolumn{4}{c|}{accuracies} & mean accuracies \\\\\n"
output += "\\hline\n"
#row for coordinates
output += "\\multirow{5}{8.5em}{\\small coordinates of elements} & \\footnotesize "
output += "{:.5f}".format(accuracies_coord[0])
output += " & \\footnotesize "
output += "{:.5f}".format(accuracies_coord[1])
output += " & \\footnotesize "
output += "{:.5f}".format(accuracies_coord[2])
output += " & \\footnotesize "
output += "{:.5f}".format(accuracies_coord[3])
output += " & \\multirow{5}{3.5em}{"
output += "{:.5f}".format(mean_accuracies_coord)
output += "} \\\\\n"
output += "\\cline{2-5}\n"
output += " & \\footnotesize "
output += "{:.5f}".format(accuracies_coord[4])
output += "& \\footnotesize "
output += "{:.5f}".format(accuracies_coord[5])
output += " & \\footnotesize "
output += "{:.5f}".format(accuracies_coord[6])
output += " & \\footnotesize "
output += "{:.5f}".format(accuracies_coord[7])
output += " & \\\\\n"
output += "\\cline{2-5}\n"
output += " & \\footnotesize "
output += "{:.5f}".format(accuracies_coord[8])
output += "& \\footnotesize "
output += "{:.5f}".format(accuracies_coord[9])
output += " & \\footnotesize "
output += "{:.5f}".format(accuracies_coord[10])
output += " & \\footnotesize "
output += "{:.5f}".format(accuracies_coord[11])
output += " & \\\\\n"
output += "\\cline{2-5}\n"
output += " & \\footnotesize "
output += "{:.5f}".format(accuracies_coord[12])
output += "& \\footnotesize "
output += "{:.5f}".format(accuracies_coord[13])
output += " & \\footnotesize "
output += "{:.5f}".format(accuracies_coord[14])
output += " & \\footnotesize "
output += "{:.5f}".format(accuracies_coord[15])
output += " & \\\\\n"
output += "\\cline{2-5}\n"
output += " & \\footnotesize "
output += "{:.5f}".format(accuracies_coord[16])
output += "& \\footnotesize "
output += "{:.5f}".format(accuracies_coord[17])
output += " & \\footnotesize "
output += "{:.5f}".format(accuracies_coord[18])
output += " & \\footnotesize "
output += "{:.5f}".format(accuracies_coord[19])
output += " & \\\\\n"
output += "\\hline\n"
#row for +rhs
output += "\\multirow{5}{8.5em}{\\small coordinates of elements + RHS} & \\footnotesize "
output += "{:.5f}".format(accuracies_rhs[0])
output += " & \\footnotesize "
output += "{:.5f}".format(accuracies_rhs[1])
output += " & \\footnotesize "
output += "{:.5f}".format(accuracies_rhs[2])
output += " & \\footnotesize "
output += "{:.5f}".format(accuracies_rhs[3])
output += " & \\multirow{5}{3.5em}{"
output += "{:.5f}".format(mean_accuracies_rhs)
output += "} \\\\\n"
output += "\\cline{2-5}\n"
output += "& \\footnotesize "
output += "{:.5f}".format(accuracies_rhs[4])
output += " & \\footnotesize "
output += "{:.5f}".format(accuracies_rhs[5])
output += " & \\footnotesize "
output += "{:.5f}".format(accuracies_rhs[6])
output += " & \\footnotesize "
output += "{:.5f}".format(accuracies_rhs[7])
output += " & \\\\\n"
output += "\\cline{2-5}\n"
output += " & \\footnotesize "
output += "{:.5f}".format(accuracies_rhs[8])
output += "& \\footnotesize "
output += "{:.5f}".format(accuracies_rhs[9])
output += " & \\footnotesize "
output += "{:.5f}".format(accuracies_rhs[10])
output += " & \\footnotesize "
output += "{:.5f}".format(accuracies_rhs[11])
output += " & \\\\\n"
output += "\\cline{2-5}\n"
output += " & \\footnotesize "
output += "{:.5f}".format(accuracies_rhs[12])
output += "& \\footnotesize "
output += "{:.5f}".format(accuracies_rhs[13])
output += " & \\footnotesize "
output += "{:.5f}".format(accuracies_rhs[14])
output += " & \\footnotesize "
output += "{:.5f}".format(accuracies_rhs[15])
output += " & \\\\\n"
output += "\\cline{2-5}\n"
output += " & \\footnotesize "
output += "{:.5f}".format(accuracies_rhs[16])
output += "& \\footnotesize "
output += "{:.5f}".format(accuracies_rhs[17])
output += " & \\footnotesize "
output += "{:.5f}".format(accuracies_rhs[18])
output += " & \\footnotesize "
output += "{:.5f}".format(accuracies_rhs[19])
output += " & \\\\\n"
output += "\\hline\n"
#row for +sol
output += "\\multirow{5}{8.5em}{\\small coordinates of elements + solution} & \\footnotesize "
output += "{:.5f}".format(accuracies_sol[0])
output += " & \\footnotesize "
output += "{:.5f}".format(accuracies_sol[1])
output += " & \\footnotesize "
output += "{:.5f}".format(accuracies_sol[2])
output += " & \\footnotesize "
output += "{:.5f}".format(accuracies_sol[3])
output += " & \\multirow{5}{3.5em}{"
output += "{:.5f}".format(mean_accuracies_sol)
output += "} \\\\\n"
output += "\\cline{2-5}\n"
output += " & \\footnotesize "
output += "{:.5f}".format(accuracies_sol[4])
output += "& \\footnotesize "
output += "{:.5f}".format(accuracies_sol[5])
output += " & \\footnotesize "
output += "{:.5f}".format(accuracies_sol[6])
output += " & \\footnotesize "
output += "{:.5f}".format(accuracies_sol[7])
output += " & \\\\\n"
output += "\\cline{2-5}\n"
output += " & \\footnotesize "
output += "{:.5f}".format(accuracies_sol[8])
output += "& \\footnotesize "
output += "{:.5f}".format(accuracies_sol[9])
output += " & \\footnotesize "
output += "{:.5f}".format(accuracies_sol[10])
output += " & \\footnotesize "
output += "{:.5f}".format(accuracies_sol[11])
output += " & \\\\\n"
output += "\\cline{2-5}\n"
output += " & \\footnotesize "
output += "{:.5f}".format(accuracies_sol[12])
output += "& \\footnotesize "
output += "{:.5f}".format(accuracies_sol[13])
output += " & \\footnotesize "
output += "{:.5f}".format(accuracies_sol[14])
output += " & \\footnotesize "
output += "{:.5f}".format(accuracies_sol[15])
output += " & \\\\\n"
output += "\\cline{2-5}\n"
output += " & \\footnotesize "
output += "{:.5f}".format(accuracies_sol[16])
output += "& \\footnotesize "
output += "{:.5f}".format(accuracies_sol[17])
output += " & \\footnotesize "
output += "{:.5f}".format(accuracies_sol[18])
output += " & \\footnotesize "
output += "{:.5f}".format(accuracies_sol[19])
output += " & \\\\\n"
output += "\\hline\n"
#row for +sol+rhs
output += "\\multirow{5}{8.5em}{\\small coordinates of elements + RHS and solution} & \\footnotesize "
output += "{:.5f}".format(accuracies_rhs_sol[0])
output += " & \\footnotesize "
output += "{:.5f}".format(accuracies_rhs_sol[1])
output += " & \\footnotesize "
output += "{:.5f}".format(accuracies_rhs_sol[2])
output += " & \\footnotesize "
output += "{:.5f}".format(accuracies_rhs_sol[3])
output += " & \\multirow{5}{3.5em}{"
output += "{:.5f}".format(mean_accuracies_rhs_sol)
output += "} \\\\\n"
output += "\\cline{2-5}\n"
output += " & \\footnotesize "
output += "{:.5f}".format(accuracies_rhs_sol[4])
output += "& \\footnotesize "
output += "{:.5f}".format(accuracies_rhs_sol[5])
output += " & \\footnotesize "
output += "{:.5f}".format(accuracies_rhs_sol[6])
output += " & \\footnotesize "
output += "{:.5f}".format(accuracies_rhs_sol[7])
output += " & \\\\\n"
output += "\\cline{2-5}\n"
output += " & \\footnotesize "
output += "{:.5f}".format(accuracies_rhs_sol[8])
output += "& \\footnotesize "
output += "{:.5f}".format(accuracies_rhs_sol[9])
output += " & \\footnotesize "
output += "{:.5f}".format(accuracies_rhs_sol[10])
output += " & \\footnotesize "
output += "{:.5f}".format(accuracies_rhs_sol[11])
output += " & \\\\\n"
output += "\\cline{2-5}\n"
output += " & \\footnotesize "
output += "{:.5f}".format(accuracies_rhs_sol[12])
output += "& \\footnotesize "
output += "{:.5f}".format(accuracies_rhs_sol[13])
output += " & \\footnotesize "
output += "{:.5f}".format(accuracies_rhs_sol[14])
output += " & \\footnotesize "
output += "{:.5f}".format(accuracies_rhs_sol[15])
output += " & \\\\\n"
output += "\\cline{2-5}\n"
output += " & \\footnotesize "
output += "{:.5f}".format(accuracies_rhs_sol[16])
output += "& \\footnotesize "
output += "{:.5f}".format(accuracies_rhs_sol[17])
output += " & \\footnotesize "
output += "{:.5f}".format(accuracies_rhs_sol[18])
output += " & \\footnotesize "
output += "{:.5f}".format(accuracies_rhs_sol[19])
output += " & \\\\\n"
output += "\\hline\n"
output += "\\end{tabular}"

table = open("table_accuracies.txt","w")
table.write(output)
table.close()

print("------------------------------------------------------------------------------------")
print("coordinates:")
print(accuracies_coord)
print("mean:")
print(mean_accuracies_coord)
print("------------------------------------------------------------------------------------")
print("+rhs:")
print(accuracies_rhs)
print("mean:")
print(mean_accuracies_rhs)
print("------------------------------------------------------------------------------------")
print("+sol:")
print(accuracies_sol)
print("mean:")
print(mean_accuracies_sol)
print("------------------------------------------------------------------------------------")
print("+rhs+sol:")
print(accuracies_rhs_sol)
print("mean:")
print(mean_accuracies_rhs_sol)
print("------------------------------------------------------------------------------------")