import numpy as np
from matplotlib import cm
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class Cinder:
	'''Class for Cyllinder Object Creation'''

	def __init__(self,radius=1,height=1,meshsize=100):
		self.r=radius
		self.h=height
		self.ms=meshsize
		self.cyl_mesh()
		self.cyl_plot()
	
	def cyl_mesh(self):
		'''Make the mesh for a cyllinder, generate the datapoints'''
		 # generate the domain of thetas 
		x = np.linspace(0,self.r,self.ms)
		z = np.linspace(0,self.h,self.ms)
		X,Z=np.meshgrid(x,z)
		print(X,Z)
		Y = np.sqrt(self.r**2-X**2)
		self.meshed=X,Y,Z

	def cyl_plot(self):
		x,y,z=self.meshed
		fig = plt.figure()
		ax = fig.add_subplot(111, projection='3d')
		surface = ax.plot_surface(x, y, z, cmap=cm.hot_r,linewidth=0, antialiased=False,alpha=0.2, rstride=self.r, cstride=self.h)
		fig.colorbar(surface, shrink=0.5, aspect=5)
		self.fig=fig
		self.ax=ax

	def display(self):
		plt.show()

if __name__=='__main__':
	pass