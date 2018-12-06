import os
from bulb import Bulb
from tqdm import tqdm
import numpy as np

class Cinematic(object):
	'''Handles the making of movies from generated bulb frames.'''
	def __init__(self,fps = 20, movie_length = 2, deg_lims = [2,8], obpos = np.array([0 , 0 , 3.]), res = 500 ,movie_name = 'Mandelmoves' , offset = 0 , views = False, elipse = False):
		self.fps = fps # change framerate
		self.off = offset # give frame naming index an offset so don't rewrite good frames
		self.res = res # movie resolution
		self.views = views # Trace camera path along geodesic if true, else just go from obpos
		self.movin = movie_name # saved filename
		self.obpos = obpos # observer position
		self.elip = elipse # Trace camera path along elipse between poles if true, else just go from obpos
		self.mov_len = movie_length # movie length in seconds
		self.deg_star, self.deg_end = deg_lims # limits on power of recursive formula

	def stitch(self):
		'''Uses the ffmpeg terminal command to stitch together the png frames into a .mp4 movie file with given fps. Offset counter to adjust for cache'''
		# directs to frames to be iterated over. %d is interpreted by ffmpeg along with -start_number
		# this %d allows ffmpeg to iterated over sequential files in the /frames folder, and make a movie
		self.gen_frames() # make frames at given fps
		input(' :: Check /frames to see generated frames :: \n :: Press <Enter> to Continue :: ')
		cwd = os.getcwd()
		location = cwd + '/frames/frame%d.png' 
		# command output will be mp4 file at given fps. Suppress command line output (verbose command)
		ffmpeg_cmd = "ffmpeg -r {} -start_number {} -i {} -vcodec mpeg4 {}.mp4".format(self.fps , self.off , location , self.movin)
		os.system(ffmpeg_cmd) # make the movie
		os.system('rm -R frames') # cleanup frames folder
		os.system('mkdir frames') # cleanup frames folder
		savemsg = ' :: {}.mp4 saved in {} :: '.format(self.movin , cwd)
		return(savemsg)

	def gen_frames(self):
		'''Generates frames for a movie using the Bulb class object.'''
		fmax = self.fps*self.mov_len # get number of frames for a movie of length in seconds
		if self.elip: # if want to rotate bulb on a path
			self.path = self.elipse(pts = fmax) # apply number of frames to camera path
		elif self.views:
			self.path = self.viewer(pts = fmax) # apply number of frames to camera path
		else:
			# if you dont want a path, just use the observer position in each iteration
			x,y,z = self.obpos[0] * np.ones(fmax),self.obpos[1] * np.ones(fmax), self.obpos[2] * np.ones(fmax)
			self.path = np.vstack((x,y,z)).T
		degrees = np.linspace(self.deg_star, self.deg_end, fmax) # apply number of frames to degrees
		# make a new set of frames and dont overwrite frames you already have using offset
		for i in tqdm(range(degrees.size), desc = ' :: Generating Frames :: '):
			bulb = Bulb(observer_position = np.array(self.path[i]), degree = degrees[i], imsize = self.res, counter = i + self.off) 
			bulb.bulb_image()
		return(fmax,self.fps) #return the max frame index and framerate for the movie (can be useful)

	def elipse(self, pts = 360):
		'''Makes eliptical path between poles.'''
		print(' :: Setting Up Eliptical Path :: ')
		theta = np.linspace(0, 2 * np.pi, pts)
		# using equation for elipse in polar
		a = 2.0 # major axis
		b = 2.0 # minor axis
		radius = (a * b)/np.sqrt(b**2 * np.cos(theta)**2 + a**2 * np.sin(theta)**2)
		x = np.zeros_like(theta) # do this in polar, fix elipse to y,z plane
		y = radius * np.sin(theta)
		z = radius * np.cos(theta)
		path = np.vstack((x,y,z)).T # return point coordinates as rows
		return(path)

	def viewer(self, pts = 1000 , loc = 9):
		'''Sit at some views along a great circle while iterating.'''
		print(' :: Setting Up View Points :: ')
		radius = 3.0
		theta = np.linspace(0, 2 * np.pi, loc) # increment angle along path locations
		x = np.zeros(pts) # to do this in polar, fix circle to y,z plane
		y = np.zeros_like(x)
		z = np.zeros_like(y)
		# wait at location for pts/loc frames
		for i in range(pts): 
			y[i] += radius * np.sin(theta[(loc*i)//pts])
			z[i] += radius * np.cos(theta[(loc*i)//pts])
		path = np.vstack((x,y,z)).T # return point coordinates as rows
		return(path)

if __name__=='__main__':
	movie = Cinematic(views = True,res = 100, movie_length = 10)
	movie.stitch()
	
