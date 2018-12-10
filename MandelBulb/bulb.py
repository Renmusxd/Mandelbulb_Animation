import numpy as np
import matplotlib.pyplot as plt
from numba import jit
import scipy.misc
import os

class Bulb(object):
	'''Generate individual images of the Mandelbulb set with ray tracing.'''
	def __init__(self,degree=8, observer_position=np.array([0., 0., 3.]), max_steps=32, iterations=32, bailout=2**20, min_distance=5e-4, zoom=0, power=0.2, imsize = 500, x_size=500, y_size=500, span=[1.2, 1.2], center=[0, 0], counter=0, cm='gray', color_map =[1,0,1,0,1,0], grad=False):
		'''Initializes config variables for bulb object'''
		self.cm = cm # choose the colormap for the resultant bulb from in colordict presets
		self.itr = iterations # Constraint: number iterations before we decide a point under recursion formula is bounded or not by bail, i.e in set.
		self.deg = degree  # the power n used in the recursive formula V --> V^n + C any degree >= 0 works, but smaller degree uses more iterations
		self.span = span # another control of zoom of picture, numerator term
		self.grad = grad # colorgradient
		self.maxs = max_steps
		self.mind = min_distance # minimum distance from observer position that is considered a 
		self.bail = bailout # Constraint: points within the bulb set need to stay within bailout, a radius, over 32 iterations.
		self.zoom = zoom # controls zoom, denominator term
		self.obpos = observer_position # literally the position in space the observer would be in resultant png. Used for ray tracing source position.
		self.power = power 
		self.width = imsize # image width and resolution (always a square)
		self.xsize = x_size # same as width but used in different context
		self.ysize = y_size # same as height but used in different context
		self.height = imsize # image height and resolution (always a square)
		self.center = center # sets bulb position in x,y plane of the image
		self.counter = counter # index of generated images
		self.color_map = color_map
		self.colordict = {'fiery':[1/3,150,1,0,1/6,0],'blue':[1/6,0,0,20,1,0],'xmas':[-1/1.5,160,1,0,0.2,0],'70s':[.5,255/2,-1,255,-1,255],'gray':[1,0,1,0,1,0],'teal':[0,0,1,0,1,0],'poison':[1,0,0,30,0,200],'misc':[-1/1.5,150,1,0,0.5,70]}
		
	def paint(self):
		'''Generates the pal colormap values to be used in scipy.misc.toimage. Defaults are stored in self.colordict, and are called by their names in new instance'''
		if self.grad:
			m1, b1, m2, b2, m3, b3 = self.color_map
			triplet = [[0,0,0]]
			for i in range(1,255):
				triplet.append([m1*i+b1 , m2*i+b2 , m3*i+b3])
			return(triplet)
		else:
			try:
				self.cm = str(self.cm)
				assert self.cm in self.colordict
			except Exception:
				print('''Invalid colormap, available choices: \n \n {}'''.format(self.colordict))
			else:
				m1, b1, m2, b2, m3, b3 = self.colordict[self.cm]
				triplet = [[0,0,0]]
				for i in range(1,255):
					triplet.append([m1*i+b1 , m2*i+b2 , m3*i+b3])
				return(triplet)

	def get_plane_points(self):
		'''Makes a blank 2D canvas, parrallel to the screen, onto which will project the image of the mandelbulb, 
		like flashing light onto polaroid film.'''
		x_min, x_max = self.get_boundaries() # get x and y axis limits. Use zoom and span parameters to zoom in or out
		y_min, y_max = self.get_boundaries()
		a , b , c = self.obpos # position of observer, xyz coordinates as abc
		x = np.linspace(x_min, x_max, self.width) # fill axes with set resolution
		y = np.linspace(y_min, y_max, self.height) # fill axes with set resolution
		x, y = np.meshgrid(x, y) # Create 2D meshrid 'canvas'
		x, y = x.ravel(), y.ravel() # Flatten the arrays (quickly) so easier to parse
		# The below if statements check dot product of observer position and canvas/plane normal direction. 
		# Requires dot product is zero for screen to face canvas
		if np.abs(c) > 1e-4: 
			z = -(a*x + b*y)/c
			plane_points = np.vstack((x, y, z)).T
		elif np.abs(a) > 1e-4:
			z = -(c*x + b*y)/a
			plane_points = np.vstack((z, y, x)).T
		elif np.abs(b) > 1e-4:
			z = -(a*x + c*y)/b
			plane_points = np.vstack((x, z, y)).T       
		return(plane_points) # returns N cartesian points in a (Nx3) matrix with x,y,z coords as columns,
		# where number rows is self.width*self.height, so total number of points in meshgrid/on canvas

	def get_boundaries(self):
		'''Determine axis bounds given the center position of the bulb, and magnification.'''
		axmin = self.center[0] - self.span[0]/2.**self.zoom 
		axmax = self.center[1] + self.span[1]/2.**self.zoom
		return(axmin , axmax) 

	def get_directions(self, plane_points):
		'''Gets vector directions from observer postion to every point in the generated plane.'''
		v = np.array(plane_points - self.obpos) # gets vectors
		v = v/np.linalg.norm(v, axis=1)[:, np.newaxis] # normalize vectors
		return(v) # returns an array of unit vectors pointing to the discrete points on the canvas

	@jit
	def DistanceEstimator(self,plane_points):
		'''This does the actual Mandelbulb math to determine if points in the generated plane are part of the 3D set. This is main workhorse'''
		m = plane_points.shape[0] # this shape[0] is the number of points in the plane, corresponding the the number of rows
		# where again each row is a set of x,y,z coordinates
		x, y, z = np.zeros(m), np.zeros(m), np.zeros(m)
		x0, y0, z0 = plane_points[:, 0], plane_points[:, 1], plane_points[:, 2] # strip x , y , z colums from planepoints
		dr = np.ones(m)
		theta = np.zeros(m)
		phi = np.zeros(m)
		rn = np.zeros(m)
		for _ in range(self.itr): # test recursive function exceeds radius over 'itr' iterations
			r = np.sqrt(x*x + y*y + z*z) # this is part of change to spherical coords
			logic = (r < self.bail) 
			# this sets the radius threshold, cannot exceed radius of bail. If r[i] exceeds bail, logic[i] = False
			# otherwise logic[i] = True, and we keep iterating over that element of r until it is false
			# Logic is an array. Each array like dr uses [logic] to check if it should update a value it has stored,
			# for example if dr_old = [1,2,1,2], logic=[T,F,T,F] then dr_old[logic] = 3 gives
			# dr_old = [3,2,3,2]
			# Thus this function checks all points in the plane simultaneously!
			# With this cool framework in mind:
			theta[logic] = np.arctan2(np.sqrt(x[logic]*x[logic] + y[logic]*y[logic]), z[logic]) # these are change coords to spherical
			phi[logic] = np.arctan2(y[logic], x[logic]) # these are change coords to spherical

			dr[logic] = np.power(r[logic], self.deg - 1) * self.deg * dr[logic] + 1.0 
			# Below is the recursive Mandelbulb formula by Daniel White and Paul Nylander
			# https://en.wikipedia.org/wiki/Mandelbulb#frb-inline
			rn[logic] = r[logic] ** self.deg 
			theta[logic] = theta[logic] * self.deg
			phi[logic] = phi[logic] * self.deg
			x[logic] = rn[logic] * np.sin(theta[logic]) * np.cos(phi[logic]) + x0[logic]
			y[logic] = rn[logic] * np.sin(theta[logic]) * np.sin(phi[logic]) + y0[logic]
			z[logic] = rn[logic] * np.cos(theta[logic]) + z0[logic]
		return(0.5 * np.log(r) * r / dr)

	def trace(self,directions):
		total_distance = np.zeros(directions.shape[0]) # new array with same size as number of points
		keep_iterations = np.ones_like(total_distance)
		steps = np.zeros_like(total_distance)
		for _ in range(self.maxs):
			positions = self.obpos[np.newaxis, :] + total_distance[:, np.newaxis] * directions
			distance = self.DistanceEstimator(positions)
			keep_iterations[distance < self.mind] = 0
			total_distance += distance * keep_iterations
			steps += keep_iterations
		return 1 - (steps/self.maxs)**self.power

	def bulb_image(self):
		'''Returns an array with the color values for the pixels in a 2D image grid'''
		plane_points = self.get_plane_points() # get plane points
		directions = self.get_directions(plane_points) # get directions to plane points from origin
		image = self.trace(directions)
		image = image.reshape(self.width, self.height)
		print(image)
		arraymax = np.amax(image)
		#rescale colorvalues so picture is brighter. Array maximum * 1//arraymax is 1 so it will be white
		image = (1//arraymax)*image
		print(image)
		scipy.misc.toimage(image, pal = self.paint() ).save(os.getcwd() + '/frames/frame{}.png'.format(self.counter)) # save in the frames folder
		#note, used os to get current working directory for wherever script is used

if __name__=='__main__':
	bulb = Bulb( cm = '70s',imsize = 20)
	bulb.bulb_image()



