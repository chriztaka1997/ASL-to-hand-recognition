#!/bin/bash
python3 ./export_inference_graph.py \
--input_type=image_tensor \
--pipeline_config_path=./data/ssd_mobilenet_v2_coco.config \
--trained_checkpoint_prefix=./data/train/model.ckpt-10527 \
--output_directory=./data/train/export
