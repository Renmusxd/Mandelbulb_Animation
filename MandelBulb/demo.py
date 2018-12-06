import time
from film import Cinematic
from bulb import Bulb
import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg 
import numpy as np

if __name__=='__main__':

	# Make single high res picture of Mandelbulb, with a given colormap, and with a specific degree from the mandelbulb set.
	# takes ~ 50 seconds
	frame_index = 10
	Mandelbulb = Bulb(cm = 'blue', imsize = 1000, observer_position = np.array([1,2,3]) , degree = 6 ,counter = frame_index) # init
	Mandelbulb.bulb_image() # make the frame
	os.system('open /frames/frame{}'.format(frame_index))
	input(' :: Press <Enter> to Continue :: ')

	# Make a low res movie of some degrees from a specific viewpoint, with given resolution and movie length
	movie = Cinematic(res = 100, obpos = np.array([1,2,-3]) , movie_length = 20 ,deg_lims=[2,20])
	movie.stitch()
	os.system('open Mandelmoves.mp4')
	input(' :: Press <Enter> to Continue :: ')
	
	
	# Make a low res movie of some degrees showing several viewpoints, save under different movie name
	movie_name = 'Different'
	movie = Cinematic(res = 100 , movie_length = 20 ,deg_lims=[2,20], views = True, movie_name = movie_name)
	movie.stitch()
	os.system('open {}.mp4'.format(movie_name))
	input(' :: Press <Enter> to Continue :: ')