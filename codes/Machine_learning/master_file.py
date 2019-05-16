import os
import glob
import cv2
import csv
import json
import numpy as np
from frame_by_frame_opencv import masking
import random

def nothing(x):
    pass


#prepare the for the main function
def getpos(event, x, y, flags, param):
    global left_right_lower, left_left_upper
    global right_right_lower, right_left_upper
    global flag
    if event == cv2.EVENT_LBUTTONDOWN and flag == 0:
        left_left_upper=[x, y]
        flag = 1
    if event == cv2.EVENT_LBUTTONUP:
        left_right_lower = [x, y]
        flag = 0

    if event == cv2.EVENT_RBUTTONDOWN and flag == 0:
        right_left_upper=[x, y]
        flag = 2
    if event == cv2.EVENT_RBUTTONUP:
        right_right_lower = [x, y]
        flag = 0

    if event == cv2.EVENT_MOUSEMOVE and flag > 0:
        if flag == 1:
            left_right_lower = [x, y]
        elif flag == 2:
            right_right_lower = [x, y]


#create a dataset with a new background
def getBg(maskDir, colorDir, bgDir, bgName, file_name):
    bright = cv2.getTrackbarPos('bright', 'gen')
    contrast = cv2.getTrackbarPos('contrast', 'gen')

    maskPath = os.path.join(maskDir, file_name)
    mask = cv2.imread(maskPath)
    png = np.zeros((mask.shape[0], mask.shape[1], 4))
    png[:, :, 3] = mask[:, :, 0]

    # [raw] is raw image with hand
    colorPath = os.path.join(colorDir, file_name)
    raw = cv2.imread(colorPath)
    png[:, :, 0] = raw[:, :, 0]
    png[:, :, 1] = raw[:, :, 1]
    png[:, :, 2] = raw[:, :, 2]
    #png = (bright * 0.01) * png + contrast

    # [bg]: is backgound picture
    bgPath = bgDir + bgName
    bg = cv2.imread(bgPath)
    bg = cv2.resize(bg, (png.shape[1], png.shape[0]))

    mean_png = np.sum(png) / (png.shape[0] * png.shape[1] * png.shape[2])
    mean_bg = np.sum(bg) / (bg.shape[0] * bg.shape[1] * bg.shape[2])
    alph = (mean_bg / mean_png) * (bright * 0.01)
    alpha = alph if alph < 1.0 else 1

    '''
    #b = b1 * a1/255 + b0 * (255 - a1)/255
    #g = g1 * a1/255 + g0 * (255 - a1)/255
    #r = r1 * a1/255 + r0 * (255 - a1)/255
    '''
    png[:, :, 0:3] = png[:, :, 0:3] * alpha + contrast * alpha
    bg[:, :, 0:3] = bg[:, :, 0:3] * alpha + contrast * alpha
    bg[:, :, 0] = png[:, :, 0] * png[:, :, 3] / 255 + bg[:, :, 0] * (255 - png[:, :, 3]) / 255
    bg[:, :, 1] = png[:, :, 1] * png[:, :, 3] / 255 + bg[:, :, 1] * (255 - png[:, :, 3]) / 255
    bg[:, :, 2] = png[:, :, 2] * png[:, :, 3] / 255 + bg[:, :, 2] * (255 - png[:, :, 3]) / 255

    return bg





#######
# Creating the dataset
def create_dataset(colorDir,maskDir,bgDir,dataDir):


    #color = [file for file in os.listdir("/Users/wg/Desktop/hands/Hand1Edit_frame/color")]
    #mask = [file for file in os.listdir("/Users/wg/Desktop/hands/Hand1Edit_frame/color")]

    cv2.namedWindow('gen')
    cv2.setMouseCallback("gen", getpos)

    #list of all the background picture
    bgName = os.listdir(bgDir)
    bgName.sort()

    #list of all the images in color directory
    items = os.listdir(colorDir)
    items.sort()

    data =[]

    for file_name in items:
        loop = True
        global left_right_lower, left_left_upper
        global right_right_lower, right_left_upper
        left_left_upper = [0, 0]
        left_right_lower = [0, 0]
        right_left_upper = [0, 0]
        right_right_lower = [0, 0]
        while (loop):
            global set_flag

            bg = getBg(maskDir, colorDir,bgDir,bgName[0], file_name)

            vis = bg

            cv2.rectangle(vis, tuple(left_left_upper), tuple(left_right_lower), (255,0,0), 1)
            cv2.rectangle(vis, tuple(right_left_upper), tuple(right_right_lower), (255, 0, 0), 1)

            cv2.imshow("gen", vis)

            c = cv2.waitKey(30)
            #110 is the numerical value of n
            if c == 110:
                bg_random= []
                for i in range(15):
                    bg_random.append(random.choice(bgName))

                for bg_name in bg_random:
                    data =[]
                    json_name = dataDir+"/d_"+str(bg_name[0:2])+"_"+str(file_name[5:10])+".json"
                    # img_name = "d_" + str(bg_name[0:2]) + "_" + str(file_name[5:10]) + ".png"
                    # bg1 = getBg(maskDir, colorDir, bgDir, bg_name, file_name)
                    # img_full_path = os.path.join(dataDir, img_name)
                    # cv2.imwrite(img_full_path, bg1)

                    with open(json_name, "w")as f:
                        #json
                        #the naming of the dataset is d_##_*****
                        # ##is the background used
                        # *****is the frame of hand that is being used
                        img_name = "d_"+str(bg_name[0:2])+"_"+str(file_name[5:10])+".png"
                        left_center = [(left_left_upper[0] + left_right_lower[0])/2,
                                       (left_left_upper[1] + left_right_lower[1])/2 ]
                        right_center = [(right_left_upper[0] + right_right_lower[0])/2,
                                        (right_left_upper[1] + right_right_lower[1])/2 ]
                        data.append({"image_id": img_name,"human_annotations": { "left_hand": [left_left_upper[0],left_left_upper[1],
                                left_right_lower[0],left_right_lower[1]], "right_hand":[right_left_upper[0],right_left_upper[1],
                                right_right_lower[0],right_right_lower[1]]}, "keypoint":{"left_center": [left_center[0],
                                left_center[1] ,1],"right_center":[right_center[0],right_center[1],1]}})
                        #generate the picture with bg
                        bg1 = getBg(maskDir,colorDir,bgDir,bg_name,file_name)
                        img_full_path = os.path.join(dataDir,img_name)
                        cv2.imwrite(img_full_path, bg1)
                        f.write(json.dumps(data))

                print("next")
                loop = False

    cv2.destroyAllWindows()

    # Creating the dataset
def create_dataset_using_csv(colorDir,maskDir,bgDir,dataDir):


    #color = [file for file in os.listdir("/Users/wg/Desktop/hands/Hand1Edit_frame/color")]
    #mask = [file for file in os.listdir("/Users/wg/Desktop/hands/Hand1Edit_frame/color")]

    cv2.namedWindow('gen')
    cv2.setMouseCallback("gen", getpos)

    #list of all the background picture
    print(os.listdir(bgDir))
    bgName = os.listdir(bgDir)
    bgName.sort()

    #list of all the images in color directory
    items = os.listdir(dataDir)
    items.sort()

    data =[]

    for file_name in items:
        loop = True
        global left_right_lower, left_left_upper
        global right_right_lower, right_left_upper
        left_left_upper = [0, 0]
        left_right_lower = [0, 0]
        right_left_upper = [0, 0]
        right_right_lower = [0, 0]
        while (loop):
            global set_flag

            #bg = getBg(maskDir, colorDir,bgDir,bgName[0], file_name)

            vis = cv2.imread( os.path.join(dataDir,file_name))

            cv2.rectangle(vis, tuple(left_left_upper), tuple(left_right_lower), (255,0,0), 1)
            cv2.rectangle(vis, tuple(right_left_upper), tuple(right_right_lower), (255, 0, 0), 1)

            cv2.imshow("gen", vis)

            c = cv2.waitKey(30)
            #110 is the numerical value of n
            if c == 110:
                # bg_random= []
                # for i in range(15):
                #     bg_random.append(random.choice(bgName))
                #
                # for bg_name in bg_random:
                #     data =[]
                json_name = dataDir+"/d_"+str(file_name[:-4])+".json"
                # img_name = "d_" + str(bg_name[0:2]) + "_" + str(file_name[5:10]) + ".png"
                # bg1 = getBg(maskDir, colorDir, bgDir, bg_name, file_name)
                # img_full_path = os.path.join(dataDir, img_name)
                # cv2.imwrite(img_full_path, bg1)

                with open(json_name, "w")as f:
                    #json
                    #the naming of the dataset is d_##_***
                    # ##is the background used
                    # *****is the frame of hand that is being used
                    img_name = "d_"+str(file_name)+".png"
                    left_center = [(left_left_upper[0] + left_right_lower[0])/2,
                                   (left_left_upper[1] + left_right_lower[1])/2 ]
                    right_center = [(right_left_upper[0] + right_right_lower[0])/2,
                                    (right_left_upper[1] + right_right_lower[1])/2 ]
                    data.append({"image_id": img_name,"human_annotations": { "left_hand": [left_left_upper[0],left_left_upper[1],
                            left_right_lower[0],left_right_lower[1]], "right_hand":[right_left_upper[0],right_left_upper[1],
                            right_right_lower[0],right_right_lower[1]]}, "keypoint":{"left_center": [left_center[0],
                            left_center[1] ,1],"right_center":[right_center[0],right_center[1],1]}})
                    #generate the picture with bg
                    #bg1 = getBg(maskDir,colorDir,bgDir,bg_name,file_name)
                    img_full_path = os.path.join(dataDir,img_name)
                    # cv2.imwrite(img_full_path, bg1)
                    f.write(json.dumps(data))
                print("next")
                loop = False

    cv2.destroyAllWindows()

def process_order(colorDir,maskDir,bgDir,dataDir,videoPath):
    # Masking from the video
    # turn the video into pictures

    #video_path = "./hand.mov"
    #masking(videoPath,colorDir,maskDir)

    bright = 100
    contrast = 0
    cv2.namedWindow('gen')

    cv2.createTrackbar('bright', 'gen', 0, 100, nothing)
    cv2.setTrackbarPos('bright', 'gen', bright)

    cv2.createTrackbar('contrast', 'gen', 0, 100, nothing)
    cv2.setTrackbarPos('contrast', 'gen', contrast)
    create_dataset(colorDir,maskDir,bgDir,dataDir)

# main
if __name__ == '__main__':
    flag = 0
    left_left_upper = [-100,-100]
    left_right_lower = [-100,-100]
    right_left_upper = [-100,-100]
    right_right_lower = [-100,-100]



    #Directory for the images
    colorDir = "./color/"
    maskDir = "./mask/"
    bgDir = "./Background/"
    dataDir = "./dataset"

    videoPath = "./videos/random"

    process_order(colorDir,maskDir,bgDir,dataDir,videoPath)