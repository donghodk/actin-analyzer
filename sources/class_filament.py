import numpy as np
from skimage.morphology import skeletonize
from scipy.optimize import curve_fit  # fitting
import matplotlib.pyplot as plt  # plotting






def pix_dis(pix1,pix2):
    return np.sqrt((pix1[0]-pix2[0])**2 + (pix1[1]-pix2[1])**2)


def linear_func(x,a,b):
    return a*x+b



#############################################
#### CLASS FILAMENT
#############################################

#### TODO
# - find the angle: maybe the easiest is to fit the filament with a line (curve_fit function) a*x+b and then get the angle from a? (undergoin)
# - approx of curvature: ratio of biggest_dimension and length?
# - get width: ratio of skeleton length vs raw_length?

class filament:    # this is a class (object oriented code, kinda…) it will simplify things in the long run…
    def __init__(self, contour,size_x,size_y):
        self.contour = contour  # this is the contour
        self.skeleton = []   # this is the skeleton of this contour (calculated after)
        self.terminal_points = []
        self.size_x = size_x
        self.size_y = size_y
        self.compute_skeleton()


    
                    
                
    
       
    """          
    def compute_skeleton(self):  # I've an idea of a speed-up here
        self.terminal_points = []
        self.skeleton = []
        tamp_mat = np.zeros((self.size_x,self.size_y))
        small_tamp_mat = np.zeros(())
        for i in range(len(self.contour)):
            tamp_mat[self.contour[i][0], self.contour[i][1]] = 1
        skele = skeletonize(tamp_mat)
        for i in range(len(self.contour)):
            if (skele[self.contour[i][0]][self.contour[i][1]] == 1):  # skeleton is in the contour
            
                self.skeleton.append([self.contour[i][0],self.contour[i][1]])
                N_neighbors = 0
                for ii in range(-1,2):
                    for jj in range(-1,2):
                        if (self.contour[i][0]+ii > 0 and self.contour[i][0]+ii < self.size_x and self.contour[i][1]+jj > 0 and self.contour[i][1]+jj < self.size_y):
                            if (skele[self.contour[i][0]+ii][self.contour[i][1]+jj] == 1):
                                N_neighbors += 1
                if (N_neighbors==2):
                    self.terminal_points.append([self.contour[i][0],self.contour[i][1]])

    """



    
    def compute_skeleton(self):  # Sped up version
        self.terminal_points = []
        self.skeleton = []
        contour_np = np.array(self.contour)
        contour_np = contour_np.T
        tamp_mat = np.zeros((self.size_x,self.size_y))
        mm_x = [np.amin(contour_np[0]),np.amax(contour_np[0])]
        mm_y = [np.amin(contour_np[1]),np.amax(contour_np[1])]
        small_tamp_mat = np.zeros((mm_x[1]-mm_x[0]+1,mm_y[1]-mm_y[0]+1)) # no need to skeletonize something filled with zeros, let's work with a small one instead and then paste it in the big one
        for i in range(len(self.contour)):
            #tamp_mat[self.contour[i][0], self.contour[i][1]] = 1
            small_tamp_mat[self.contour[i][0]-mm_x[0],self.contour[i][1]-mm_y[0]] = 1
        skele = skeletonize(small_tamp_mat)
        tamp_mat[mm_x[0]:mm_x[1]+1,mm_y[0]:mm_y[1]+1] = skele
        skele = tamp_mat.copy()
        for i in range(len(self.contour)):
            if (skele[self.contour[i][0]][self.contour[i][1]] == 1):  # skeleton is in the contour
            
                self.skeleton.append([self.contour[i][0],self.contour[i][1]])
                N_neighbors = 0
                for ii in range(-1,2):
                    for jj in range(-1,2):
                        if (self.contour[i][0]+ii > 0 and self.contour[i][0]+ii < self.size_x and self.contour[i][1]+jj > 0 and self.contour[i][1]+jj < self.size_y):
                            if (skele[self.contour[i][0]+ii][self.contour[i][1]+jj] == 1):
                                N_neighbors += 1
                if (N_neighbors==2):
                    self.terminal_points.append([self.contour[i][0],self.contour[i][1]])





                    
        
        
                
    def raw_length(self):
        return len(self.contour)

    def skeleton_length(self):
        return len(self.skeleton)

    def thickness_proxy(self):
        return len(self.contour) / len(self.skeleton)

    def biggest_dimension(self):
        tamp_max = 0
        for i in range(len(self.contour)):
            for j in range(len(self.contour)):
                dis = pix_dis(self.contour[i],self.contour[j])
                if dis > tamp_max:
                    tamp_max = dis
        return tamp_max

    def main_angle(self):
        X = []
        Y = []
        for i in range(len(self.skeleton)):
            X.append(self.skeleton[i][0])
            Y.append(self.skeleton[i][1])
        try:
            popt,pcov = curve_fit(linear_func, X,Y)
            #print(popt)
            return (np.arctan(popt[0]),0)  # the error on a (pcov) carries some info on the straightness of the filament, but cannot be used "as it". We need to propagate it through the arctan. I am putting it to 0 for now.
        except:
            print("/!\ Not enougth point to fit a line!")
            return(np.nan)
            


    def get_tendency_around_pix(self, pix, distance):
        for i in range(len(self.skeleton)):
            d_x = 0
            d_y = 0
            N = 0
            dis = np.sqrt((pix[0] - self.skeleton[i][0])**2 + (pix[1] - self.skeleton[i][1])**2)
            if (dis < distance and dis > 0):
                d_x += (pix[0] - self.skeleton[i][0])/dis
                d_y += (pix[1] - self.skeleton[i][1])/dis
                N+=1
        if (N != 0):
            d_x /= N
            d_y /= N


            max_d = max(np.abs(d_x),np.abs(d_y))
            d_x /= max_d
            d_y /= max_d

        return d_x,d_y


    def get_tendency_around_TP(self, TP, distance):
        return self.get_tendency_around_pix(self.terminal_points[TP],distance)
                








            
