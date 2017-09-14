import cv2
import numpy as np
from matplotlib import pyplot as plt
from distance import *

def mapping(im):
#def mapping(picture_name):
    
    #im = cv2.imread(picture_name + '.jpg')

    ###########################################
    ## Convert to grayscale and then to binary
    ###########################################
    imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    cv2.imwrite('gray.jpg',imgray)
    ret,thresh = cv2.threshold(imgray,100,1,cv2.THRESH_TOZERO)
    #cv2.imwrite('thresh.jpg',thresh)
    im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(im2, contours, -1, (255,255,0), 10)
    #cv2.imwrite(picture_name + '_lines.jpg',im2)
    #plt.imshow(im2,'gray')
    #plt.show()
    
    #########################################################
    ## Use only a portion of image for more accurate results
    #########################################################
    #crop_img = im2[1500:2390, 800:2400]
    height, width = im2.shape 
    crop_img = im2[(height/2)+100:(height), (width/2-650):(width/2+650)]
    cv2.imwrite('cropped.jpg',crop_img)
    #pixelpoints = cv2.findNonZero(crop_img)
    #print(pixelpoints)

    ####################################
    ## Create a list with the obstacles
    ####################################
    obstacles = [ ]
    crop_height, crop_width = crop_img.shape
    print("Begin loop")
    for x in range(crop_width-1):
        for y in range(crop_height-10, 0, -1):
            if crop_img[y,x] == 255:
                #print("(%d, %d)", x, y)
                #obstacle[y,x] = crop_img[y,x]
                obstacles.append(objectDistance(crop_height-y, x))
                
                break
    print("End loop")            

    #plt.imshow(crop_img,'gray')
    #plt.show()
    
    return obstacles
    #blur = cv2.GaussianBlur(imgray,(5,5),0)
    #ret3,im2 = cv2.threshold(blur,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

#mapping('testedge9')

