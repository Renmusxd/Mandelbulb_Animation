import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from numba import jit
from tqdm import tqdm

# Path generating scripts. They all work, but only views has potential to work with bulb 
@jit
def looper(self, pts = 360):
	'''Makes circular path along great circle. Can only be used from a start point on z axis'''
	print(' :: Setting Up Circular Path :: ')
	radius = 3.0
	theta = np.linspace(0, 2 * np.pi, pts) # increment angle along path
	x = np.zeros_like(theta) # do this in polar, fix circle to y,z plane
	y = np.zeros_like(theta) # start from start position
	z = np.zeros_like(theta) # start from start position
	for i in range(pts): # offset to handle initial position
		y[i] += radius * np.sin(theta[i])
		z[i] += radius * np.cos(theta[i])
	return(x,y,z)

@jit
def elipse(pts = 360):
	'''Makes eliptical path between poles.'''
	print(' :: Setting Up Eliptical Path :: ')
	theta = np.linspace(0, 2 * np.pi, pts)
	# using equation for elipse in polar
	a = 4.0 # major axis
	b = 4.0 # minor axis
	radius = (a * b)/np.sqrt(b**2 * np.cos(theta)**2 + a**2 * np.sin(theta)**2)
	x = np.zeros_like(theta) # do this in polar, fix elipse to y,z plane
	y = radius * np.sin(theta)
	z = radius * np.cos(theta)
	return(x,y,z)

def views(pts = 1000):
	'''Sit at some views along a great circle while iterating'''
	print(' :: Setting Up View Points :: ')
	radius = 3.0
	theta = np.linspace(0, 2 * np.pi, 9) # increment angle along path
	x = np.zeros(pts) # do this in polar, fix circle to y,z plane
	y = np.zeros_like(x) # start from start position
	z = np.zeros_like(y) # start from start position
	for i in range(pts): # offset to handle initial position
		y[i] += radius * np.sin(theta[(9*i)//pts])
		z[i] += radius * np.cos(theta[(9*i)//pts])
	return(x,y,z)

if __name__=='__main__':
	x,y,z = elipse()
	print(y.size == z.size , y.shape == z.shape)
	fig = plt.figure()
	ax = fig.gca(projection = '3d')
	ax.plot(x,y,z, color = 'r',label = 'Path0')
	ax.legend()
	ax.set_xlim(-5,5)
	ax.set_ylim(-5,5)
	ax.set_zlim(-5,5)
	fig.show()
	input(' :: Press <Enter> to continue :: ')



