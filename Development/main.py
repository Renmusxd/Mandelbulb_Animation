from mandel import space
import numpy as np
import matplotlib.pyplot as plt 
from mpl_toolkits.mplot3d import Axes3D
import time 

def display(Vmax=10,n=8,itr=32):
	x,y,z = space(Vmax=Vmax, n=n, itr=itr)
	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')
	ax.scatter(x,y,z, c='r', marker='o')
	ax.set_xlabel('X Label')
	ax.set_ylabel('Y Label')
	ax.set_zlabel('Z Label')

	fig.show()
	t=time.perf_counter()
	input('Press <Enter> to exit')
	return(t)

if __name__=='__main__':
	t0 = time.perf_counter()
	t=display(Vmax=200,n=8)-t0 # keep Vmax^3 reasonable!
	print('Time elapsed during operation:', t ,'sec')