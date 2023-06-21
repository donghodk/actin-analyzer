import numpy as np
from skimage.morphology import skeletonize
from scipy.optimize import curve_fit  # fitting
from sources.class_filament import *







#############################################
#### CLASS FILAMENT GROUP
#############################################


##### TODO
# - add the handlers for the ratios that will soon be coded for the filament class

class filament_group:
    def __init__(self):
        self.filaments = []

    def add_filament(self, filament):
        self.filaments.append(filament)

    def get_skeleton_img_with_len(self, sizeX, sizeY):
        img = np.zeros((sizeX,sizeY)) #might be the other way around
        for i in self.filaments:
            ske = i.skeleton
            for j in ske:
                img[j[0],j[1]] = len(ske)
        return img


    def get_skeleton_img_with_terminal_points(self, sizeX, sizeY):
        img = np.zeros((sizeX,sizeY)) #might be the other way around
        for i in self.filaments:
            ske = i.skeleton
            for j in ske:
                img[j[0],j[1]] = 1
            for j in i.terminal_points:
                img[j[0],j[1]] = 2
        return img


    def get_skeleton_img(self, sizeX, sizeY):
        img = np.zeros((sizeX,sizeY)) #might be the other way around
        for i in self.filaments:
            ske = i.skeleton
            for j in ske:
                img[j[0],j[1]] = 1
        return img




    def get_contour_img_with_len(self, sizeX, sizeY):
        img = np.zeros((sizeX,sizeY)) #might be the other way around
        for i in self.filaments:
            ske = i.contour
            for j in ske:
                img[j[0],j[1]] = len(ske)
        return img
            
            
             

    def filter_on_RL(self, min_length, max_length):  # filter filaments on their raw length
        k = 0
        to_del = []
        for i in self.filaments:
            if (i.raw_length() > max_length or i.raw_length() < min_length):
                to_del.append(k)
            k+=1
        for i in range(len(to_del)):  ## it is a bit weird and not very efficient...
            del self.filaments[to_del[-i-1]]


    def filter_on_SL(self, min_length, max_length): # filter filaments on their skeleton length
        k = 0
        to_del = []
        for i in self.filaments:
            if (i.skeleton_length() > max_length or i.skeleton_length() < min_length):
                to_del.append(k)
            k+=1
        for i in range(len(to_del)):  ## it is a bit weird and not very efficient...
            del self.filaments[to_del[-i-1]]


            
    ########## RAW LENGTH
    def get_raw_lengths(self):
        raw_lengths = []
        for i in self.filaments:
            raw_lengths.append(i.raw_length())
        return raw_lengths

    def get_mean_raw_length(self):
        lengths = self.get_raw_lengths()
        lengths = np.array(lengths)
        return np.mean(lengths)

    def get_std_raw_length(self):
        lengths = self.get_raw_lengths()
        lengths = np.array(lengths)
        return np.std(lengths)


    
    ########## SKELETON LENGTH
    def get_skeleton_lengths(self):
        skeleton_lengths = []
        for i in self.filaments:
            skeleton_lengths.append(i.skeleton_length())
        return skeleton_lengths

    def get_mean_skeleton_length(self):
        lengths = self.get_skeleton_lengths()
        lengths = np.array(lengths)
        return np.mean(lengths)

    def get_std_skeleton_length(self):
        lengths = self.get_skeleton_lengths()
        lengths = np.array(lengths)
        return np.std(lengths)

    ########## THICKNESS PROXY
    def get_thicknesses_proxy(self):
        thicknesses = []
        for i in self.filaments:
            thicknesses.append(i.thickness_proxy())
        return thicknesses

    def get_mean_thicknesses_proxy(self):
        thicknesses = []
        for i in self.filaments:
            thicknesses.append(i.thickness_proxy())
        thicknesses = np.array(thicknesses)
        return np.mean(thicknesses)
    
    def get_std_thicknesses_proxy(self):
        thicknesses = []
        for i in self.filaments:
            thicknesses.append(i.thickness_proxy())
        thicknesses = np.array(thicknesses)
        return np.std(thicknesses)


    ########### BIGGEST DIMENSION RAW
    def get_raw_BD(self):
        raw_BD = []
        for i in self.filaments:
            raw_BD.append(i.biggest_dimension())
        return raw_BD

    def get_mean_BD(self):
        BD = self.get_raw_BD()
        BD = np.array(BD)
        return np.mean(BD)

    def get_std_BD(self):
        BD = self.get_raw_BD()
        BD = np.array(BD)
        return np.std(BD)



    ############## ANGLE
    def get_angles(self):
        angles = []
        for i in self.filaments:
            ang = i.main_angle() # When there is an error, "err" iss removed and only assign the return value to one variable "ang". 2021.11.10
            angles.append(ang)
        return angles

    def get_mean_angle(self):
        angles = self.get_angles()
        angles = np.array(angles)
        return np.mean(angles)

    def get_std_angle(self):
        angles = self.get_angles()
        angles = np.array(angles)
        return np.std(angles)


    def get_filament_index_from_pixel_in_skeleton(self,pixel):
        to_return = -1
        for i in range(len(self.filaments)):
            for j in range(len(self.filaments[i].skeleton)):
                if (self.filaments[i].skeleton[j] == pixel):
                    to_return = i
                    break
        return to_return

    def merge_filaments(self,f1,f2):
        if (f2>f1):
            to_del = self.filaments.pop(f2) # this filament is now removed from the list
            self.filaments[f1].contour += to_del.contour
            self.filaments[f1].compute_skeleton()
            return f1
        else:
            to_del = self.filaments.pop(f1) # this filament is now removed from the list
            self.filaments[f2].contour += to_del.contour
            self.filaments[f2].compute_skeleton()
            return f2
                


    

    def gap_fill(self,max_gap,memory,**kwarg):
        explore = False
        verbose = False
        for key, value in kwarg.items():
            if (key== "explore"):
                explore = value
            if (key== "verbose"):
                verbose = value


        size_x = self.filaments[0].size_x
        size_y = self.filaments[0].size_y
        N_filaments = len(self.filaments)
        current_filament = 0
        map = self.get_skeleton_img(size_x, size_y)

        while (current_filament<N_filaments):  # or < ?
            if (verbose):
                print(" [gap_fill] -> " + str(current_filament)+"/"+str(N_filaments),end="\r")
            if (len(self.filaments[current_filament].skeleton) > 1):
                current_TP = 0
                N_TP = len(self.filaments[current_filament].terminal_points)
                #print(current_filament)
                while (current_TP < N_TP):
                     current_gap = 1
                     #print(self.filaments[current_filament].terminal_points)
                     current_TP_pix = self.filaments[current_filament].terminal_points[current_TP]
                     pending_pix = []
                     d_x,d_y = self.filaments[current_filament].get_tendency_around_TP(current_TP,memory)
                     candidate_pix = []
                     found_good_fil = False
                     if not (d_x==0 and d_y==0):
                         while (current_gap <= max_gap):
                             current_pix = [int(current_TP_pix[0] + current_gap * d_x),int(current_TP_pix[1] + current_gap * d_y)]
                             if not (current_pix[0] >= 0 and current_pix[0] < size_x and current_pix[1] >= 0 and  current_pix[1] < size_y):
                                 break
                             pending_pix.append(current_pix)
                             current_gap += 1
                             found_good_fil = False
                             found_other_fil = False
                             
                             if (map[current_pix[0],current_pix[1]] == 1):
                                 found_other_fil = True
                                 candidate_pix = [current_pix[0],current_pix[1]]
                             if (explore):
                                 for ii in range(-1,2):
                                     for jj in range(-1,2):
                                         if (current_pix[0]+ii >= 0 and current_pix[0]+ii < size_x and current_pix[1]+jj >= 0 and  current_pix[1]+jj < size_y):
                                             if (map[current_pix[0]+ii,current_pix[1]+jj] == 1):
                                                 found_other_fil = True
                                                 candidate_pix = [current_pix[0]+ii,current_pix[1]+jj]
                                         
                             if (found_other_fil):
                                  candidate_fil = self.get_filament_index_from_pixel_in_skeleton(candidate_pix)
                                  
                                  if (candidate_fil != current_filament and candidate_fil != -1):
                                      found_good_fil = True
                                      if (verbose):
                                          print("\n * Found two potential matching filaments: ", current_filament, candidate_fil," at pix", candidate_pix)
                                      current_filament = self.merge_filaments(current_filament, candidate_fil)
                                      for cc in pending_pix:
                                          if not (cc in self.filaments[current_filament].contour):
                                              self.filaments[current_filament].contour.append(cc)
                                          self.filaments[current_filament].compute_skeleton()
                                      #current_filament = 0
                                      current_TP = 0
                             if (found_good_fil):
                                  current_TP = 0
                                  break
                         if (found_good_fil):
                              current_TP = 0
                              break

 
                                      

                         


                     current_TP +=1



            current_filament +=1
            map = self.get_skeleton_img(self.filaments[0].size_x, self.filaments[0].size_y)
            N_filaments = len(self.filaments)


            
            
    
            
            
