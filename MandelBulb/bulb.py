import numpy as np
from PIL import Image
from matplotlib import cm
import os


class Bulb(object):
	"""Generate individual images of the Mandelbulb set with ray tracing."""

	def __init__(self, max_steps=32, iterations=32, bailout=2 ** 20, min_distance=5e-4, zoom=0, power=0.2, imsize=500,
				 x_size=500, y_size=500, span=None, center=None):
		"""Initializes config variables for bulb object"""
		# Choose the colormap for the resultant bulb from in colordict presets
		if center is None:
			center = [0, 0]
		if span is None:
			span = [1.2, 1.2]
		self.itr = iterations  # Constraint: number iterations before we decide a point under recursion formula is bounded or not by bail, i.e in set.
		self.span = span  # another control of zoom of picture, numerator term
		self.maxs = max_steps
		self.mind = min_distance  # minimum distance from observer position that is considered a
		self.bail = bailout  # Constraint: points within the bulb set need to stay within bailout, a radius, over 32 iterations.
		self.zoom = zoom  # controls zoom, denominator term
		self.power = power
		self.width = imsize  # image width and resolution (always a square)
		self.xsize = x_size  # same as width but used in different context
		self.ysize = y_size  # same as height but used in different context
		self.height = imsize  # image height and resolution (always a square)
		self.center = center  # sets bulb position in x,y plane of the image

	def get_plane_points(self):
		"""
		Makes a blank 2D canvas, parrallel to the screen, onto which will project the image of the mandelbulb,
		like flashing light onto polaroid film.
		"""
		# get x and y axis limits. Use zoom and span parameters to zoom in or out
		x_min, x_max = self.get_boundaries()
		y_min, y_max = self.get_boundaries()
		# position of observer, xyz coordinates as abc
		a, b, c = self.obpos
		x = np.linspace(x_min, x_max, self.width)  # fill axes with set resolution
		y = np.linspace(y_min, y_max, self.height)  # fill axes with set resolution
		x, y = np.meshgrid(x, y)  # Create 2D meshrid 'canvas'
		x, y = x.ravel(), y.ravel()  # Flatten the arrays (quickly) so easier to parse
		# The below if statements check dot product of observer position and canvas/plane normal direction.
		# Requires dot product is zero for screen to face canvas
		if np.abs(c) > 1e-4:
			z = -(a * x + b * y) / c
			plane_points = np.vstack((x, y, z)).T
		elif np.abs(a) > 1e-4:
			z = -(c * x + b * y) / a
			plane_points = np.vstack((z, y, x)).T
		elif np.abs(b) > 1e-4:
			z = -(a * x + c * y) / b
			plane_points = np.vstack((x, z, y)).T
		else:
			raise ValueError("a, b, or c should be above 1e-4")

		return plane_points  # returns N cartesian points in a (Nx3) matrix with x,y,z coords as columns,

	# where number rows is self.width*self.height, so total number of points in meshgrid/on canvas

	def get_boundaries(self):
		"""Determine axis bounds given the center position of the bulb, and magnification."""
		axmin = self.center[0] - self.span[0] / 2. ** self.zoom
		axmax = self.center[1] + self.span[1] / 2. ** self.zoom
		return axmin, axmax

	def get_directions(self, plane_points):
		"""Gets vector directions from observer postion to every point in the generated plane."""
		v = np.array(plane_points - self.obpos)  # gets vectors
		v = v / np.linalg.norm(v, axis=1)[:, np.newaxis]  # normalize vectors
		return v  # returns an array of unit vectors pointing to the discrete points on the canvas

	def distance_estimator(self, plane_points):
		"""
		This does the actual Mandelbulb math to determine if points in the generated plane are part of the 3D set.
		This is main workhorse
		"""

		# this shape[0] is the number of points in the plane, corresponding the the number of rows
		m = plane_points.shape[0]

		# where again each row is a set of x,y,z coordinates
		x, y, z = np.zeros(m), np.zeros(m), np.zeros(m)

		# strip x , y , z colums from planepoints
		x0, y0, z0 = plane_points[:, 0], plane_points[:, 1], plane_points[:, 2]

		dr = np.ones(m)
		theta = np.zeros(m)
		phi = np.zeros(m)
		rn = np.zeros(m)

		for _ in range(self.itr):
			# test recursive function exceeds radius over 'itr' iterations
			r = np.sqrt(x ** 2 + y ** 2 + z ** 2)
			logic = (r < self.bail)
			# this sets the radius threshold, cannot exceed radius of bail. If r[i] exceeds bail, logic[i] = False
			# otherwise logic[i] = True, and we keep iterating over that element of r until it is False
			xy = np.sqrt(x[logic] * x[logic] + y[logic] * y[logic])
			theta[logic] = np.arctan2(xy, z[logic])  # these are change coords to spherical
			phi[logic] = np.arctan2(y[logic], x[logic])  # these are change coords to spherical
			dr[logic] = np.power(r[logic], self.deg - 1) * self.deg * dr[logic] + 1.0
			rn[logic] = r[logic] ** self.deg
			theta[logic] = theta[logic] * self.deg
			phi[logic] = phi[logic] * self.deg
			x[logic] = rn[logic] * np.sin(theta[logic]) * np.cos(phi[logic]) + x0[logic]
			y[logic] = rn[logic] * np.sin(theta[logic]) * np.sin(phi[logic]) + y0[logic]
			z[logic] = rn[logic] * np.cos(theta[logic]) + z0[logic]

		return 0.5 * np.log(r) * r / dr

	def trace(self, directions):
		total_distance = np.zeros(directions.shape[0])  # new array with same size as number of points
		keep_iterations = np.ones_like(total_distance)
		steps = np.zeros_like(total_distance)
		for _ in range(self.maxs):
			positions = self.obpos[np.newaxis, :] + total_distance[:, np.newaxis] * directions
			distance = self.distance_estimator(positions)
			keep_iterations[distance < self.mind] = 0
			total_distance += distance * keep_iterations
			steps += keep_iterations
		return 1 - (steps / self.maxs) ** self.power

	def bulb_image(self, degree=8, observer_position=None, counter=0):
		"""Returns an array with the color values for the pixels in a 2D image grid"""

		if observer_position is None:
			observer_position = np.array([0., 0., 3.])

		# the power n used in the recursive formula V --> V^n + C any degree >= 0 works,
		# but smaller degree uses more iterations
		self.deg = degree
		# literally the position in space the observer would be in resultant png.
		# Used for ray tracing source position.
		self.obpos = observer_position

		plane_points = self.get_plane_points()  # get plane points
		directions = self.get_directions(plane_points)  # get directions to plane points from origin
		image = self.trace(directions)
		image = image.reshape(self.width, self.height)
		arraymax = np.amax(image)

		# rescale colorvalues so picture is brighter. Array maximum * 1//arraymax is 1 so it will be white
		image = (1 // arraymax) * image
		img = Image.fromarray(np.uint8(cm.gist_earth(image) * 255))

		if not os.path.exists("frames"):
			os.makedirs("frames")
		im = img.save('frames/frame{}.png'.format(counter))  # index of generated images
# note, used os to get current working directory for wherever script is used


if __name__ == '__main__':
	# Example of medium size/res image generation (default viewpoint).
	bulb = Bulb(imsize=1000)
	bulb.bulb_image()
