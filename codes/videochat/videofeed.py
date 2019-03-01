import cv2 as cv
from PIL import Image

class VideoFeed:

    def __init__(self,mode=1,name="w1",capture=1):
        print name
        if mode == 1:
            cv.startWindowThread()
            cv.namedWindow(name, cv.WINDOW_AUTOSIZE)
        self.camera_index = 0
        self.name=name
        if capture == 1:
            #old code
            # self.capture = cv.CaptureFromCAM(self.camera_index)
            self.capture = cv.VideoCapture(0)

        #Testing
        # while(True):
        #     ret, frame = self.capture.read()
        #     cv.imshow("Live web cam test", frame)
        #
        #     key = cv.waitKey(1)
        #     if key in [27, 81, 113]:
        #         break
        #
        # cap.release()
        # cv.destroyAllWindows()

    def get_frame(self):
        ret, self.frame = self.capture.read()
        self.c = cv.WaitKey(1)
        #code might be for switching cams
        # if(self.c=="n"): #in "n" key is pressed while the popup window is in focus
        #     self.camera_index += 1 #try the next camera index
        #     self.capture = cv.VideoCapture(0)
        #     if not self.capture: #if the next camera index didn't work, reset to 0.
        #         self.camera_index = 0
        #         self.capture = cv.VideoCapture(0)
        jpegImg = Image.fromstring("RGB",cv.GetSize(self.frame),self.frame.tostring())
        retStr = jpegImg.tostring("jpeg","RGB")
        print("Compressed Size = ",len(retStr))
        return retStr

        #jpeg.compress(self.frame,640,480,8)

    def set_frame(self, frame):
#im image("RGB",(640,480))
        jpegPIL = Image.fromstring("RGB",(640,480),frame,"jpeg","RGB","raw")
        cv_im = cv.CreateImage((640,480), cv.IPL_DEPTH_8U, 3)
        cv.SetData(cv_im,jpegPIL.tostring())
        cv.ShowImage(self.name, cv_im)
if __name__=="__main__":
    vf = VideoFeed(1,"test",1)
    while 1:
        m = vf.get_frame()
        vf.set_frame(m)


# def display():
#     cap = cv.VideoCapture(0)
#
#     while True:
#         ret, frame = cap.read()
#         cv.imshow('Live Web-Cam Feed', frame)
#
#         key = cv.waitKey(1)
#         if key in [27, 81, 113]:
#             break
#
#     cap.release()
#     cv.destroyAllWindows()
#
#
# if __name__=='__main__':
#     display()
