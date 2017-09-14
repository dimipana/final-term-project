###########################################################
# Function that is called every time the car receives a   #
# command from the socket, to control the movement of the #
# vehicle.                                                #
###########################################################

import RPi.GPIO as GPIO
import time 

def move(direction):
################### GPIO initialization ################### 
    GPIO.setmode(GPIO.BOARD)
    
    Motor1A = 7
    Motor1B = 11
    Motor1E = 13
     
    Motor2A = 12
    Motor2B = 16
    Motor2E = 18

    GPIO.setup(Motor1A,GPIO.OUT)
    GPIO.setup(Motor1B,GPIO.OUT)
    GPIO.setup(Motor1E,GPIO.OUT)
     
    GPIO.setup(Motor2A,GPIO.OUT)
    GPIO.setup(Motor2B,GPIO.OUT)
    GPIO.setup(Motor2E,GPIO.OUT)
    
###########################################################
    
###################### Stop command #######################
    if (direction==5):
        print ("Stop")
        GPIO.output(Motor1E,GPIO.LOW)
        GPIO.output(Motor2E,GPIO.LOW)
        
###########################################################     

################ Going forward command ####################
    elif(direction==1):
        print ("Going forwards")
        GPIO.output(Motor1A,GPIO.HIGH)
        GPIO.output(Motor1B,GPIO.LOW)
        GPIO.output(Motor1E,GPIO.HIGH)
         
        GPIO.output(Motor2A,GPIO.HIGH)
        GPIO.output(Motor2B,GPIO.LOW)
        GPIO.output(Motor2E,GPIO.HIGH)
        
###########################################################

############### Going backwards command ###################
    elif (direction==2):
        print ("Going backwards")
        GPIO.output(Motor1A,GPIO.LOW)
        GPIO.output(Motor1B,GPIO.HIGH)
        GPIO.output(Motor1E,GPIO.HIGH)
         
        GPIO.output(Motor2A,GPIO.LOW)
        GPIO.output(Motor2B,GPIO.HIGH)
        GPIO.output(Motor2E,GPIO.HIGH)
        
########################################################### 

################# Turn right command ######################
    elif (direction==4):
        print ("Turn right")
        GPIO.output(Motor1A,GPIO.HIGH)
        GPIO.output(Motor1B,GPIO.LOW)
        GPIO.output(Motor1E,GPIO.HIGH)
         
        GPIO.output(Motor2A,GPIO.LOW)
        GPIO.output(Motor2B,GPIO.HIGH)
        GPIO.output(Motor2E,GPIO.HIGH)
        time.sleep(0.3)
        GPIO.output(Motor1E,GPIO.LOW)
        GPIO.output(Motor2E,GPIO.LOW)
        
########################################################### 

################## Turn left command ######################
    elif (direction==3):
        print ("Turn left")
        GPIO.output(Motor1A,GPIO.LOW)
        GPIO.output(Motor1B,GPIO.HIGH)
        GPIO.output(Motor1E,GPIO.HIGH)
         
        GPIO.output(Motor2A,GPIO.HIGH)
        GPIO.output(Motor2B,GPIO.LOW)
        GPIO.output(Motor2E,GPIO.HIGH)
        time.sleep(0.3)
        GPIO.output(Motor2E,GPIO.LOW)
        GPIO.output(Motor1E,GPIO.LOW)
########################################################### 

    else:
        print ("No command given")
 

def movetime(direction, movetime):
################### GPIO initialization ###################
    mpersec = 0.14
    degpersecL = 99.2
    degpersecR = 91.8 
    
    GPIO.setmode(GPIO.BOARD)
    
    Motor1A = 7
    Motor1B = 11
    Motor1E = 13
     
    Motor2A = 12
    Motor2B = 16
    Motor2E = 18

    GPIO.setup(Motor1A,GPIO.OUT)
    GPIO.setup(Motor1B,GPIO.OUT)
    GPIO.setup(Motor1E,GPIO.OUT)
     
    GPIO.setup(Motor2A,GPIO.OUT)
    GPIO.setup(Motor2B,GPIO.OUT)
    GPIO.setup(Motor2E,GPIO.OUT)
    
###########################################################
    
###################### Stop command #######################
    if (direction==5):
        print ("Stop")
        GPIO.output(Motor1E,GPIO.LOW)
        GPIO.output(Motor2E,GPIO.LOW)
        
###########################################################     

################ Going forward command ####################
    elif(direction==1):
        print ("Going forwards")
        GPIO.output(Motor1A,GPIO.HIGH)
        GPIO.output(Motor1B,GPIO.LOW)
        GPIO.output(Motor1E,GPIO.HIGH)
         
        GPIO.output(Motor2A,GPIO.HIGH)
        GPIO.output(Motor2B,GPIO.LOW)
        GPIO.output(Motor2E,GPIO.HIGH)
        time.sleep(movetime)
        GPIO.output(Motor1E,GPIO.LOW)
        GPIO.output(Motor2E,GPIO.LOW)
        return (movetime*mpersec)
###########################################################

############### Going backwards command ###################
    elif (direction==2):
        print ("Going backwards")
        GPIO.output(Motor1A,GPIO.LOW)
        GPIO.output(Motor1B,GPIO.HIGH)
        GPIO.output(Motor1E,GPIO.HIGH)
                
        GPIO.output(Motor2A,GPIO.LOW)
        GPIO.output(Motor2B,GPIO.HIGH)
        GPIO.output(Motor2E,GPIO.HIGH)
        time.sleep(movetime)
        GPIO.output(Motor1E,GPIO.LOW)
        GPIO.output(Motor2E,GPIO.LOW)
        return (-movetime*mpersec)
########################################################### 

################# Turn right command ######################
    elif (direction==4):
        print ("Turn right")
        GPIO.output(Motor1A,GPIO.HIGH)
        GPIO.output(Motor1B,GPIO.LOW)
        GPIO.output(Motor1E,GPIO.HIGH)
         
        GPIO.output(Motor2A,GPIO.LOW)
        GPIO.output(Motor2B,GPIO.HIGH)
        GPIO.output(Motor2E,GPIO.HIGH)
        time.sleep(movetime)
        GPIO.output(Motor1E,GPIO.LOW)
        GPIO.output(Motor2E,GPIO.LOW)
        return (-movetime*degpersecR)
########################################################### 

################## Turn left command ######################
    elif (direction==3):
        print ("Turn left")
        GPIO.output(Motor1A,GPIO.LOW)
        GPIO.output(Motor1B,GPIO.HIGH)
        GPIO.output(Motor1E,GPIO.HIGH)
         
        GPIO.output(Motor2A,GPIO.HIGH)
        GPIO.output(Motor2B,GPIO.LOW)
        GPIO.output(Motor2E,GPIO.HIGH)
        time.sleep(movetime)
        GPIO.output(Motor2E,GPIO.LOW)
        GPIO.output(Motor1E,GPIO.LOW)
        return (movetime*degpersecL)
########################################################### 

    else:
        print ("No command given")
 

    
