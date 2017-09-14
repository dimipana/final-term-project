import math

def objectDistance(pixel_height, pixel_width):

    # In pixels
    img_height = 1200
    img_width = 1600

    # In cm
    cam_height = 21
    a = 48
    b = 52.3
    angle = math.radians(66.4)
    #print("angle: ", angle)

    # Convert pixel height to cm
    h = cam_height * pixel_height / (img_height / 2)
    #print("h: ",h)

    # Law of cosines
    c_sqr = b*b + h*h - 2*b*h*math.cos(angle)
    c = math.sqrt(c_sqr)
    #print("c: ", c)

    # Law of sines
    theta = math.asin(b*math.sin(angle)/c)
    if theta < math.pi:
        theta = math.pi - theta
    #print("theta: ", theta)
        
    # Find d'
    #print("theta': ", math.pi-theta)
    d_small = math.tan(math.pi-theta)*h
    #print("d_small: ", d_small)

    # Final distance from camera
    d = d_small + a
    #print("Distance from camera: ", d)
    
    ##############################################
    ############ Finding the angle ###############
    ##############################################
    
    theta = math.radians(30.25)

    # Find b
    b = math.tan(theta) * d
    #print("b: ", b)

    # Find x and direction (left or right of center)
    x = (pixel_width - img_width/2) * b / (img_width/2)
    if x < 0:
        phi = -1 * math.atan((-x)/d)
        direction = 0
    else:
        phi = math.atan(x/d)
        direction = 1

    # Find the final angle
    phi = math.degrees(phi)    
    #print("Angle: ", phi)
    #if direction:
    #    print("Direction: right")
    #else:
    #    print("Direction: left")
    d = d/100
    #print(d, phi, pixel_height, pixel_width)
    return d, phi
    

