import numpy as np
import scipy
from PIL import Image
from scipy import misc
import os
obpos = np.array([0,0,4])
power = 0.2
size = 100
def DistanceEstimator(plane_points):
        '''I think theis also does mandelbulb set calculations?'''
        m = plane_points.shape[0]
        x, y, z = np.zeros(m), np.zeros(m), np.zeros(m)
        x0, y0, z0 = plane_points[:, 0], plane_points[:, 1], plane_points[:, 2]
        dr = np.zeros(m) + 1
        r = np.zeros(m)
        theta = np.zeros(m)
        phi = np.zeros(m)
        zr = np.zeros(m)
        for _ in range(32):
            r = np.sqrt(x*x + y*y + z*z)
            idx1 = r < 2**20 # this sets the radius threshold, cannot exceed radius 1000 (default)
            dr[idx1] = np.power(r[idx1], 8 - 1) * 8 * dr[idx1] + 1.0
            theta[idx1] = np.arctan2(np.sqrt(x[idx1]*x[idx1] + y[idx1]*y[idx1]), z[idx1])
            phi[idx1] = np.arctan2(y[idx1], x[idx1])
            zr[idx1] = r[idx1] ** 8
            theta[idx1] = theta[idx1] * 8
            phi[idx1] = phi[idx1] * 8
            x[idx1] = zr[idx1] * np.sin(theta[idx1]) * np.cos(phi[idx1]) + x0[idx1]
            y[idx1] = zr[idx1] * np.sin(theta[idx1]) * np.sin(phi[idx1]) + y0[idx1]
            z[idx1] = zr[idx1] * np.cos(theta[idx1]) + z0[idx1]
        return(0.5 * np.log(r) * r / dr)

x = np.linspace(-1.2, 1.2, size)
y = np.linspace(-1.2, 1.2, size)
x, y = np.meshgrid(x, y)
x, y = x.ravel(), y.ravel()
z = x + y 
plane_points = np.vstack((x,y,z)).T
v = np.array(plane_points - obpos)
v = v/np.linalg.norm(v, axis=1)[:, np.newaxis]
directions = v 
total_distance = np.zeros(directions.shape[0])
keep_iterations = np.ones_like(total_distance)
steps = np.zeros_like(total_distance)
for _ in range(32):
            positions = obpos[np.newaxis, :] + total_distance[:, np.newaxis] * directions
            distance = DistanceEstimator(positions) 
            keep_iterations[distance < 1e-3] = 0
            total_distance += distance * keep_iterations
            steps += keep_iterations
print(steps)
def NumPy2PIL(input):
    """Converts a numpy array to a PIL image.

    Supported input array layouts:
       2 dimensions of numpy.uint8
       3 dimensions of numpy.uint8
       2 dimensions of numpy.float32
    """
    if not isinstance(input, np.ndarray):
        raise TypeError('Must be called with numpy.ndarray!')
    # Check the number of dimensions of the input array
    ndim = input.ndim
    if not ndim in (2, 3):
        raise ValueError('Only 2D-arrays and 3D-arrays are supported!')
    if ndim == 2:
        channels = 1
    else:
        channels = input.shape[2]
    # supported modes list: [(channels, dtype), ...]
    modes_list = [(1, np.uint8), (3, np.uint8), (1, np.float32), (4,np.uint8)]
    mode = (channels, input.dtype)
    if not mode in modes_list:
        raise ValueError('Unknown or unsupported input mode')
    return Image.fromarray(input) 

print(positions)
print(distance)
image = 1 - (steps/32)**power
image = image.reshape(size, size)
print(image)
arraymax = np.amax(image)
#print(arraymax)
image = (1/arraymax)*image 
print(image)
#image = image

for i in range(len(image)):
    for j in range(len(image[i])):
        image[j][i] = np.uint32(255 * image[i][j])


print(image)

im = Image.fromarray(image, mode='RGB')
#im = im.convert(mode='HSV')
im = im.save(os.getcwd()+'/frames/frame50.png')










