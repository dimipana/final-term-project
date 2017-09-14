import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import math


# Draws a list of points in 2D Figure
def drawPoints(points, robPos, robDir):
    dx=[]
    dy=[]
    for i in range(0,len(points)):
        
        hypotenuse = points[i][0]/math.cos(math.radians(points[i][1]))
        w = robDir-points[i][1]
        
        dx.append(robPos[0] + math.cos(math.radians(w))*hypotenuse)
        dy.append(robPos[1] + math.sin(math.radians(w))*hypotenuse)
	
    plt.plot(dx, dy, 'r.')
    plt.plot(robPos[0],robPos[1], 'g*')
    for i in range(0,4):   
        print(dx[i])
        print(dy[i])    

