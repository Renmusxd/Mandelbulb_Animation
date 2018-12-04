import os
from bulb import Bulb
from tqdm import tqdm
import numpy as np


class Cinematic(object):
	'''Handles the making of movies from generated bulb frames.'''
	def __init__(self,fps = 20, movie_length = 2, deg_lims = [2,8], obpos = np.array([0 , 0 , 3.]), res = 500 ,movie_name = 'Mandlemoves' , offset = 0):
		self.fps = fps # change framerate
		self.off = offset # give frame naming index an offset so don't rewrite good frames
		self.res = res # movie resolution
		self.movin = movie_name # saved filename
		self.obpos = obpos # observer position
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
		os.system('cp -R -n frames/ Frames_Cache') # save frames to cache. Saves only files, and only if files do not exist
		os.system('rm -R frames') # cleanup frames folder
		os.system('mkdir frames') # cleanup frames folder
		savemsg = ' :: {}.mp4 saved in {} :: '.format(self.movin , cwd)
		return(savemsg)

	def gen_frames(self):
		'''Generates frames for a movie using the Bulb class object.'''
		fmax = self.fps*self.mov_len # get number of frames for a movie of length in seconds
		degrees = np.linspace(self.deg_star, self.deg_end, fmax) # apply number of frames
		# make a new  set of frames and dont overwrite frames you already have
		for i in tqdm(range(degrees.size), desc = ' :: Generating Frames :: '):
			bulb = Bulb(observer_position = self.obpos, degree = degrees[i], imsize = self.res, counter = i + self.off) 
			bulb.bulb_image()
		return(fmax,self.fps) #return the max frame index and framerate for the movie

if __name__=='__main__':
	movie = Cinematic(fps = 2.5, res = 1000)
	movie.stitch()
