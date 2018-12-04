import time
from film import Cinematic




if __name__=='__main__':
	t0 = time.perf_counter()
	movie = Cinematic(obpos = np.array([1,2,3]) , movie_length = 20 deg_lims=[2,20])
	movie.stitch()
	t = time.perf_counter() - t0
	print(' :: Time Elapsed During Operation {}s :: '.format(int(t)))