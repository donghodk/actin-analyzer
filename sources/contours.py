import colorama as cl


def convex_contours(binary_mat):  # I have an idea how to do this, but this is... (Inspired by something on Fast)
    contours = []
    mat = binary_mat.copy()
    for i in range(len(binary_mat)):
        for j in range(len(binary_mat[0])):
            if (mat[i][j] != 0):
                start_pix = [i,j]
                waiting_pix = []
                contour_pix = []
                contour_pix.append(start_pix)
                convex = False
                mat[i][j] = 0
                current_pix = [i,j]
                if (j+1 < len(mat[0]) and mat[current_pix[0]][current_pix[1]+1] != 0):  # should have done an intricated loop…
                    waiting_pix.append([current_pix[0],current_pix[1]+1])
                    mat[current_pix[0],current_pix[1]+1] = 0
                    contour_pix.append([current_pix[0],current_pix[1]+1])
                    
                if (current_pix[1]-1 >= 0 and mat[current_pix[0]][current_pix[1]-1] != 0):
                    waiting_pix.append([current_pix[0],current_pix[1]-1])
                    mat[current_pix[0],current_pix[1]-1] = 0
                    contour_pix.append([current_pix[0],current_pix[1]-1])
                
                if (current_pix[0]+1 < len(mat) and mat[current_pix[0]+1][current_pix[1]] != 0):
                    waiting_pix.append([current_pix[0]+1,current_pix[1]])
                    mat[current_pix[0]+1,current_pix[1]] = 0
                    contour_pix.append([current_pix[0]+1,current_pix[1]])
                    
                if (current_pix[0]-1 >=0 and mat[current_pix[0]-1][current_pix[1]] != 0):
                    waiting_pix.append([current_pix[0]-1,current_pix[1]])
                    mat[current_pix[0]-1,current_pix[1]] = 0
                    contour_pix.append([current_pix[0]-1,current_pix[1]])
                    
                if (current_pix[0]+1 < len(mat) and current_pix[1]+1 < len(mat[0]) and mat[current_pix[0]+1][current_pix[1]+1] != 0):
                    waiting_pix.append([current_pix[0]+1,current_pix[1]+1])
                    mat[current_pix[0]+1,current_pix[1]+1] = 0
                    contour_pix.append([current_pix[0]+1,current_pix[1]+1])
                    
                if ( current_pix[0]+1 < len(mat) and current_pix[1]-1 >= 0 and mat[current_pix[0]+1][current_pix[1]-1] != 0):
                    waiting_pix.append([current_pix[0]+1,current_pix[1]-1])
                    mat[current_pix[0]+1,current_pix[1]-1] = 0
                    contour_pix.append([current_pix[0]+1,current_pix[1]-1])
                    
                if (current_pix[0]-1 >= 0 and current_pix[1]+1 < len(mat[0]) and mat[current_pix[0]-1][current_pix[1]+1] != 0):
                    waiting_pix.append([current_pix[0]-1,current_pix[1]+1])
                    mat[current_pix[0]-1,current_pix[1]+1] = 0
                    contour_pix.append([current_pix[0]-1,current_pix[1]+1])
                    
                if (current_pix[0]-1 >=0 and current_pix[1]-1 >=0 and mat[current_pix[0]-1][current_pix[1]-1] != 0):
                    waiting_pix.append([current_pix[0]-1,current_pix[1]-1])
                    mat[current_pix[0]-1,current_pix[1]-1] = 0
                    contour_pix.append([current_pix[0]-1,current_pix[1]-1])





                

                while (len(waiting_pix) != 0):
                    current_pix = waiting_pix.pop(0)
                    #if (len(contour_pix) > 15 and (abs(current_pix[0] - start_pix[0]) ==1 or abs(current_pix[1] - start_pix[1]) ==1)): convex = True
                    
                    if (current_pix[1]+1 < len(mat[0]) and mat[current_pix[0]][current_pix[1]+1] != 0):  # should have done an intricated loop…
                        waiting_pix.append([current_pix[0],current_pix[1]+1])
                        mat[current_pix[0],current_pix[1]+1] = 0
                        contour_pix.append([current_pix[0],current_pix[1]+1])

                    if (current_pix[1]-1 >= 0 and mat[current_pix[0]][current_pix[1]-1] != 0):
                        waiting_pix.append([current_pix[0],current_pix[1]-1])
                        mat[current_pix[0],current_pix[1]-1] = 0
                        contour_pix.append([current_pix[0],current_pix[1]-1])

                    if (current_pix[0]+1 < len(mat) and mat[current_pix[0]+1][current_pix[1]] != 0):
                        waiting_pix.append([current_pix[0]+1,current_pix[1]])
                        mat[current_pix[0]+1,current_pix[1]] = 0
                        contour_pix.append([current_pix[0]+1,current_pix[1]])

                    if (current_pix[0]-1 >=0 and mat[current_pix[0]-1][current_pix[1]] != 0):
                        waiting_pix.append([current_pix[0]-1,current_pix[1]])
                        mat[current_pix[0]-1,current_pix[1]] = 0
                        contour_pix.append([current_pix[0]-1,current_pix[1]])

                    if (current_pix[0]+1 < len(mat) and current_pix[1]+1 < len(mat[0]) and mat[current_pix[0]+1][current_pix[1]+1] != 0):
                        waiting_pix.append([current_pix[0]+1,current_pix[1]+1])
                        mat[current_pix[0]+1,current_pix[1]+1] = 0
                        contour_pix.append([current_pix[0]+1,current_pix[1]+1])

                    if ( current_pix[0]+1 < len(mat) and current_pix[1]-1 >= 0 and mat[current_pix[0]+1][current_pix[1]-1] != 0):
                        waiting_pix.append([current_pix[0]+1,current_pix[1]-1])
                        mat[current_pix[0]+1,current_pix[1]-1] = 0
                        contour_pix.append([current_pix[0]+1,current_pix[1]-1])

                    if (current_pix[0]-1 >= 0 and current_pix[1]+1 < len(mat[0]) and mat[current_pix[0]-1][current_pix[1]+1] != 0):
                        waiting_pix.append([current_pix[0]-1,current_pix[1]+1])
                        mat[current_pix[0]-1,current_pix[1]+1] = 0
                        contour_pix.append([current_pix[0]-1,current_pix[1]+1])

                    if (current_pix[0]-1 >=0 and current_pix[1]-1 >=0 and mat[current_pix[0]-1][current_pix[1]-1] != 0):
                        waiting_pix.append([current_pix[0]-1,current_pix[1]-1])
                        mat[current_pix[0]-1,current_pix[1]-1] = 0
                        contour_pix.append([current_pix[0]-1,current_pix[1]-1])

                """
                if (convex == True):
                    tamp_mat = mat.copy()
                    tamp_mat = np.array(tamp_mat,dtype = np.int16)
                    for k in range(len(contour_pix)):
                        tamp_mat[contour_pix[k][0],contour_pix[k][1]] = 2
                    print(len(contour_pix))
                    print(contour_pix)
                    plt.pcolormesh(tamp_mat)
                    plt.waitforbuttonpress()
                """
                
                   
                contours.append(contour_pix)
                print("    [Contours.py] > " + cl.Back.GREEN+str(len(contours))+cl.Style.RESET_ALL + " contours found so far\r",end = "")
    print()
    return contours
