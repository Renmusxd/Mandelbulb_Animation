import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from numba import jit
from tqdm import tqdm

# @jit
def circle(start = np.array([0.,0.,3.]), pts = 100):
	print(' :: Setting Up Path :: ')

	radius = np.sqrt(start_position[0]**2 + start_position[1]**2 + start_position[2]**2)
	theta = np.linspace(0, 2 * np.pi, pts) # increment angle along path
	x = start_position[0] * np.ones_like(theta) # start from start position
	y = start_position[1] * np.ones_like(theta) # start from start position
	z = start_position[2] * np.ones_like(theta) # start from start position

	for i in range(1,pts): # offset to handle 
		x[i] += radius * np.cos(theta[i]) - x[i-1]
		y[i] += radius * np.sin(theta[i]) - x[i-1]
	return(x,y,z)

if __name__=='__main__':
	# this all works great
	x,y,z = circle(pts = 10)
	fig = plt.figure()
	ax = fig.gca(projection='3d')
	ax.plot(x, y, z, color = 'r',label='Path0')
	ax.legend()
	fig.show()
	input(' :: Press <Enter> to continue :: ')



