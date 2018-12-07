import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numba import jit
from copy import copy
from scipy import ndimage
from tqdm import tqdm
import scipy.misc

def get_plane_points(Q, center, span, zoom, width, height):
    print('Get plane_points')
    x_min, x_max = get_boundaries(center[0], span[0], zoom) 
    y_min, y_max = get_boundaries(center[1], span[1], zoom)
    a, b , c = Q
    x = np.linspace(x_min, x_max, width)
    y = np.linspace(y_min, y_max, height)
    x, y = np.meshgrid(x, y)
    x, y = x.reshape(-1), y.reshape(-1)
    if np.abs(c) > 1e-4:
        z = -(a*x + b*y)/c
        P = np.vstack((x, y, z)).T
    elif np.abs(a) > 1e-4:
        z = -(c*x + b*y)/a
        P = np.vstack((z, y, x)).T
    elif np.abs(b) > 1e-4:
        z = -(a*x + c*y)/b
        P = np.vstack((x, z, y)).T
    print('Done')
    print(P)
    return P

def get_directions(P, Q):
    v = np.array(P - Q)
    v = v/np.linalg.norm(v, axis=1)[:, np.newaxis]
    print('Done')
    print(v)
    return v

@jit
def DistanceEstimator(positions, iterations, degree=8, bailout=1000):
    m = positions.shape[0]
    x, y, z = np.zeros(m), np.zeros(m), np.zeros(m)
    x0, y0, z0 = positions[:, 0], positions[:, 1], positions[:, 2]
    dr = np.zeros(m) + 1
    r = np.zeros(m)
    theta = np.zeros(m)
    phi = np.zeros(m)
    zr = np.zeros(m)
    for _ in range(iterations):
        r = np.sqrt(x*x + y*y + z*z)
        idx1 = r < bailout
        dr[idx1] = np.power(r[idx1], degree - 1) * degree * dr[idx1] + 1.0

        theta[idx1] = np.arctan2(np.sqrt(x[idx1]*x[idx1] + y[idx1]*y[idx1]), z[idx1])
        phi[idx1] = np.arctan2(y[idx1], x[idx1])

        zr[idx1] = r[idx1] ** degree
        theta[idx1] = theta[idx1] * degree
        phi[idx1] = phi[idx1] * degree

        x[idx1] = zr[idx1] * np.sin(theta[idx1]) * np.cos(phi[idx1]) + x0[idx1]
        y[idx1] = zr[idx1] * np.sin(theta[idx1]) * np.sin(phi[idx1]) + y0[idx1]
        z[idx1] = zr[idx1] * np.cos(theta[idx1]) + z0[idx1]

    return 0.5 * np.log(r) * r / dr

def trace(start, directions, max_steps, min_distance, iterations, degree, bailout, power):
    total_distance = np.zeros(directions.shape[0])
    keep_iterations = np.ones_like(total_distance)
    steps = np.zeros_like(total_distance)
    print('DistanceEstimator running')
    for _ in tqdm(range(max_steps)):
        positions = start[np.newaxis, :] + total_distance[:, np.newaxis] * directions
        distance = DistanceEstimator(positions, iterations, degree, bailout)
        keep_iterations[distance < min_distance] = 0
        total_distance += distance * keep_iterations
        steps += keep_iterations
    print('Done')
    print(1 - (steps/max_steps)**power)
    return 1 - (steps/max_steps)**power

def plot_mandelbulb(degree=8, observer_position=np.array([1, 1, 3.]), max_steps=32, iterations=32, bailout=2**20, min_distance=5e-3, zoom=0, power=0.2, width=500, height=500, x_size=500, y_size=500, span=[1.2, 1.2], center=[0, 0]):
    plane_points = get_plane_points(observer_position, center=center, span=span, zoom=zoom, width=width, height=height)
    directions = get_directions(plane_points, observer_position)
    image = trace(observer_position, directions, max_steps, min_distance, iterations, degree, bailout, power)
    image = image.reshape(width, height)
    return(image)
    # fig ,ax = plt.subplots(figsize=(width, height))
    # ax.imshow(image)
    # fig.show()
    # input('Press <Enter> to exit')

def get_boundaries(center, span, zoom):
    print('Got boundaries')
    print(center - span/2.**zoom, center + span/2.**zoom)
    return center - span/2.**zoom, center + span/2.**zoom 

if __name__=='__main__':
    image=plot_mandelbulb(degree=8,min_distance=5e-4)
    xsize=image.size
    print(np.amax(image))
    image=3.8*image

    scipy.misc.toimage(image, cmin=0.0, cmax=1,mode='L').save('outfile.png')








