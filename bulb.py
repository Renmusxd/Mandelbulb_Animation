import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numba import jit
from copy import copy
import scipy.misc
from tqdm import tqdm
import os

class Bulb(object):
    '''Generate 2D array with colormap values for making png images of the 3D Mandelbulb. Save'''
    def __init__(self,degree=8, observer_position=np.array([0., 0., 3.]), max_steps=32, iterations=32, bailout=2**20, min_distance=5e-4, zoom=0, power=0.2, width=500, height=500, x_size=500, y_size=500, span=[1.2, 1.2], center=[0, 0],counter=0):
        '''Init config variables for bulb object'''
        self.itr = iterations # Constraint: number iterations before we decide a point under recursion formula is bounded or not by bail, i.e in set.
        self.deg = degree  # the power n used in the recursive formula V --> V^n + C
        self.span = span # span of data points on the axes
        self.maxs = max_steps
        self.mind = min_distance
        self.bail = bailout # Constraint: points within the bulb set need to stay within bailout, a radius, over 32 iterations.
        self.zoom = zoom # literally used to magnify image regions if desired.
        self.obpos = observer_position # literally the position in space the observer would be in resultant png. Used for ray tracing source position.
        self.power = power 
        self.width = width # image width
        self.xsize = x_size # same as width but used in different contexts
        self.ysize = y_size # same as height but used in different context
        self.height = height # image height
        self.center = center # where the bulb is centered     
        self.counter = counter # number of generated images

    def get_plane_points(self):
        '''I think this is where members of the set are calculated.'''
        x_min, x_max = self.get_boundaries() 
        y_min, y_max = self.get_boundaries()
        a , b , c = self.obpos # position of observer, xyz coordinates as abc
        x = np.linspace(x_min, x_max, self.width)
        y = np.linspace(y_min, y_max, self.height)
        x, y = np.meshgrid(x, y)
        x, y = x.ravel(), y.ravel() # flatten the arrays quickly so easier to parse
        if np.abs(c) > 1e-4: # if observer position greater than some number, set the farthest point on the bulb?
            z = -(a*x + b*y)/c
            plane_points = np.vstack((x, y, z)).T
        elif np.abs(a) > 1e-4:
            z = -(c*x + b*y)/a
            plane_points = np.vstack((z, y, x)).T
        elif np.abs(b) > 1e-4:
            z = -(a*x + c*y)/b
            plane_points = np.vstack((x, z, y)).T       
        return(plane_points)

    def get_boundaries(self):
        '''determine axis bounds the expected span, center position of bulb, and magnification.'''
        axmin = self.center[0] - self.span[0]/2.**self.zoom 
        axmax = self.center[1] + self.span[1]/2.**self.zoom
        return(axmin , axmax)

    def get_directions(self, plane_points):
        '''gets vector directions from observer postion to every point in the generated plane'''
        v = np.array(plane_points - self.obpos)
        v = v/np.linalg.norm(v, axis=1)[:, np.newaxis]
        return(v)

    @jit
    def DistanceEstimator(self,plane_points):
        '''I think theis also does mandelbulb set calculations?'''
        m = plane_points.shape[0]
        x, y, z = np.zeros(m), np.zeros(m), np.zeros(m)
        x0, y0, z0 = plane_points[:, 0], plane_points[:, 1], plane_points[:, 2]
        dr = np.zeros(m) + 1
        r = np.zeros(m)
        theta = np.zeros(m)
        phi = np.zeros(m)
        zr = np.zeros(m)
        for _ in range(self.itr):
            r = np.sqrt(x*x + y*y + z*z)
            idx1 = r < self.bail # this sets the radius threshold, cannot exceed radius 1000 (default)
            dr[idx1] = np.power(r[idx1], self.deg - 1) * self.deg * dr[idx1] + 1.0
            theta[idx1] = np.arctan2(np.sqrt(x[idx1]*x[idx1] + y[idx1]*y[idx1]), z[idx1])
            phi[idx1] = np.arctan2(y[idx1], x[idx1])
            zr[idx1] = r[idx1] ** self.deg
            theta[idx1] = theta[idx1] * self.deg
            phi[idx1] = phi[idx1] * self.deg
            x[idx1] = zr[idx1] * np.sin(theta[idx1]) * np.cos(phi[idx1]) + x0[idx1]
            y[idx1] = zr[idx1] * np.sin(theta[idx1]) * np.sin(phi[idx1]) + y0[idx1]
            z[idx1] = zr[idx1] * np.cos(theta[idx1]) + z0[idx1]
        return(0.5 * np.log(r) * r / dr)

    def trace(self,directions):
        total_distance = np.zeros(directions.shape[0])
        keep_iterations = np.ones_like(total_distance)
        steps = np.zeros_like(total_distance)
        for _ in range(self.maxs):
            positions = self.obpos[np.newaxis, :] + total_distance[:, np.newaxis] * directions
            distance = self.DistanceEstimator(positions)
            keep_iterations[distance < self.mind] = 0
            total_distance += distance * keep_iterations
            steps += keep_iterations
        return 1 - (steps/self.maxs)**self.power

    def bulb_image(self):
        '''Returns an array with the color values for the pixels in a 2D image grid'''
        plane_points = self.get_plane_points() # get plane points
        directions = self.get_directions(plane_points) # get directions to plane points from origin
        image = self.trace(directions)
        image = image.reshape(self.width, self.height)
        arraymax = np.amax(image)
        #rescale colorvalues so picture is brighter. Array maximum * 1//arraymax is 1 so it will be white
        image = (1/arraymax)*image 
        scipy.misc.toimage(image, cmin=0.0, cmax=1,mode='L').save(os.getcwd()+'/frames/frame{}.png'.format(self.counter)) # save in the frames folder
        #note, used os to get current working directory for wherever script is used

if __name__=='__main__':
    bulb = Bulb()
    bulb.bulb_image()



