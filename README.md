# final-term-project
A multimodal driven RC car which is also capable of extracting a 2D plain from an onboard camera.


## The 2d plain-3d algorithm file includes a subproject which proceded the main one. 
In this subproject, we implemented the basic movement of the robot using only voice commands or hardcoded movements. Our aim was to check whether we could extract depth maps from a single stereo camera. After this attempt fell short cause of the very low point of view the robot had, we converted our interest into making a 2D plain of the room after taking a number of photos.

#### It includes:
1. The code we used for testing a 3D algorithm on the robot's onboard camera, written in python, using the opencv library.
2. The code we used for the main robot movement for this subproject as well as the 2d plain extraction procedure, also written in python and opencv.
3. The report that states some results, tests and conlcusions.


## The Multimodal input movement file contains the whole system code of the main project. It breaks down to three subfiles:
1. *Gesture input*: This file contains the code we used for the gesture input mode, written in C++ .
2. *Voice input* : This file contains the code we used for the voice input mode, written in java using the irisTK platform.
3. *Robot movement*: This file contains the code that run on the robot. The robot is controlled by a raspberry Pi 2 model B so the code is written in python.
#### The file also contains the actual thesis of the project. 


### You can watch a demo of the project here: https://youtu.be/veawjPnT6Nc
