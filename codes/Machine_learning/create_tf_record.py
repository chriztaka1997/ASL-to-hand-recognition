import re
import hashlib
import io
import json
import os
import csv
from PIL import Image
import numpy as np
import cv2
import json
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

import tensorflow as tf

from object_detection.utils import dataset_util
#from utils import label_map_util

flags = tf.app.flags
tf.flags.DEFINE_string('output_dir', '', 'Output data directory.')

FLAGS = flags.FLAGS

tf.logging.set_verbosity(tf.logging.INFO)


def write_tf_record_from_dataset_detection(type, record_file):

    writer = tf.python_io.TFRecordWriter(record_file)
    cut_margin = 20
    paths = {'test': './manual_test',
             'train': './GenerateB'}
    inpath = paths[type]

    # all .json files in inpath dir
    files = sorted([f for f in os.listdir(inpath) if f.endswith('.json')])

    for i, f in enumerate(files):
        #print (str(i) + " ",f )
        xmins = []
        xmaxs = []
        ymins = []
        ymaxs = []
        classes = [1,1]
        image_format = b'jpg'
        with open(os.path.join(inpath, f), 'r') as fid:
            pst = []
            dat = json.load(fid)

            keypoints_right = np.array(dat[0]['human_annotations']['right_hand'])
            dat[0]['human_annotations']['right_hand'] = keypoints_right.tolist()

            keypoints_left = np.array(dat[0]['human_annotations']['left_hand'])
            dat[0]['human_annotations']['left_hand'] = keypoints_left.tolist()


            
            file_path = os.path.join(inpath, f[2:-5]+ '.jpg')
            with tf.gfile.GFile(file_path, 'rb') as fid:
                encoded_jpg = fid.read()
            encoded_jpg_io = io.BytesIO(encoded_jpg)
            image = Image.open(encoded_jpg_io)
            width, height = image.size

            xmins.append(keypoints_left[0]*1.0/width)
            xmins.append(keypoints_right[0]*1.0/width)

            ymins.append(keypoints_left[1]*1.0/height)
            ymins.append(keypoints_right[1]*1.0/height)

            xmaxs.append(keypoints_left[2]*1.0/width)
            xmaxs.append(keypoints_right[2]*1.0/width)

            ymaxs.append(keypoints_left[3]*1.0/height)
            ymaxs.append(keypoints_right[3]*1.0/height)

        feature_dict = {
            'image/height': dataset_util.int64_feature(height),
            'image/width': dataset_util.int64_feature(width),
            'image/filename': dataset_util.bytes_feature(f.encode('utf-8')),
            'image/source_id': dataset_util.bytes_feature(f.encode('utf-8')),
            'image/encoded': dataset_util.bytes_feature(encoded_jpg),
            'image/format': dataset_util.bytes_feature(image_format),
            'image/object/bbox/xmin': dataset_util.float_list_feature(xmins),
            'image/object/bbox/xmax': dataset_util.float_list_feature(xmaxs),
            'image/object/bbox/ymin': dataset_util.float_list_feature(ymins),
            'image/object/bbox/ymax': dataset_util.float_list_feature(ymaxs),
            'image/object/class/label': dataset_util.int64_list_feature(classes),
        }

        print("save tf.train.Exampe almost {:.2f}%".format(i * 100 / len(files)))
        example = tf.train.Example(features=tf.train.Features(feature=feature_dict))
        writer.write(example.SerializeToString())
    writer.close()
    print("write success")

# for test
def read_dataset(imgs, labels):
    cut_margin = 15
    paths = {'test': 'manual_test',
             'train': 'manual_train'}
    inpath = paths['train']

    # all .json files in inpath dir
    files = sorted([f for f in os.listdir(inpath) if f.endswith('.json')])

    for f in files:
        with open(os.path.join(inpath, f), 'r') as fid:
            pst = []
            height = width = 0
            dat = json.load(fid)
            keypoints = np.array(dat['hand_pts'])
            invalid = keypoints[:, 2] != 1
            is_left = dat['is_left']
            dat['hand_pts'] = keypoints.tolist()
            im = cv2.imread(os.path.join(inpath, f[0:-5] + '.jpg'))
            height = im.shape[0]
            width = im.shape[1]

            for p in range(keypoints.shape[0]):
                if keypoints[p, 2] != 0:
                    tmp_point = (int(keypoints[p, 0]), int(keypoints[p, 1]))
                    cv2.circle(im, tmp_point, 2, (255, 255, 255))
                    pst.append(tmp_point)
            # convert list to np.array
            np_pst = np.array(pst)
            # find xmin ymin xmax ymax
            findex = 0
            max_x = max_y = min_x = min_y = 0
            for point in np_pst:
                if(len(point) == 2):
                    x = int(point[0])
                    y = int(point[1])

                    if(findex == 0):
                        min_x = x
                        min_y = y
                    findex += 1
                    max_x = x+cut_margin if (x+cut_margin > max_x) else max_x
                    min_x = x-cut_margin if (x-cut_margin < min_x) else min_x
                    max_y = y+cut_margin if (y+cut_margin > max_y) else max_y
                    min_y = y-cut_margin if (y-cut_margin < min_y) else min_y
            boxarray = []
            hold = {}
            hold['xmin'] = min_x
            hold['ymin'] = min_y
            hold['xmax'] = max_x
            hold['ymax'] = max_y
            if (min_x > 0 and min_y > 0 and max_x > 0 and max_y > 0):
                boxarray.append(hold)

            cv2.rectangle(im, (min_x, max_y), (max_x, min_y), (0, 255, 0), 1)

        cv2.imshow("test", im)
        cv2.waitKey(1000)

def main(_):

    if not tf.gfile.IsDirectory(FLAGS.output_dir):
        tf.gfile.MakeDirs(FLAGS.output_dir)

    # train set
    #write_tf_record_from_dataset_detection(type='train', record_file='./train.record')
    #read_dataset("a", "a")
    write_tf_record_from_dataset_detection(type='train', record_file='./train.record')
    # test set
    #write_tf_record_from_dataset_detection(type='test', record_file='./test.record')
if __name__ == '__main__':
   tf.app.run()

