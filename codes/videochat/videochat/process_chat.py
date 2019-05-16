from multiprocessing import Process
import cv2 as cv

def display(num):
    # if(cv.VideoCapture().isOpened()==False):
    #     print("false")
    #     name = "Web Cam " + str(num)
    #     cap = cv.VideoCapture(num)
    # else:
    #     print("error accessing camera")

    # if(cv.VideoCapture().isOpened() == False):
    if(num == 0):
        print("opening laptop webcam")
        name = "Web Cam " + str(num)
        # cap = cv.VideoCapture(num)
        cap = cv.VideoCapture(0)
        if(cap.isOpened() == False):
            print("Error accessing laptop webcam")
        else:
            print("Successfully opened laptop webcam")
    else:
        print("Opening external webcam")
        name = "Web Cam " + str(num)
        cap = cv.VideoCapture(1)
        if(cap.isOpened() == False):
            print("Error accessing external webcam")
        else:
            print("Successfully opened external webcam")

    while True:
        ret, frame = cap.read()
        # cv.imshow('Live Web-Cam Feed', frame)
        cv.imshow(name, frame)
        key = cv.waitKey(1)
        if key in [27, 81, 113]:
            break

    cap.release()
    cv.destroyAllWindows()

# cameraCount = 0 #global variable

if __name__=='__main__':
    #create threads
    p1 = Process(target = display, args = (0,))
    p2 = Process(target = display, args = (1,))

    #start process 1
    p1.start()
    #start process 2
    p2.start()

    #wait until process 1 is completely executed
    p1.join()
    #wait until process 2 is completely executed
    p2.join()

    print('Done')
