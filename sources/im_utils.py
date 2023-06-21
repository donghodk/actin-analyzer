import numpy as np  # numerics
import math as math  # math
import skimage.io as io
import skimage.color
from skimage.filters import threshold_otsu
from skimage.feature import peak_local_max
from scipy.ndimage.filters import gaussian_filter
from scipy.ndimage.filters import laplace
from scipy.ndimage.filters import gaussian_gradient_magnitude


def scaled_laplace(arr):
    lap = np.array(laplace(gaussian_filter(arr,1),output = np.float))
    max_lap = np.max(np.array(lap).flatten()) #haha
    #return lap *((1./max_lap) )  # yes or no ?
    return lap