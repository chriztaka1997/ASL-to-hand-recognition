#!/usr/bin/python
import socket, videosocket
from videofeed import VideoFeed
# from multiprocessing import Process, Queue  
import threading
import time
import cv2 as cv
import sys

class Server:
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create socket object
        port = 5000
        self.server_socket.bind(("", port)) #bind socket to port
        self.server_socket.listen(0) #enable server to accept connections
        self.videofeed = VideoFeed("server",0) #create videofeed object

        print("Waiting for client on port: %d", port) #display port that the socket is listening on

        client_socket, address = self.server_socket.accept() 

        print("I got a connection from ", address) #display ip address of connected client

        self.vsock = videosocket.videosocket(client_socket) #create videosocket object

        self.p1 = threading.Thread(target = self.display_video)
        self.p2 = threading.Thread(target = self.vidSend)

        # self.p1.p1Alive = True

    def display_video(self): #multiprocessing/threading
        while(True):
            frame= self.vsock.vreceive() #receive frame data through socket

            setFrame = self.videofeed.set_frame(frame) #unmarshal frame data

            cv.imshow('Server', setFrame) #display on window 

            key = cv.waitKey(1)
            if key in [27,81,113]: #quit when q/esc is pressed
                print("Exiting program. . . .")
                cv.destroyAllWindows()
                # self.p1Alive = False
                # sys.exit()
                break
            
    
    def vidSend(self): #multiprocessing
        while(True):   
            # if(self.p1.p1Alive):
                frame=self.videofeed.get_frame() #get frame from camera

                self.vsock.vsend(frame) #send frame data through socket
            # else:
            #     print("breaking")
            #     break


    def start(self):

        # p1 = Process(target = self.display_video) #receive
        # p2 = Process(target = self.vidSend) #send
        # p1 = threading.Thread(target = self.display_video)
        # p2 = threading.Thread(target = self.vidSend)

        self.p1.start()
        self.p2.start()

        self.p1.join()
        self.p2.join()
        sys.exit()
        # p2.join()
        # print("second exited")
        
            


if __name__ == "__main__":
    server = Server()
    server.start()
