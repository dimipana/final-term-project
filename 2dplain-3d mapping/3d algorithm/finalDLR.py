from __future__ import print_function

import numpy as np
import cv2

ply_header = '''ply
format ascii 1.0
element vertex %(vert_num)d
property float x
property float y
property float z
property uchar red
property uchar green
property uchar blue
end_header
'''

def write_ply(fn, verts, colors):
    verts = verts.reshape(-1, 3)
    colors = colors.reshape(-1, 3)
    verts = np.hstack([verts, colors])
    with open(fn, 'wb') as f:
        f.write((ply_header % dict(vert_num=len(verts))).encode('utf-8'))
        np.savetxt(f, verts, fmt='%f %f %f %d %d %d ')


def depthExtraction(pair):
    print('loading images...')
    imgL = cv2.pyrDown(pair[0])  # downscale images for faster processing
    imgR = cv2.pyrDown(pair[1]) 

    # disparity range is tuned for 'aloe' image pair
    #window_size = 5
    #min_disp = 16
    #num_disp = 112-min_disp
    stereo = cv2.StereoSGBM_create(minDisparity = 12,
                               numDisparities=64,
                               blockSize=7,
                               P1 = 205,
                               P2 = 480,
                               disp12MaxDiff = 1,
                               uniquenessRatio = 10,
                               speckleWindowSize = 171,
                               speckleRange = 1
    )

    print('computing disparity...')
    disp = stereo.compute(imgL, imgR).astype(np.float32) / 16.0
    cv2.imwrite('disp.jpg', disp)
    print('generating 3d point cloud...',)
    h, w = imgL.shape[:2]
    f = 0.8*w                          # guess for focal length
    Q = np.float32([[1, 0, 0, -0.5*w],
                    [0,-1, 0,  0.5*h], # turn points 180 deg around x-axis,
                    [0, 0, 0,     -f], # so that y-axis looks up
                    [0, 0, 1,      0]])
    points = cv2.reprojectImageTo3D(disp, Q)
    colors = cv2.cvtColor(imgL, cv2.COLOR_BGR2RGB)
    mask = disp > disp.min()
    out_points = points[mask]
    out_colors = colors[mask]
    out_fn = 'out.ply'
    
    write_ply('out.ply', out_points, out_colors)
    print('%s saved' % 'out.ply')

    cv2.imshow('left', imgL)
    cv2.imshow('disparity', (disp-min_disp)/num_disp)
    cv2.waitKey()

cv2.destroyAllWindows()
