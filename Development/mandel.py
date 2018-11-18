import numpy as np
from numba import jit
from tqdm import tqdm
import time

class Mandel(object):

    def __init__(self,vmax = 2, pts = 1000, n = 8, itr = 32):
        self.vmax=vmax
        self.pts=pts
        self.itr=itr
        self.n=n

    @jit
    def member(self, Cx, Cy, Cz):
        '''Determines if a point with 3 coordinates is in the mandelbulb set.'''
        # start 'orbit' from <0,0,0>
        x, y, z = 0.0, 0.0, 0.0
        counter=0 # count iterations
        for i in range(self.itr): #iteration threshold
            # White and Nylander's formula for the nth power (wikipedia)
            # first move to spherical coordinates to apply recursion formula
            r = np.sqrt(x*x + y*y + z*z) 
            theta = np.arctan2(np.sqrt(x*x + y*y), z)
            phi = np.arctan2(y, x)
            # apply recursion formula
            x = r**self.n * np.sin(theta*self.n) * np.cos(phi*self.n) + Cx
            y = r**self.n * np.sin(theta*self.n) * np.sin(phi*self.n) + Cy
            z = r**self.n * np.cos(theta*self.n) + Cz
            if x**2 + y**2 + z**2 > self.vmax: # vector length threshold
                return(counter)
            else:
                counter = counter + 1
        return(0)

    @jit
    def sphere(self,Cx,Cy,Cz):
        if (Cx**2 + Cy**2 + Cz**2 >= self.vmax):
            return(False)
        else:
            return(True)

    @jit
    def space(self):
        '''Generates a set of points in 3D space that are members of the mandelbulb set.'''
        print(' :: Generating Axes :: ')
        x0 = np.linspace(-self.vmax,self.vmax,self.pts)
        y0 = np.linspace(-self.vmax,self.vmax,self.pts)
        z0 = np.linspace(-self.vmax,self.vmax,self.pts)

        print(' :: Generating Meshgrid :: ')
        x,y,z = np.meshgrid(x0,y0,z0)

        print(' :: Shaping Space :: ')
        x = x.flatten() #flatten out array to 1D so as easier to parse
        y = y.flatten()
        z = z.flatten()
        
        spacex = np.array([])
        spacey = np.array([])
        spacez = np.array([]) 
        cm = np.array([]) # initialize the colormap index

        for i in tqdm(range(x.size), desc ='Finding Mandelbulb Set Members'):
            cm_idx = self.member(x[i],y[i],z[i]) #colormap index
            if cm_idx > 0:
                spacex = np.append(spacex,x[i])
                spacey = np.append(spacey,y[i])
                spacez = np.append(spacez,z[i])
                cm = np.append(cm,cm_idx)
        return(spacex,spacey,spacez,cm)





