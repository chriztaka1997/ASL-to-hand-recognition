#!/bin/bash
python3 ./train.py \
--pipeline_config_path=./data/ssd_mobilenet_v2_coco.config \
--train_dir=./data/train
