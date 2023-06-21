#!/usr/bin/python3

"""
T. Combriat. 2020
Program to get features from fluorescence images, especially actin filaments
Dongho_branch
"""

print()
print("***********************************************************")
print("************************* AA ******************************")
print("***************************************** Kwak/Combriat2020")
print()

#################
# library imports
#################
import matplotlib.pyplot as plt  # plotting
import numpy as np  # numerics
#import math as math  # math
#import skvideo.io  # video opener
import skimage.io as io
#import skimage.color
#from skimage.filters import threshold_otsu
#from skimage.feature import peak_local_max
#from scipy.ndimage.filters import gaussian_filter
#from scipy.ndimage.filters import laplace
#from scipy.ndimage.filters import gaussian_gradient_magnitude
#from scipy.ndimage import maximum_filter
from skimage.morphology import skeletonize
from skimage import filters
#from scipy import fftpack
from tqdm import tqdm  # fancy progress bar
#from scipy.optimize import curve_fit  # fitting
import os  as os # folder and file manipulation
#from scipy.signal import savgol_filter
import colorama as cl
import cv2
import pandas as pd

cl.init()

########################
# local imports
########################
from sources.im_utils import *
from sources.contours import *
from sources.class_filament import *
from sources.class_filament_group import *
from parameters import *

def my_histogram(a, n,rang):
    hist, bin_edges = np.histogram(a,bins = n,range = rang)
    centers = []
    for i in range(len(hist)):
        centers.append((bin_edges[i]+bin_edges[i+1])/2)
    return hist,centers

""" TODO
  - opening the files (BEWARE: this has to be all-OS compatible (use os.sep to navigate and not "/" or "\\".))  DONE
  - enhance contrast DONE
  - find the pixels belonging to actin fibers  DONE
  - feed these pixels into a "well-defined" filament object  DONE
  - implement method for this object to compute the parameters we want  undergoing
"""

#####################
## Global data containers
names = []
skeleton_lengths = []
skeleton_angles = []
skeleton_thickness = []
threshold_value = 0
sep = os.sep

## Parameters
skeleton_length_low_threshold = 1 #For line 174-175
gap_threshold = 5 #For line 207
skeleton_length_low_threshold_after_gap = 10 #For line 222, comment out that line and plot below that if not using this parameter

try:
    os.mkdir(output_folder)
except:
    print("Folder already created!")

ls = os.listdir(input_folder)

for i in ls:
    if (i.split("_")[-1] == "img1.tif"):
    
        names.append(str(i))

        print(cl.Fore.BLUE + "- Opening file: " + cl.Style.RESET_ALL + cl.Back.BLUE + i + cl.Style.RESET_ALL)

        #### Loading an image, applying a few filters
        raw_img = io.imread(input_folder + sep + i) #These are more than 8bits images
        #raw_img = gaussian_filter(raw_img, sigma=10)        
        raw_img = cv2.cvtColor(raw_img, cv2.COLOR_BGR2GRAY)
        raw_img = np.stack((raw_img,raw_img,raw_img), axis=2)
        raw_green = raw_img[:,:,1]
        lap_green = scaled_laplace(raw_img[:,:,1])
        #max_fil_green = maximum_filter(lap_green,5)
        #grad_green = gaussian_gradient_magnitude(lap_green,7)
        #scharr_green = filters.scharr(lap_green)

        #### Automatically finding a good threshold value: the mean of laplacian corresponds to the background, we take only pixels that are away of one std from this mean
        threshold_value = np.mean(lap_green.flatten())-np.std(lap_green.flatten())
        print(cl.Fore.BLUE + "Taking an automatic threshold value of " + cl.Style.RESET_ALL + cl.Back.BLUE + str(threshold_value) + cl.Style.RESET_ALL)

        thresholded_img = lap_green < np.array(filters.threshold_local(lap_green,25,offset = -threshold_value))
       
        #### Create a square mesh for plotting using matplotlib
        XX,YY  = np.meshgrid(np.arange(len(raw_green[0])), np.arange(len(raw_green)))

        ####################################################
        ############ PLOT ##################################
        ####################################################
        
        if (plot_img):
            ## Trying to figure an algo, will need to be put in a function in the end

            fig = plt.figure()
            ax1 = fig.add_subplot(2,2,1)
            ax1.title.set_text("Original image")
            ax1.pcolormesh(XX,YY,raw_green)
            ax1.invert_yaxis()
            #ax1.imshow(raw_green)
            #plt.show()
            #plt.colorbar()


            ax2 = fig.add_subplot(2,2,2,sharex=ax1,sharey=ax1)
            ax2.title.set_text("Laplacian")
            ax2.pcolormesh(XX,YY,lap_green)
            #ax2.imshow(lap_green)
            #plt.colorbar()


            ax3 = fig.add_subplot(2,2,3,sharex=ax1,sharey=ax1)
            ax3.title.set_text("Threshold local")
            ax3.pcolormesh(XX,YY,thresholded_img, shading = "nearest")
            #ax3.pcolormesh(XX,YY,lap_green<-500) ## thresholding


            ax4 = fig.add_subplot(2,2,4,sharex=ax1,sharey=ax1)
            ax4.title.set_text("Skeleton")
            ax4.pcolormesh(XX,YY,skeletonize(thresholded_img), shading = "nearest")

            
            ### HESSIAN FILTER
            #ax5 = fig.add_subplot(2,3,6)
            #ax5.title.set_text("Hybrid Hessian filter")
            #ax5.imshow(hessian(raw_green), cmap=plt.cm.gray)
            

            ax1.set_aspect("equal")    
            ax2.set_aspect("equal")
            ax3.set_aspect("equal")
            ax4.set_aspect("equal")
            #ax5.set_aspect("equal")

            plt.tight_layout()
            plt.show()

        #########################################
        ########## FINDING FILAMENTS ############
        #########################################
            
        print(cl.Fore.BLUE + "- Finding the contours... " + cl.Style.RESET_ALL)
        contours = convex_contours(lap_green < np.array(filters.threshold_local(lap_green,25,offset = -threshold_value)))

        print(cl.Fore.BLUE + "- Grouping the contours and computing skeletons... " + cl.Style.RESET_ALL)
        filaments = filament_group()
        for j in tqdm(range(len(contours))):
            filaments.add_filament(filament(contours[j],len(raw_green),len(raw_green[0])))
        print(cl.Fore.GREEN + "    Done! " + cl.Style.RESET_ALL)
        
        print(cl.Fore.BLUE + "- Filtering... " + cl.Style.RESET_ALL)
        filaments.filter_on_SL(skeleton_length_low_threshold,np.inf)

        filtered_filaments = filaments.get_skeleton_img_with_terminal_points(len(raw_green),len(raw_green[0]))
        
        if (plot_img):
            fig = plt.figure()
            
            ax1 = fig.add_subplot(2,2,1)
            ax1.title.set_text("Original image")
            ax1.pcolormesh(XX,YY,raw_green, shading = "nearest")
            ax1.invert_yaxis()
            #ax1.colorbar()

            #ax2 = fig.add_subplot(2,2,2, sharex=ax1, sharey=ax1)
            #ax2.title.set_text("Selected filaments (low_thrs={})".format(skeleton_length_low_threshold))
            #ax2.pcolormesh(XX,YY,filtered_filaments,shading = "nearest")
            #ax2.colorbar()
            
            ax2 = fig.add_subplot(2,2,2, sharex=ax1, sharey=ax1)
            ax2.title.set_text("Selected filaments before filling (low_thrs={})".format(skeleton_length_low_threshold))
            ax2.pcolormesh(XX,YY,filtered_filaments,shading = "nearest")

            #ax3 = fig.add_subplot(2,2,3,sharex=ax1,sharey=ax1)
            #ax3.title.set_text("Selected filaments before filling (low_thrs={})".format(skeleton_length_low_threshold))
            #ax3.pcolormesh(XX,YY,filtered_filaments.copy())  
            #ax3.colorbar()
    
        print(len(filaments.filaments))
        filaments.gap_fill(gap_threshold,50,explore=True,verbose=False)
        print(len(filaments.filaments))
        
        filtered_filaments = filaments.get_skeleton_img_with_terminal_points(len(raw_green),len(raw_green[0]))
        
        if (plot_img):
            ax3 = fig.add_subplot(2,2,3,sharex=ax1,sharey=ax1)
            ax3.title.set_text("Selected filaments after filling (gap_thrs={})".format(gap_threshold))
            ax3.pcolormesh(XX,YY,filtered_filaments.copy())
            
            #ax4 = fig.add_subplot(2,2,4,sharex=ax1,sharey=ax1)
            #ax4.title.set_text("Selected filaments after filling (low_thrs={})".format(skeleton_length_low_threshold))
            #ax4.pcolormesh(XX,YY,filtered_filaments.copy())
            #ax4.colorbar()
        
        filaments.filter_on_SL(skeleton_length_low_threshold_after_gap,np.inf)
        filtered_filaments = filaments.get_skeleton_img_with_terminal_points(len(raw_green),len(raw_green[0]))
        filtered_filaments = np.ma.masked_array(filtered_filaments, filtered_filaments < 0.1)

        if (plot_img):        
            ax4 = fig.add_subplot(2,2,4,sharex=ax1,sharey=ax1)
            ax4.title.set_text("Selected filaments final (low_thrs={})".format(skeleton_length_low_threshold_after_gap))
            ax4.pcolormesh(XX,YY,raw_green,shading='nearest')
            ax4.pcolormesh(XX,YY,filtered_filaments.copy(),cmap='YlOrBr')
            
            ax1.set_aspect("equal")
            ax2.set_aspect("equal")
            ax3.set_aspect("equal")
            ax4.set_aspect("equal")
            
            plt.tight_layout()
            plt.show()
            
            #import plotly.io as pio
            #pio.write_html(fig, file="Ex1_Hela_cont_15min_2_top_Out_MIP.html", auto_open=True) 

        print(cl.Fore.GREEN + "    Done!" + cl.Style.RESET_ALL)
        #print(cl.Back.GREEN + "    Raw statistics:" + cl.Style.RESET_ALL)

        #print("    Raw length:",(filaments.get_mean_raw_length()),"+/-", filaments.get_std_raw_length())
        #print("    Skeleton length:",(filaments.get_mean_skeleton_length()),"+/-", filaments.get_std_skeleton_length())
        #print("    Mean angle:",(filaments.get_mean_angle()),"+/-", filaments.get_std_angle())
        #print("    Mean thickness:",(filaments.get_mean_thicknesses_proxy()))

        skeleton_lengths.append(filaments.get_skeleton_lengths())
        skeleton_angles.append(filaments.get_angles())
        skeleton_thickness.append(filaments.get_thicknesses_proxy())

        #hist,centers = my_histogram(filaments.get_skeleton_lengths(),50,(2,200))
        #plt.plot(centers,hist,label = str(i))
        #plt.hist(filaments.get_skeleton_lengths(),bins = 50)
        #plt.show()

        #filaments.filter_on_RL(1,2)
        #print((filaments.get_mean_BD()),"+/-", filaments.get_std_BD())
        #print((filaments.get_mean_length()),"pm", filaments.get_std_length())

        ##### TODO
        # - compute the histogram  DONE: Need to find a way to label
        # - find good values for the filters ONGONING...
        # - export the data ONGOING...

#plt.legend()
#plt.show()
#plt.legend()
#plt.yscale('log')
#plt.show()

#plt.boxplot(skeleton_lengths, labels = names)
#plt.title('Boxplot: skeleton lenghts')
#plt.ylabel('Skeleton lengths')
#if (export_plots):
#    plt.savefig(output_folder + sep + "Boxplot_of_skeleton_lengths.png")

#plt.hist(skeleton_lengths, 50, label = names)
#plt.title("Histogram: skeleton lengths")
#plt.xlabel('Skeleton lengths')
#plt.ylabel('# of filaments')
#if (export_plots):
#    plt.savefig(output_folder + sep +"Histogram_of_skeleton_lengths.png")

#plt.boxplot(skeleton_angles,labels = names)
#plt.title("Skeleton_angles")
#plt.show()

# data exports
Skeleton_names = pd.DataFrame(names)
Lengths = pd.DataFrame(skeleton_lengths)
Angles = pd.DataFrame(skeleton_angles)
Thickness = pd.DataFrame(skeleton_thickness)

Skeleton_names.to_csv('nv_names.csv')
Lengths.to_csv('nv_lengths.csv')
Angles.to_csv('nv_angles.csv')
Thickness.to_csv('nv_thickness.csv')

