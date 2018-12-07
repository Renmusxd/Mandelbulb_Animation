import time
from film import Cinematic
from bulb import Bulb
import os
import numpy as np

if __name__=='__main__':
	#Choose a color scheme from bulb
	bulbo = Bulb()
	bulbo.colordict.keys()
	colors = bulbo.colordict.keys()
	string = ''
	for i in colors:
		string += str(i) + '\n' 
	inputstring = '\n\nPlease specify what color scheme you would like to see on the object. \n\nYou can choose from:\n{} \n\nEnter color here: '.format(string) 	
	while True:
		a = input(inputstring)
		try:
			a = str(a)
			assert a in colors
			break
		except Exception:
			print('\n\n :: Invalid color. Please choose from the given list. :: ')

	# Make single high res picture of Mandelbulb, with a given colormap, and with a specific degree from the mandelbulb set.
	# takes ~ 50 seconds
	print(' :: Demo Starting ::')
	frame_index = 10
	Mandelbulb = Bulb(cm = a, imsize = 1000, observer_position = np.array([1,2,3]) , degree = 6 ,counter = frame_index) # init
	Mandelbulb.bulb_image() # make the frame
	time.sleep(5)
	os.system('open frames/frame{}.png'.format(frame_index))
	input(' :: Press <Enter> to Continue :: ')

	# Make a low res movie of some degrees from a specific viewpoint, with given resolution and movie length
	movie = Cinematic(res = 100, obpos = np.array([1,2,-3]) , movie_length = 20 ,deg_lims=[2,20] , cm ='70s')
	movie.stitch()
	os.system('open Mandelmoves.mp4')
	input(' :: Press <Enter> to Continue :: ')
	
	
	# Make a low res movie of some degrees showing several viewpoints, save under different movie name
	movie_name = 'Different'
	movie = Cinematic(res = 100 , movie_length = 20 ,deg_lims=[2,20], views = True, movie_name = movie_name, grad = True)
	movie.stitch()
	os.system('open {}.mp4'.format(movie_name))
	input(' :: Press <Enter> to Continue :: ')


