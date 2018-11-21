import subprocess as subp
from bulb import Bulb
from tqdm import tqdm
import numpy as np

def gif(fmax):
	'''Uses the gif terminal command to stitch together the png frames into a .gif movie file with 60 fps'''
	pass

def gen_frames(start_deg = 2, end_deg = 8, obpos = np.array([0 , 0 , 3.]), movie_length = 2):
	'''Generates frames for a movie using the Bulb class object.'''
	fmax=60*movie_length # get number of frames for a movies of length in seconds
	degrees=np.linspace(start_deg, end_deg, fmax) # get 60 fps
	for i in tqdm(range(degrees.size), desc = ' :: Generating Frames :: '): 
		bulb=Bulb(observer_position = obpos, degree = degrees[i], counter = i)
		bulb.bulb_image()
	return(fmax) #return the max frame index

if __name__=='__main__':
    fmax = gen_frames()
    # gif(fmax)
