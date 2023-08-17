import numpy as np
import matplotlib.pyplot as plt

losses_coord = np.load("losses_coord.npy")
losses_rhs = np.load("losses_coord+rhs.npy")
losses_sol = np.load("losses_coord+sol.npy")
losses_rhs_sol = np.load("losses_coord+sol+rhs.npy")

losses = np.transpose(np.array([losses_coord,
								losses_rhs,
								losses_sol,
								losses_rhs_sol]))

print(np.shape(losses))
print(losses)
print(np.shape(losses)[0])

q25, q75 = np.percentile(losses, [25, 75])
bin_width = 2 * (q75 - q25) * len(losses[0]) ** (-1/3)
bins = round((losses.max() - losses.min()) / bin_width)
print("Freedman–Diaconis number of bins:", bins)

plt.hist(losses,
		 bins = bins,
		 histtype='bar', 
		 label=['case 1', 'case 2', 'case 3', 'case 4'])
plt.legend(prop={'size': 10})
plt.title('random domain, fixed right hand side')
plt.ylabel('number of networks')
plt.xlabel('accuracies')

plt.savefig('histogram_rand-domain_fixed-rhs.png')