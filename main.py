import os
from bulb import Bulb
from tqdm import tqdm
import numpy as np
import time

def stitch(fmax,fps):
	'''Uses the ffmpeg terminal command to stitch together the png frames into a .gif movie file with 60 fps'''
	# directs to frames to be iterated over. %d is interpreted by ffmpeg along with -start_number
	# this %d allows ffmpeg to iterated over sequential files in the /frames folder, and make a movie
	cwd = os.getcwd() + '/frames/frame%d.png' 
	# command output will be mp4 file at given fps. Suppress command line output (verbose command)
	ffmpeg_cmd = "ffmpeg -r {} -start_number 0 -i {} -vcodec mpeg4 Mandelmoves.mp4 > /dev/null".format(fps , cwd)
	os.system(ffmpeg_cmd)
	print(' :: Mandelmoves.mp4 saved in {} :: '.format(os.getcwd()))

def gen_frames(start_deg = 2, end_deg = 8, obpos = np.array([0 , 0 , 3.]), movie_length = 2 , fps = 20):
	'''Generates frames for a movie using the Bulb class object.'''
	fmax=fps*movie_length # get number of frames for a movies of length in seconds
	degrees=np.linspace(start_deg, end_deg, fmax) # get 60 fps
	for i in tqdm(range(degrees.size), desc = ' :: Generating Frames :: '): 
		bulb=Bulb(observer_position = obpos, degree = degrees[i], counter = i)
		bulb.bulb_image()
	return(fmax,fps) #return the max frame index and framerate for the movie

if __name__=='__main__':
	t0=time.perf_counter()
	fmax,fps = gen_frames(start_deg = 1 , end_deg = 10 , obpos = np.array([1,2,3]) , movie_length = 10)
	input(' :: Press <Enter> to continue :: ')
	stitch(fmax,fps)
	t=time.perf_counter()-t0
	print(' :: Time Elapsed During Operation {}s :: '.format(t))
