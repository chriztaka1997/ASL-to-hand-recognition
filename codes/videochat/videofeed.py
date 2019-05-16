import cv2 as cv
from PIL import Image
import sys
import numpy as np
import os
# import pdb;

class VideoFeed:
    
    # def __init__(self,mode=1,name="w1",capture=1, cameraNum = "w1"):
    def __init__(self, name="w1", cameraNum = "w1"):
        print(name)

        self.camera_index = 0
        self.name=name

        if(cv.VideoCapture().isOpened() == False):
            print("Open webcam " + str(cameraNum)) #laptop camera
            self.capture = cv.VideoCapture(cameraNum)
            if(self.capture.isOpened() == True):
                print("Successfully opened camera")
            else:
                print("Couldn't open camera")
        else:
            print("Cannot access webcam " + cameraNum)
        
        # print("End of VideoFeed _init_")


    def get_frame(self): #captures frames from local machine to send to other user
        # print("Got into get_frame\n")
        if(self.capture.isOpened() == True):
            ret, self.frame = self.capture.read()

            # cv.imshow('test', self.frame)
            # cv.waitKey(0)
            # cv.destroyAllWindows()
            # breakpoint()
            
            height = self.frame.shape[1]
            width = self.frame.shape[0]
            
            jpegImg = Image.frombytes("RGB", (height, width), self.frame.tostring())
            retStr = jpegImg.tobytes("jpeg","RGB")

            return retStr
            
        else:
            sys.exit("camera isn't open")

    def set_frame(self, frame):

        jpegPIL = Image.frombytes("RGB",(640,480),frame,"jpeg","RGB","raw")

        jpegCV = np.array(jpegPIL)
        jpegCV = jpegCV[:,:,::1].copy()
        
        # display image
        # cv.imshow('test', jpegCV)
        # cv.waitKey(0)
        # cv.destroyAllWindows()
        # breakpoint()

        return jpegCV
if __name__=="__main__":
    vf = VideoFeed("test",1)
    while 1:
        m = vf.get_frame()
        vf.set_frame(m)


# if __name__=='__main__':
#     display()
