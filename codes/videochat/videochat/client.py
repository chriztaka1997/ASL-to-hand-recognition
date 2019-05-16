#!/usr/bin/python
import socket, videosocket
from videofeed import VideoFeed
# from multiprocessing import Process, Queue  
import threading
import time
import cv2 as cv
import sys

class Client:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create socket object
        try:
            self.client_socket.connect(("127.0.0.1", 5000))#local machine address
            # self.client_socket.connect(("192.168.43.41", 5000))#chris's address address
        except  socket.error, exc: #catch socket exception
            print("Caught exception socket.error: %s" % exc)
            sys.exit()

        print("Connected to server\n")
    
        self.vsock = videosocket.videosocket (self.client_socket) #create videosocket object
       
        self.videofeed = VideoFeed("client",1) #create videofeed object

    def display_video(self): #multiprocessing/threading
        while(True):
            frame = self.vsock.vreceive() #receive frame data from socket
            newFrame = self.videofeed.set_frame(frame) #unmarshall frame data

            cv.imshow('Client 1', newFrame) #display frame on window
            key = cv.waitKey(1)

            if key in [27,81,113]: #quit when q/esc is pressed
                print("Exiting program. . . .")
                cv.destroyAllWindows()
                # sys.exit()
                break

    def vidSend(self): #multiprocessing
        while(True):
            frame = self.videofeed.get_frame() #capture frame
            self.vsock.vsend(frame) #send frame

    def connect(self):
        # p1 = Process(target = self.display_video)
        # p2 = Process(target = self.vidSend)
        p1 = threading.Thread(target = self.display_video)
        p2 = threading.Thread(target = self.vidSend)

        p1.start()
        p2.start()

        p1.join()
        # print("waiting for second")
        sys.exit()
        # p2.join()
        # print("second exited")



if __name__ == "__main__":
    client = Client()
    client.connect()
