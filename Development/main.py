from mandelset import space
import numpy as np
import matplotlib.pyplot as plt 
from mpl_toolkits.mplot3d import Axes3D
import time 

def display(Vmax=10):
	t0=time.perf_counter()
	x,y,z = space(Vmax)
	t=time.perf_counter()-t0
	print('Time elapsed During space generation:', t ,'sec')

	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')
	ax.scatter(x,y,z, marker='o')
	ax.set_xlabel('X Label')
	ax.set_ylabel('Y Label')
	ax.set_zlabel('Z Label')

	fig.show()
	input('Press <Enter> to exit')

if __name__=='__main__':
	display()