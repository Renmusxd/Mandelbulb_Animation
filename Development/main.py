from mandel import Mandel as man
import time 
import matplotlib.pyplot as plt 
from mpl_toolkits.mplot3d import Axes3D

def save(listarrays):
    '''For large arrays, save to .txt so dont need to recalc. Takes in list of arrays'''
    while True:
        try:
            ans = input("Want to save values? (y/n) : ")
            ans = str(ans)
            ans = ans.lower()
        except Exception:
            print('Try again')
        else:
            if ans == 'y':
                counter=1
                for i in listarrays:
                    record(i,title='{}_VNI'.format(counter))
                    counter+=1
                print('Saved {} files'.format(counter))
                break
            elif ans == 'n':
                break
            else:
                print('Try again')

def record(array,title='Array'):
    '''Saves array values into .txt with newline separation.'''
    filestr = ''''''
    datafile=open('Data/{}.txt'.format(title),'a')
    for i in range(array.size):
        filestr+='{} \n'.format(array[i])
    datafile.write(filestr)
    datafile.close()

def display(x,y,z,cm):
    """Display 3D set of coordinates"""
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x,y,z, c=cm, marker='o')
    ax.grid(False)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
    plt.axis('off')

    fig.show()
    t=time.perf_counter()
    input('Press <Enter> to exit')
    return(t)

def get_array(filename):
    '''Remake numpy array from .txt file with saved values'''
    datafile = open('{}'.format(filename),'r')
    lines = datafile.readlines() # list of the lines
    array = np.empty(len(lines)) #initialize array of correct size
    for i in range(len(lines)):
        array[i]=lines[i] # make array of lines
        datafile.close()
    return(array)

if __name__=='__main__':
	while True:
		try:
			ans = input('Recalculate or use saved data? (r/s) : ')
			ans = str(ans)
			ans = ans.lower()

		except Exception:
			print('Try again')

		else:
			if ans == 'r':
				pts=int(input('# pts per axis to be diplayed: '))
				# Also perf counter
				t0 = time.perf_counter()
				# get space and color map index using mandelbulb object
				bulb = man(pts = pts)
				x,y,z,cm = bulb.space()
				# display space
				t = display(x,y,z,cm)-t0
				print('Time elapsed during display operation:', t ,'sec')
				#Save array if desired
				save([x,y,z,cm])
				break

			elif ans == 's':
				t0 = time.perf_counter()
				# get arrays
				x = get_array('Data/1_VNI.txt')
				y = get_array('Data/2_VNI.txt')
				z = get_array('Data/3_VNI.txt')
				cm = get_array('Data/4_VNI.txt')
				# debug execution, time estimation
				t = display(x,y,z,cm) - t0
				print('Time elapsed during display operation:', t ,'sec')
				break

			else:
				print('Try again')