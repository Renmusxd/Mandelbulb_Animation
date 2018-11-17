import mandel as man
import time 

if __name__=='__main__':
	while True:
		try:
			ans = input('Recalc or use saved? (r/s) : ')
			ans = str(ans)
			ans = ans.lower()

		except Exception:
			print('Try again')

		else:
			if ans == 'r':
				config=input('List config options, comma separated (Vmax, n, itr): ')
				Vmax,n,itr=config.strip('()').split(',')
				Vmax = int(Vmax)
				n = int(n)
				itr = int(itr)
				estimate=(2**3)*(Vmax**3)/(1000000*60)
				print('Time estimate: {} minutes'.format(estimate))
				t0 = time.perf_counter()
				x,y,z = man.space(Vmax,n,itr)
				t = man.display(x,y,z)-t0
				print('Time elapsed during display operation:', t ,'sec')
				man.save([x,y,z])
				break

			elif ans == 's':
				t0 = time.perf_counter()
				x = man.get_array('Data/1_VNI.txt')
				y = man.get_array('Data/2_VNI.txt')
				z = man.get_array('Data/3_VNI.txt')
				t = man.display(x,y,z) - t0
				print('Time elapsed during display operation:', t ,'sec')
				break

			else:
				print('Try again')
else:
	print('main.py unused')