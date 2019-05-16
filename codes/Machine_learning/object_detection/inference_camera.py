import sys
import os
import time
import tensorflow as tf
import numpy as np
from PIL import Image
import cv2

from utils import label_map_util
from utils import visualization_utils as vis_util

NUM_CLASSES = 1
PATH_TO_CKPT = './data/train/export/frozen_inference_graph.pb'
PATH_TO_LABELS = './data/cmu_label_map.prototxt'
image_path = './test_data/'

TEST_IMAGE = []
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)

detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')

config = tf.ConfigProto()
config.gpu_options.allow_growth = True

files = os.listdir(image_path)
for item in files:
    TEST_IMAGE.append(os.path.join(image_path, item))

with detection_graph.as_default():
    with tf.Session(graph=detection_graph) as sess:
        for file in TEST_IMAGE:

            image_np = cv2.imread(file).astype(np.uint8)
            cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB, image_np)
            image_np = cv2.resize(image_np, (image_np.shape[1]//2, image_np.shape[0]//2))
            image_np_expanded = np.expand_dims(image_np, axis=0)

            image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
            boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
            scores = detection_graph.get_tensor_by_name('detection_scores:0')
            classes = detection_graph.get_tensor_by_name('detection_classes:0')
            num_detections = detection_graph.get_tensor_by_name('num_detections:0')
            start_time = time.time()

            print(time.ctime())
            (boxes, scores, classes, num_detections) = sess.run([boxes, scores, classes, num_detections],
                                                                feed_dict={image_tensor: image_np_expanded})
            print('{} elapsed time: {:.3f}s'.format(time.ctime(), time.time() - start_time))

            vis_util.visualize_boxes_and_labels_on_image_array(
                image_np, np.squeeze(boxes), np.squeeze(classes).astype(np.int32), np.squeeze(scores),
                category_index, use_normalized_coordinates=True, line_thickness=2)
            image_np = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
            cv2.imshow('test', image_np)
            cv2.waitKey()
