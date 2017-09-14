import sys
import cv2
import time
import numpy
import socket
import RPi.GPIO as GPIO
from threading import Thread

moves = {
    
    'forward':1,
    'backwards':2,
    'left':3,
    'right':4,
    'stop':5,
    'photo':10,
    'finalize':20,
    'exit':0
}

def moveThread():
    global command#
    global closeThreads

    # Gpio setup
    GPIO.cleanup()
    
##    Back = 26
##    Left = 25
##    Right = 5
##    Front = 21
##    All = [Back, Left, Right, Front]
##    
##    GPIO.setmode(GPIO.BCM)
##    GPIO.setup(Back, GPIO.OUT)
##    GPIO.setup(Front, GPIO.OUT)
##    GPIO.setup(Right, GPIO.OUT)
##    GPIO.setup(Left, GPIO.OUT)
##
##    while not closeThreads:
##        if command == 1:
##            GPIO.output(Back, GPIO.LOW)
##            GPIO.output(Left, GPIO.LOW)
##            GPIO.output(Right, GPIO.LOW)
##            GPIO.output(Front, GPIO.HIGH)
##        elif command == 2:
##            GPIO.output(Back, GPIO.HIGH)
##            GPIO.output(Left, GPIO.LOW)
##            GPIO.output(Right, GPIO.LOW)
##            GPIO.output(Front, GPIO.LOW)
##        elif command == 3:
##            GPIO.output(Back, GPIO.LOW)
##            GPIO.output(Left, GPIO.HIGH)
##            GPIO.output(Right, GPIO.LOW)
##            GPIO.output(Front, GPIO.LOW)
##        elif command == 4:
##            GPIO.output(Back, GPIO.LOW)
##            GPIO.output(Left, GPIO.LOW)
##            GPIO.output(Right, GPIO.HIGH)
##            GPIO.output(Front, GPIO.LOW)
##        else:
##            GPIO.output(All, GPIO.LOW)

    GPIO.setmode(GPIO.BOARD)
    
    Motor1A = 35
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

    while not closeThreads:
        if command == 1:
            #print("Going forward")
            GPIO.output(Motor1A,GPIO.HIGH)
            GPIO.output(Motor1B,GPIO.LOW)
            GPIO.output(Motor1E,GPIO.HIGH)
         
            GPIO.output(Motor2A,GPIO.HIGH)
            GPIO.output(Motor2B,GPIO.LOW)
            GPIO.output(Motor2E,GPIO.HIGH)
            time.sleep(0.2)
            
        elif command == 2:
            #print ("Going backwards")
            GPIO.output(Motor1A,GPIO.LOW)
            GPIO.output(Motor1B,GPIO.HIGH)
            GPIO.output(Motor1E,GPIO.HIGH)
                
            GPIO.output(Motor2A,GPIO.LOW)
            GPIO.output(Motor2B,GPIO.HIGH)
            GPIO.output(Motor2E,GPIO.HIGH)
            time.sleep(0.2)
            
        elif command == 3:
            #print ("Turn left")
            GPIO.output(Motor1A,GPIO.LOW)
            GPIO.output(Motor1B,GPIO.HIGH)
            GPIO.output(Motor1E,GPIO.HIGH)
         
            GPIO.output(Motor2A,GPIO.HIGH)
            GPIO.output(Motor2B,GPIO.LOW)
            GPIO.output(Motor2E,GPIO.HIGH)
            time.sleep(0.2)
            
        elif command == 4:
            #print ("Turn right")
            GPIO.output(Motor1A,GPIO.HIGH)
            GPIO.output(Motor1B,GPIO.LOW)
            GPIO.output(Motor1E,GPIO.HIGH)
         
            GPIO.output(Motor2A,GPIO.LOW)
            GPIO.output(Motor2B,GPIO.HIGH)
            GPIO.output(Motor2E,GPIO.HIGH)
            time.sleep(0.2)
            
        else:
            #print ("Else")
            GPIO.output(Motor1E,GPIO.LOW)
            GPIO.output(Motor2E,GPIO.LOW)
            time.sleep(0.2)
            
    command = 5

    GPIO.cleanup()
    print("Move thread closed!\n")
    return


def videoFeedThread(conn, addr):
    global sendFrame
    global connected
    print("This is the video feed thread!\n")

    # Video Camera Initialization
    cap = cv2.VideoCapture(0)
    cap.set(3, 160)
    cap.set(4, 120)
    ret, frame = cap.read()
    height, width, channels = frame.shape
    print(width, height)

    while not closeThreads:
        if sendFrame and connected:
            sendFrame = False
            ret, frame = cap.read()
            try:
                conn.send(frame)
            except:
                print("Could not send!\n")
                break
                
        
    print("Video thread closed!\n")
    return
    

def main():
    global command
    global sendFrame
    global connected
    global closeThreads
    
    # Robot Position and Direction
    robotPos = [0,0]        # Robot position is 0,0 on 2D plain
    robotDir = 90           # Robot direction is 90 degrees
    
    # Socket initialization
    connected = False
    soc = socket.socket()
    host = "###.###.#.##"
    port = '5
    print(host, port)
    soc.bind((host, port))
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    soc.listen(2)

    # Wait for connection
    print("Waiting for first connection . . .")
    conn, addr = soc.accept()

    # Once connected
    print("Got connection from ", addr)
    sendFrame = False
    connected = True

    closeThreads = False
    command = 5
    
    videoFeedThreadID = Thread(target = videoFeedThread, args = (conn, addr))
    videoFeedThreadID.start()
    
    moveThreadID = Thread(target = moveThread, args = ())
    moveThreadID.start()

    conn2, addr2 = soc.accept()
    
    
    while connected:

        try:
            order = conn.recv(16)
            #print(order, '\n')
        except:
            print("could not receive!\n")
            connected = False
            break
                
        if order[:3] == b'ASK':
            sendFrame = True
        elif order[:4] == b'Quit':
            print(order, '\n')
            command = 5
            conn.close()
            connected = False
            closeThreads = True
            break
        elif order[:7] == b'Forward':
            command = 1
        elif order[:9] == b'Backwards':
            command = 2
        elif order[:4] == b'Left':
            command = 3
        elif order[:5] == b'Right':
            command = 4
        else:
            print(order)
            command = 5
        order = b' '

        try:
            order2 = conn2.recv(16)
            #print(order, '\n')
        except:
            print("could not receive!\n")
            connected = False
            break
                
        if order2[:3] == b'ASK':
            sendFrame = True
        elif order2[:4] == b'quit':
            print(order2, '\n')
            command = 5
            conn2.close()
            connected = False
            closeThreads = True
            break
        elif order2[:7] == b'forward':
            command = 1
        elif order2[:9] == b'backwards':
            command = 2
        elif order2[:4] == b'left':
            command = 3
        elif order2[:5] == b'right':
            command = 4
        else:
            print(order2)
            command = 5
        order = b' '


    closeThreads = True
    time.sleep(0.5)
    print("Main out!\n")
    
    
main()
