import numpy as np

losses_coord = np.load("losses_coord.npy")
losses_rhs = np.load("losses_coord+rhs.npy")
losses_sol = np.load("losses_coord+sol.npy")
losses_rhs_sol = np.load("losses_coord+sol+rhs.npy")

mean_losses_coord = sum(losses_coord)/len(losses_coord)
mean_losses_rhs = sum(losses_rhs)/len(losses_rhs)
mean_losses_sol = sum(losses_sol)/len(losses_sol)
mean_losses_rhs_sol = sum(losses_rhs_sol)/len(losses_rhs_sol)


#header of the table
output =  "\\begin{tabular}{|l|l|l|l|l|c|}\n"
output += "\\hline\n"
output += "input & \\multicolumn{4}{c|}{losses} & mean losses \\\\\n"
output += "\\hline\n"
#row for coordinates
output += "\\multirow{5}{8.5em}{\\small coordinates of elements} & \\footnotesize "
output += "{:.5f}".format(losses_coord[0])
output += " & \\footnotesize "
output += "{:.5f}".format(losses_coord[1])
output += " & \\footnotesize "
output += "{:.5f}".format(losses_coord[2])
output += " & \\footnotesize "
output += "{:.5f}".format(losses_coord[3])
output += " & \\multirow{5}{3.5em}{"
output += "{:.5f}".format(mean_losses_coord)
output += "} \\\\\n"
output += "\\cline{2-5}\n"
output += " & \\footnotesize "
output += "{:.5f}".format(losses_coord[4])
output += "& \\footnotesize "
output += "{:.5f}".format(losses_coord[5])
output += " & \\footnotesize "
output += "{:.5f}".format(losses_coord[6])
output += " & \\footnotesize "
output += "{:.5f}".format(losses_coord[7])
output += " & \\\\\n"
output += "\\cline{2-5}\n"
output += " & \\footnotesize "
output += "{:.5f}".format(losses_coord[8])
output += "& \\footnotesize "
output += "{:.5f}".format(losses_coord[9])
output += " & \\footnotesize "
output += "{:.5f}".format(losses_coord[10])
output += " & \\footnotesize "
output += "{:.5f}".format(losses_coord[11])
output += " & \\\\\n"
output += "\\cline{2-5}\n"
output += " & \\footnotesize "
output += "{:.5f}".format(losses_coord[12])
output += "& \\footnotesize "
output += "{:.5f}".format(losses_coord[13])
output += " & \\footnotesize "
output += "{:.5f}".format(losses_coord[14])
output += " & \\footnotesize "
output += "{:.5f}".format(losses_coord[15])
output += " & \\\\\n"
output += "\\cline{2-5}\n"
output += " & \\footnotesize "
output += "{:.5f}".format(losses_coord[16])
output += "& \\footnotesize "
output += "{:.5f}".format(losses_coord[17])
output += " & \\footnotesize "
output += "{:.5f}".format(losses_coord[18])
output += " & \\footnotesize "
output += "{:.5f}".format(losses_coord[19])
output += " & \\\\\n"
output += "\\hline\n"
#row for +rhs
output += "\\multirow{5}{8.5em}{\\small coordinates of elements + RHS} & \\footnotesize "
output += "{:.5f}".format(losses_rhs[0])
output += " & \\footnotesize "
output += "{:.5f}".format(losses_rhs[1])
output += " & \\footnotesize "
output += "{:.5f}".format(losses_rhs[2])
output += " & \\footnotesize "
output += "{:.5f}".format(losses_rhs[3])
output += " & \\multirow{5}{3.5em}{"
output += "{:.5f}".format(mean_losses_rhs)
output += "} \\\\\n"
output += "\\cline{2-5}\n"
output += "& \\footnotesize "
output += "{:.5f}".format(losses_rhs[4])
output += " & \\footnotesize "
output += "{:.5f}".format(losses_rhs[5])
output += " & \\footnotesize "
output += "{:.5f}".format(losses_rhs[6])
output += " & \\footnotesize "
output += "{:.5f}".format(losses_rhs[7])
output += " & \\\\\n"
output += "\\cline{2-5}\n"
output += " & \\footnotesize "
output += "{:.5f}".format(losses_rhs[8])
output += "& \\footnotesize "
output += "{:.5f}".format(losses_rhs[9])
output += " & \\footnotesize "
output += "{:.5f}".format(losses_rhs[10])
output += " & \\footnotesize "
output += "{:.5f}".format(losses_rhs[11])
output += " & \\\\\n"
output += "\\cline{2-5}\n"
output += " & \\footnotesize "
output += "{:.5f}".format(losses_rhs[12])
output += "& \\footnotesize "
output += "{:.5f}".format(losses_rhs[13])
output += " & \\footnotesize "
output += "{:.5f}".format(losses_rhs[14])
output += " & \\footnotesize "
output += "{:.5f}".format(losses_rhs[15])
output += " & \\\\\n"
output += "\\cline{2-5}\n"
output += " & \\footnotesize "
output += "{:.5f}".format(losses_rhs[16])
output += "& \\footnotesize "
output += "{:.5f}".format(losses_rhs[17])
output += " & \\footnotesize "
output += "{:.5f}".format(losses_rhs[18])
output += " & \\footnotesize "
output += "{:.5f}".format(losses_rhs[19])
output += " & \\\\\n"
output += "\\hline\n"
#row for +sol
output += "\\multirow{5}{8.5em}{\\small coordinates of elements + solution} & \\footnotesize "
output += "{:.5f}".format(losses_sol[0])
output += " & \\footnotesize "
output += "{:.5f}".format(losses_sol[1])
output += " & \\footnotesize "
output += "{:.5f}".format(losses_sol[2])
output += " & \\footnotesize "
output += "{:.5f}".format(losses_sol[3])
output += " & \\multirow{5}{3.5em}{"
output += "{:.5f}".format(mean_losses_sol)
output += "} \\\\\n"
output += "\\cline{2-5}\n"
output += " & \\footnotesize "
output += "{:.5f}".format(losses_sol[4])
output += "& \\footnotesize "
output += "{:.5f}".format(losses_sol[5])
output += " & \\footnotesize "
output += "{:.5f}".format(losses_sol[6])
output += " & \\footnotesize "
output += "{:.5f}".format(losses_sol[7])
output += " & \\\\\n"
output += "\\cline{2-5}\n"
output += " & \\footnotesize "
output += "{:.5f}".format(losses_sol[8])
output += "& \\footnotesize "
output += "{:.5f}".format(losses_sol[9])
output += " & \\footnotesize "
output += "{:.5f}".format(losses_sol[10])
output += " & \\footnotesize "
output += "{:.5f}".format(losses_sol[11])
output += " & \\\\\n"
output += "\\cline{2-5}\n"
output += " & \\footnotesize "
output += "{:.5f}".format(losses_sol[12])
output += "& \\footnotesize "
output += "{:.5f}".format(losses_sol[13])
output += " & \\footnotesize "
output += "{:.5f}".format(losses_sol[14])
output += " & \\footnotesize "
output += "{:.5f}".format(losses_sol[15])
output += " & \\\\\n"
output += "\\cline{2-5}\n"
output += " & \\footnotesize "
output += "{:.5f}".format(losses_sol[16])
output += "& \\footnotesize "
output += "{:.5f}".format(losses_sol[17])
output += " & \\footnotesize "
output += "{:.5f}".format(losses_sol[18])
output += " & \\footnotesize "
output += "{:.5f}".format(losses_sol[19])
output += " & \\\\\n"
output += "\\hline\n"
#row for +sol+rhs
output += "\\multirow{5}{8.5em}{\\small coordinates of elements + RHS and solution} & \\footnotesize "
output += "{:.5f}".format(losses_rhs_sol[0])
output += " & \\footnotesize "
output += "{:.5f}".format(losses_rhs_sol[1])
output += " & \\footnotesize "
output += "{:.5f}".format(losses_rhs_sol[2])
output += " & \\footnotesize "
output += "{:.5f}".format(losses_rhs_sol[3])
output += " & \\multirow{5}{3.5em}{"
output += "{:.5f}".format(mean_losses_rhs_sol)
output += "} \\\\\n"
output += "\\cline{2-5}\n"
output += " & \\footnotesize "
output += "{:.5f}".format(losses_rhs_sol[4])
output += "& \\footnotesize "
output += "{:.5f}".format(losses_rhs_sol[5])
output += " & \\footnotesize "
output += "{:.5f}".format(losses_rhs_sol[6])
output += " & \\footnotesize "
output += "{:.5f}".format(losses_rhs_sol[7])
output += " & \\\\\n"
output += "\\cline{2-5}\n"
output += " & \\footnotesize "
output += "{:.5f}".format(losses_rhs_sol[8])
output += "& \\footnotesize "
output += "{:.5f}".format(losses_rhs_sol[9])
output += " & \\footnotesize "
output += "{:.5f}".format(losses_rhs_sol[10])
output += " & \\footnotesize "
output += "{:.5f}".format(losses_rhs_sol[11])
output += " & \\\\\n"
output += "\\cline{2-5}\n"
output += " & \\footnotesize "
output += "{:.5f}".format(losses_rhs_sol[12])
output += "& \\footnotesize "
output += "{:.5f}".format(losses_rhs_sol[13])
output += " & \\footnotesize "
output += "{:.5f}".format(losses_rhs_sol[14])
output += " & \\footnotesize "
output += "{:.5f}".format(losses_rhs_sol[15])
output += " & \\\\\n"
output += "\\cline{2-5}\n"
output += " & \\footnotesize "
output += "{:.5f}".format(losses_rhs_sol[16])
output += "& \\footnotesize "
output += "{:.5f}".format(losses_rhs_sol[17])
output += " & \\footnotesize "
output += "{:.5f}".format(losses_rhs_sol[18])
output += " & \\footnotesize "
output += "{:.5f}".format(losses_rhs_sol[19])
output += " & \\\\\n"
output += "\\hline\n"
output += "\\end{tabular}"

table = open("table_losses.txt","w")
table.write(output)
table.close()

print("------------------------------------------------------------------------------------")
print("coordinates:")
print(losses_coord)
print("mean:")
print(mean_losses_coord)
print("------------------------------------------------------------------------------------")
print("+rhs:")
print(losses_rhs)
print("mean:")
print(mean_losses_rhs)
print("------------------------------------------------------------------------------------")
print("+sol:")
print(losses_sol)
print("mean:")
print(mean_losses_sol)
print("------------------------------------------------------------------------------------")
print("+rhs+sol:")
print(losses_rhs_sol)
print("mean:")
print(mean_losses_rhs_sol)
print("------------------------------------------------------------------------------------")