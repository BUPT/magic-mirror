"""
File: process.py
Author: Duan-JM
Email: vincent.duan95@outlook.com
Github: https://github.com/Duan-JM
Description:
    The module here is used the AI/none methods to process the data
    then give the actions' params
"""
import os
import math
import time
import multiprocessing as mp

import torch
from detectron2.config import get_cfg
from detectron2.data import MetadataCatalog
from detectron2.data.detection_utils import read_image
from detectron2.engine.defaults import DefaultPredictor
from detectron2.utils.visualizer import ColorMode, Visualizer


class BasicProcess:
    """
    BaseClass for all module in ProcessModule
    """
    def set_device(self, data_source_device):
        """
        Point out which hardware to ouput

        [optional]
        """
        pass

    def take_action(self):
        """
        params: params: the params for the actions

        return: flag(boolen): check if action have done properly
        """
        raise NotImplementedError


class PeopleExistTimeProcess(BasicProcess):
    """
    Using Detectron2 to detect people
    """
    def __init__(self, detectron_config_path, input_path, pretrained, confidence_threshold, save_path=None):
        """
        params: detectron_config_path(string): config file for the detectron
        params: input_path(string): the dir of the images which you want to segement
        params: pretrained(string): a path to the official pretrained model path
        params: confidence_threshold(int):
        params: save_path(string):

        >>> process = PeopleExistTimeProcess(
                detectron_config_path='./configs/detectron2/COCO-InstanceSegmentation/mask_rcnn_R_50_C4_1x.yaml',
                input_path='./video-save-file',
                pretrained='')
        """
        self.detectron_config_path = detectron_config_path
        self.input_path = input_path
        self.pretrained = pretrained
        self.confidence_threshold = confidence_threshold
        self.save_path = save_path


    def _setup_cfg(self):
        # load config from file and command-line arguments
        cfg = get_cfg()
        cfg.merge_from_file(self.detectron_config_path)
        cfg.merge_from_list(['MODEL.WEIGHTS', self.pretrained])
        # Set score_threshold for builtin models
        cfg.MODEL.RETINANET.SCORE_THRESH_TEST = self.confidence_threshold
        cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = self.confidence_threshold
        cfg.MODEL.PANOPTIC_FPN.COMBINE.INSTANCES_CONFIDENCE_THRESH = self.confidence_threshold
        cfg.freeze()
        return cfg


    def _parse_input_file(self):
        ''' parse input file
        return image_path_list: list, list of image path
        return timestamp_list: list, list of timestamp
        '''
        image_path_list = list()
        timestamp_list = list()

        if not os.path.exists(self.input_path):
            raise ValueError("input_file_path dose not exist")

        with open(os.path.join(self.input_path, "timelog/timestamp.log"), 'r') as f:
            # TODO: Maybe add auto read all file under the dir are better, NEED
            lines = f.readlines()
            for line in lines:
                img_name, timestamp = str(line.strip()).split(":")
                image_path_list.append(os.path.join(self.input_path, img_name))
                timestamp_list.append(timestamp)

        return image_path_list, timestamp_list


    def _find_person(self, predictions, thing_classes):
        """
        Find if person are in the image
        """
        for pred_class in predictions['instances'].pred_classes:
            if thing_classes[pred_class] == 'person':
                # TODO can add ratio of person in the whole image
                return True
        return False


    def take_action(self):
        # ====> init base config
        mp.set_start_method("spawn", force=True)
        cfg = self._setup_cfg()
        detectron = VisualizationDetectron(cfg)

        # ===> image_path and timestamp
        image_path_list, timestamp_list = self._parse_input_file()

        # ===> detect for each image in path
        tmp_timestamp = None
        flag = False
        start_time = list()
        stop_time = list()
        for index, path in enumerate(image_path_list):
            # use PIL, to be consistent with evaluation
            img = read_image(path, format="BGR")
            predictions, visualized_output = detectron.run_on_image(img)
            current_time = math.floor(float(timestamp_list[index]))
            current_time = time.strftime("%H:%M:%S", time.gmtime(float(current_time)))

            if tmp_timestamp is None:
                tmp_timestamp = current_time

            if self._find_person(predictions, detectron.metadata.thing_classes):
                # ====> output to the file
                if (tmp_timestamp != current_time) and not flag:
                    tmp_timestamp = current_time
                    flag = True
                    start_time.append(current_time)
            else:
                if (tmp_timestamp != current_time) and flag:
                    tmp_timestamp = current_time
                    flag = False
                    stop_time.append(current_time)

            if self.save_path:
                if os.path.isdir(self.save_path):
                    assert os.path.isdir(self.save_path), self.save_path
                    out_filename = os.path.join(self.save_path, os.path.basename(path))
                else:
                    assert len(self.input_path) == 1, "Please specify a directory with args.output"
                    out_filename = self.save_path
                visualized_output.save(out_filename)
            else:
                Exception("you should input output place")
        print(start_time, stop_time)


class VisualizationDetectron(object):
    def __init__(self, cfg, instance_mode=ColorMode.IMAGE):
        """
        Args:
            cfg (CfgNode):
            instance_mode (ColorMode):
            parallel (bool): whether to run the model in different processes from visualization.
                Useful since the visualization logic can be slow.
        """
        self.metadata = MetadataCatalog.get(cfg.DATASETS.TEST[0])
        self.cpu_device = torch.device("cpu")
        self.instance_mode = instance_mode
        self.predictor = DefaultPredictor(cfg)

    def run_on_image(self, image):
        """
        Args:
            image (np.ndarray): an image of shape (H, W, C) (in BGR order).
                This is the format used by OpenCV.

        Returns:
            predictions (dict): the output of the model.
            vis_output (VisImage): the visualized image output.
        """
        vis_output = None
        predictions = self.predictor(image)
        # Convert image from OpenCV BGR format to Matplotlib RGB format.
        image = image[:, :, ::-1]
        visualizer = Visualizer(image, self.metadata, instance_mode=self.instance_mode)
        if "panoptic_seg" in predictions:
            panoptic_seg, segments_info = predictions["panoptic_seg"]
            vis_output = visualizer.draw_panoptic_seg_predictions(
                panoptic_seg.to(self.cpu_device), segments_info
            )
        else:
            if "sem_seg" in predictions:
                vis_output = visualizer.draw_sem_seg(
                    predictions["sem_seg"].argmax(dim=0).to(self.cpu_device)
                )
            if "instances" in predictions:
                instances = predictions["instances"].to(self.cpu_device)
                vis_output = visualizer.draw_instance_predictions(predictions=instances)

        return predictions, vis_output

if __name__ == "__main__":
    action = PeopleExistTimeProcess(
        detectron_config_path='./configs/detectron2/COCO-InstanceSegmentation/mask_rcnn_R_50_C4_1x.yaml',
        input_path='/home/deamov/sambashare/Transfer/data/',
        pretrained='detectron2://COCO-InstanceSegmentation/mask_rcnn_R_50_C4_1x/137259246/model_final_9243eb.pkl',
        confidence_threshold=0.5,
        save_path='./test'
    )
    action.take_action()
