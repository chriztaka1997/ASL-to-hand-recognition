import cv2
import os
import numpy as np

# global variable
set_flag = True
video_path = "Dataset/Videos"
background_path = "Dataset/Background"
generate_path = "Dataset/Generate_B"


# callback function
def getpos(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        pass


def bar_update(pos):
    global set_flag
    set_flag = True


# windows init
def init_windows(hsv_l, hsv_h):

    cv2.namedWindow('gen')
    cv2.setMouseCallback("gen", getpos)

    cv2.createTrackbar('H_low', 'gen', 0, 255, bar_update)
    cv2.setTrackbarPos('H_low', 'gen', hsv_l[0])

    cv2.createTrackbar('H_high', 'gen', 0, 255, bar_update)
    cv2.setTrackbarPos('H_high', 'gen', hsv_h[0])

    cv2.createTrackbar('S_low', 'gen', 0, 255, bar_update)
    cv2.setTrackbarPos('S_low', 'gen', hsv_l[1])

    cv2.createTrackbar('S_high', 'gen', 0, 255, bar_update)
    cv2.setTrackbarPos('S_high', 'gen', hsv_h[1])

    cv2.createTrackbar('V_low', 'gen', 0, 255, bar_update)
    cv2.setTrackbarPos('V_low', 'gen', hsv_l[2])

    cv2.createTrackbar('V_high', 'gen', 0, 255, bar_update)
    cv2.setTrackbarPos('V_high', 'gen', hsv_h[2])

    cv2.createTrackbar('bright', 'gen', 0, 100, bar_update)
    cv2.setTrackbarPos('bright', 'gen', bright)

    cv2.createTrackbar('contrast', 'gen', 0, 100, bar_update)
    cv2.setTrackbarPos('contrast', 'gen', contrast)


def get_hand_png(rgb, hsv_high, hsv_low):
    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)
    lower = np.array([hsv_low[0], hsv_low[1], hsv_low[2]])
    upper = np.array([hsv_high[0], hsv_high[1], hsv_high[2]])
    mask = cv2.inRange(hsv, lower, upper)
    _, msk_inv = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY_INV)
    png = np.zeros((msk_inv.shape[0], msk_inv.shape[1], 4))
    png[:, :, 0] = rgb[:, :, 0]
    png[:, :, 1] = rgb[:, :, 1]
    png[:, :, 2] = rgb[:, :, 2]
    png[:, :, 3] = msk_inv[:, :]
    return png


def generate(png, bright, contrast, frame, write=False):
    all = []
    files = os.listdir(background_path)
    for file in files:
        if not file.endswith('.jpg'):
            files.remove(file)

    for idx, file in enumerate(files):
        bg = cv2.imread(os.path.join(background_path, file))
        bg = cv2.resize(bg, (png.shape[1], png.shape[0]))
        mean_png = np.sum(png) / (png.shape[0]*png.shape[1]*png.shape[2])
        mean_bg = np.sum(bg) / (bg.shape[0]*bg.shape[1]*bg.shape[2])
        alph = (mean_bg/mean_png) * (bright*0.01)
        alph = alph if alph < 1.0 else 1

        mix = bg
        '''
        b = b1 * a1/255 + b0 * (255 - a1)/255
        g = g1 * a1/255 + g0 * (255 - a1)/255
        r = r1 * a1/255 + r0 * (255 - a1)/255
        '''
        png[:, :, 0:3] = png[:, :, 0:3]*alph + contrast*alph
        mix[:, :, 0] = png[:, :, 0] * png[:, :, 3] / 255 + bg[:, :, 0] * (255 - png[:, :, 3]) / 255
        mix[:, :, 1] = png[:, :, 1] * png[:, :, 3] / 255 + bg[:, :, 1] * (255 - png[:, :, 3]) / 255
        mix[:, :, 2] = png[:, :, 2] * png[:, :, 3] / 255 + bg[:, :, 2] * (255 - png[:, :, 3]) / 255
        all.append(mix)


        if write:
            cv2.imwrite(os.path.join(generate_path, "%08d_%03d.jpg" % (frame, idx)), mix)

    return all


def process_videos(video_path):

    cap = cv2.VideoCapture(video_path)
    frame = 0
    rand_bk = 0
    while 1:
        global set_flag
        ret, rgb = cap.read()
        if not ret:
            break
        frame += 1
        if set_flag:
            hsv_h[0] = cv2.getTrackbarPos('H_high', 'gen')
            hsv_h[1] = cv2.getTrackbarPos('S_high', 'gen')
            hsv_h[2] = cv2.getTrackbarPos('V_high', 'gen')

            hsv_l[0] = cv2.getTrackbarPos('H_low', 'gen')
            hsv_l[1] = cv2.getTrackbarPos('S_low', 'gen')
            hsv_l[2] = cv2.getTrackbarPos('V_low', 'gen')

            bright = cv2.getTrackbarPos('bright', 'gen')
            contrast = cv2.getTrackbarPos('contrast', 'gen')
            set_flag = False

        png_img = get_hand_png(rgb, hsv_h, hsv_l)
        mix = generate(png_img, bright, contrast, frame, True)

        stack = np.hstack([rgb, mix[rand_bk]])
        cv2.imshow("gen", stack)
        key = cv2.waitKey(30)
        if key == 113: #q press
            size = len(mix)
            rand_bk = np.random.randint(0, size)

    cap.release()
    cv2.destroyAllWindows()


# main
if __name__ == '__main__':

    hsv_h = [56, 255, 255]
    hsv_l = [24, 24, 24]

    bright = 100
    contrast = 0

    init_windows(hsv_l, hsv_h)

    video_files = os.listdir(video_path)
    for file in video_files:
        if not (file.endswith('.mov') or file.endswith('.mp4')):
            video_files.remove(file)

    for video in video_files:
        print(">>>>>>>>  video:", video)
        process_videos(os.path.join(video_path, video))