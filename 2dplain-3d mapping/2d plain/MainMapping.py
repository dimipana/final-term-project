import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import cv2
import numpy as np
import sys
import math
from pictureMap import mapping
from motorcontrol import movetime
from draw2D import drawPoints
import tty
import termios

def commands():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    tty.setraw(sys.stdin.fileno())
    command = 0
    
    ch = []
    ch.append(sys.stdin.read(1))
    
    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)    
    if ch[0] == '\x1b':
        ch.append(sys.stdin.read(1))
        if ch[1] == '[':
            ch.append(sys.stdin.read(1))
            if ch[2] == 'A':
                command = 1
            elif ch[2] == 'B':
                command = 2
            elif ch[2] == 'D':
                command = 3
            elif ch[2] == 'C':
                command = 4
        else:
            command = 0
    else:
        if ch[0] == 'p':
            command = 5
        elif ch[0] == 'q':
            command = 6
            
    return command



def main():

# User choose to either move the robot, take a photo where the robot stands
# or finalize the mapping
    
    robotPos=[0,0]           # Set robot position to 0,0 in 2D plain
    robotDir = 90            # and robot direction to 90, thus looking up
    plt.axis([-2,2,-3,3])    # Set the axis to be 4*4 meters

    print("\n \n Press the arrow keys to move the robot, space key to take a photo or q key to finalize the mapping \n")        #Wait for a command
    while(1):
        key=commands()
        
        if (key==0):
            print("ERROR: NOT A VALID COMMAND \n")
            sys.exit(0)
############################## PHOTO COMMAND ######################################    
        elif (key == 5):
            print("mpika")
            cam = cv2.VideoCapture(0)       #set the port of the camera
            cam.set(3, 3200)                #set the resolution and frames
            cam.set(4, 2380)
            resolution = [cam.get(3),cam.get(4)]
            fps = cam.get(5)
            print (resolution)
            print(fps)
            maxframes = 10
            for i in range(maxframes):
                ret,ImToMap = cam.read()
                if(ret==0):
                    sys.exit(0)
            
            cam.release()                   #Closes capturing device.
            obstacles = mapping(ImToMap)    #Computes obstacles
            print("Start Drawing \n")   
            drawPoints(obstacles,robotPos, robotDir)    #Draws the obstacles
            print("Finished Drawing \n")
            
############################ END PHOTO COMMAND #################################

############################## FINALIZE COMMAND #################################        
        elif (key == 6):
            print("Start Finalizing \n")
            plt.savefig('finalmapping.png')
            print("Finished Finalizing \n")
            print("Exiting... \n")
            #sys.exit(0)
            continue
############################## END FINALIZE COMMAND ##############################

############################## MOVE COMMAND ####################################
        else:
            offset = movetime(key,0.5)
            if (key < 3):        							# if the robot goes forward
                dx = math.cos(math.radians(robotDir))*offset
                dy = math.sin(math.radians(robotDir))*offset
                                
                robotPos = [robotPos[0]+dx,robotPos[1]+dy]            # set the new position of the robot

            else:
                robotDir = robotDir + offset       # otherwise, set the new direction of the camera
                if (robotDir <0 ):
                    robotDir = robotDir +360
                elif (robotDir >360):
                    robotDir = robotDir -360
                elif (robotDir==360):
                    robotDir =0
            print(robotDir)
            print(robotPos)
############################## END MOVE COMAND #################################

main()