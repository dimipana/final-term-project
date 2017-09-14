import cv2
import numpy as np
from finalDLR import *
#import matplotlib.pyplot as plt
import time
import sys
from motorcontrol import movetime
from motorcontrol import move
import RPi.GPIO as GPIO


def pairPhotos(number):
    #Take a photo, then move slightly and take the other side
    cam = cv2.VideoCapture(0)       #set the port of the camera
       
    cam.set(3, 1600)
    cam.set(4, 1200)
    #
    maxframes = 30
    for i in range(maxframes):
        retval,imageL = cam.read()
        
    cam.release()               #Closes video file or capturing device.
    print("Left taken\n")
    #time.sleep(1)
    cv2.imwrite('left%s.jpg'%number, imageL)
    #cv2.waitKey(10)
    
    
    # Move 8cm to backwards
    movetime(1,0.7)
    move(5)
    GPIO.cleanup()
    time.sleep(1)
    # Take a photo again to be used as right
    
    camR = cv2.VideoCapture(0)
    
    camR.set(3, 1600)
    camR.set(4, 1200)
    
    
    for i in range(maxframes):
        retval,imageR = camR.read()
        
        
    print("Took right\n")
    camR.release()               #Closes video file or capturing device.
    
    time.sleep(1)
    cv2.imwrite('right%s.jpg'%number, imageR)
    
    
    
    # Join the results into a tuple and return the images
    images = (imageL,imageR)
    return (images)



# Main
if __name__ == "__main__":
    print("Initializing mapping ... \n")
    pair = pairPhotos(viewsTaken)
    depthExtraction(pair)
      
    
