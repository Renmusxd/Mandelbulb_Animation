import numpy as np
from numba import jit
import time

@jit 
def member(Cx, Cy, Cz,n = 8,itr = 32):
    '''Determine if a point is in the mandelbulb set.'''
    # start 'orbit' from <0,0,0>
    x, y, z = 0.0, 0.0, 0.0
    
    for i in range(itr): #iteration threshold
        # White and Nylander's formula for the nth power (wikipedia)
        r = np.sqrt(x*x + y*y + z*z)
        theta = np.arctan2(np.sqrt(x*x + y*y), z)
        phi = np.arctan2(y, x)
        
        x = r**n * np.sin(theta*n) * np.cos(phi*n) + Cx
        y = r**n * np.sin(theta*n) * np.sin(phi*n) + Cy
        z = r**n * np.cos(theta*n) + Cz
        
        if (x**2 + y**2 + z**2 > 2).any(): # vector length threshold
            return False
    else:
        return True

@jit
def space(Vmax=10):
    '''Generates a set of points in 3D space that are members of the mandelbulb set.'''
    x,y,z=np.mgrid[-Vmax:Vmax,-Vmax:Vmax,-Vmax:Vmax]
    x=x.reshape(1,x.size)[0] #flatten out values so as easier to parse, and get rid of nested arrays
    y=y.reshape(1,y.size)[0]
    z=z.reshape(1,z.size)[0]
    spacex=np.empty((1,x.size))
    spacey=np.empty((1,y.size))
    spacez=np.empty((1,z.size))
    for i in range(x.size):
        if member(x[i],y[i],z[i]):
           spacex=x[i]
           spacey=y[i]
           spacez=z[i]       
    return(spacex,spacey,spacez)


