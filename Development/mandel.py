import numpy as np
from numba import jit
from tqdm import tqdm

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
            return False # Return boolean logic. If surpass bound after itr, not set number
    else:
        return True # If remains bounded through number itr, then set member.

@jit
def space(Vmax = 10, n=8, itr=32):
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
        if member(x[i],y[i],z[i], n=n, itr=itr):
           spacex = np.append(spacex,x[i])
           spacey = np.append(spacey,y[i])
           spacez = np.append(spacez,z[i]) 
    return(spacex,spacey,spacez)
