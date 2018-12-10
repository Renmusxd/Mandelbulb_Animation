import time
from film import Cinematic
import numpy as np
from bulb import Bulb

if __name__=='__main__':
	bulb = Bulb()
	bulb.colordict.keys()
	colors = bulb.colordict.keys()
	#colors=['fiery','blue','xmas','70s','teal','gray']
	inputstring = '\n\nPlease specify what color you would like to see on the object. \n\nYou can choose from:\nfiery (orange) \nblue \nxmas (red&green) \n70s \nteal \ngray \n\nEnter color here:'
	string = ''
	for i in colors:
		string += str(i) + '\n' 
	inputstring = '\n\nPlease specify what color you would like to see on the object. \n\nYou can choose from:\n{} \n\nEnter color here:'.format(string) 	
	while True:
		a = input(inputstring)
		try:
			a = str(a)
			assert a in colors
		except Exception:
			print('\n\n :: Invalid color. Please choose from the given list. :: ')
		else:
			t0 = time.perf_counter()
			movie = Cinematic(obpos = np.array([1,2,-3]) , fps=2, movie_length = 2, res=200, ccm = a, deg_lims=[7,9])
			movie.stitch()
			t = time.perf_counter() - t0
			print(' :: Time Elapsed During Operation {}s :: '.format(int(t)))
			break
	
