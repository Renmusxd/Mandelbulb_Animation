import numpy as np
from numba import jit
from tqdm import tqdm
import matplotlib.pyplot as plt 
from mpl_toolkits.mplot3d import Axes3D
import time

@jit
def member(Cx, Cy, Cz, n, itr):
    '''Determines if a point with 3 coordinates is in the mandelbulb set.'''
    # start 'orbit' from <0,0,0>
    x, y, z = 0.0, 0.0, 0.0
    
    for i in range(itr): #iteration threshold
        # White and Nylander's formula for the nth power (wikipedia)

        # first move to spherical coordinates to apply recursion formula
        r = np.sqrt(x*x + y*y + z*z) 
        theta = np.arctan2(np.sqrt(x*x + y*y), z)
        phi = np.arctan2(y, x)
        
        # apply recursion formula
        x = r**n * np.sin(theta*n) * np.cos(phi*n) + Cx
        y = r**n * np.sin(theta*n) * np.sin(phi*n) + Cy
        z = r**n * np.cos(theta*n) + Cz
        
        if x**2 + y**2 + z**2 > 2: # vector length threshold
            return(False) # Return boolean logic. If surpass bound after itr, do not set number
        else:
            return(True) # If remains bounded through number itr, then set member.

@jit
def sphere(Cx,Cy,Cz,Vmax):
    if (Cx**2 + Cy**2 + Cz**2 >= Vmax/2):
        return(False)
    else:
        return(True)

@jit
def space(Vmax = 10, n = 8, itr = 32):
    '''Generates a set of points in 3D space that are members of the mandelbulb set.'''
    print(' :: Generating Meshgrid :: ')
    x,y,z = np.mgrid[-Vmax:Vmax,-Vmax:Vmax,-Vmax:Vmax]
    print(' :: Generating Axes :: ')
    x = x.reshape(1,x.size)[0] #flatten out values so as easier to parse, and get rid of nested arrays
    y = y.reshape(1,y.size)[0]
    z = z.reshape(1,z.size)[0]
    spacex = np.array([])
    spacey = np.array([])
    spacez = np.array([])
    print(' :: Shaping Space :: ')
    for i in tqdm(range(x.size), desc ='Finding Mandelbulb Set Members'):
        if member(x[i],y[i],z[i],n,itr):
            # if not sphere(x[i],y[i],z[i],Vmax):
            spacex = np.append(spacex,x[i])
            spacey = np.append(spacey,y[i])
            spacez = np.append(spacez,z[i])
    return(spacex,spacey,spacez)

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

def display(x,y,z):
    """Display 3D set of coordinates"""
    fig = plt.figure()
    # xmax = np.amax(x)
    # ymax = np.amax(y)
    # zmax = np.amax(z)
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x,y,z, c='r', marker='o')
    # ax.set_xlabel('X')
    # ax.set_ylabel('Y')
    # ax.set_zlabel('Z')
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


