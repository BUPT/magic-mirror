## Module Intrduction

## input.py

Input Module is used to receive data from hardware or somewhere else, the ouput of the module will be used in Process Module

* BaseInput
  BaseClass for all module in InputModule
* VideoRecord
  Record Video from the hardware.
* AudioRecord
  Record Video from the hardware.

## process.py

* BasicProcess
  BaseClass for all module in ProcessModule

* PeopleExistTimeProcess
  Using Detectron2 to detect people
  ```python
  >>> process = PeopleExistTimeProcess(
                detectron_config_path='./configs/detectron2/COCO-InstanceSegmentation/mask_rcnn_R_50_C4_1x.yaml',
                input_path='./video-save-file',
                pretrained='')
  ```

* VisualizationDetectron
  ```python
  Args:
      cfg (CfgNode):
      instance_mode (ColorMode):
      parallel (bool): whether to run the model in different processes from visualization.
      Useful since the visualization logic can be slow.
  ```

## action.py

Define the Actions, such as send emails, split video/audio, merge video/audio

* BaseAction
* PicToVideo
  combine picture batches to video
* SplitAction 
  Direct use ffmpeg command to sperate the video. The corresponding timestamp
  ```bash
  >>> process = SplitAction('./config', './input', './output')
  >>> process.start()
  ```

  Example config_file:
  ```bash
  system.mp4 | test.mp4 | 00:00:00 | 00:00:01
  system.mp3 | test.mp3 | 00:00:00 | 00:00:01
  ```
* MergeAction
  ```python
  m = MergeMediaAction(video_path1="./human.mp4",video_path2="./speech.mp4",audio_path="./audio.mp3", output_path="./output.mp4")
  m.process() following is the use of param.
  ```
  :param video_path1: human video's path
  :param cut_position: human video's cut position, the format is (width,height,x1,y1)
  :param cut_time_during: how long should the human video be cutted
  :param scale_size:the size to scale the human video
  :param video_path2: speech video's path
  :param merge_position: two video's merge position, position that we need to overlay (x1,y1)
  :param audio_name: audio name
  :param output_path: the final audio's output path
  :param use_configuration_file: whether to use configuration file 

## utils.py

## configs/
```bash
.
└── detectron2
    ├── Base-RCNN-C4.yaml
    ├── Base-RCNN-DilatedC5.yaml
    ├── Base-RCNN-FPN.yaml
    ├── Base-RetinaNet.yaml
    ├── Cityscapes
    ├── COCO-Detection
    ├── COCO-InstanceSegmentation
    ├── COCO-Keypoints
    ├── COCO-PanopticSegmentation
    ├── Detectron1-Comparisons
    ├── LVIS-InstanceSegmentation
    ├── Misc
    ├── PascalVOC-Detection
    └── quick_schedules
```

## legacy/

```bash
.
├── audio_collector
│   └── README.md
├── merge
│   ├── configuration.txt
│   ├── merge.py
│   └── README.md
├── split_video
│   ├── example_config.txt
│   ├── process_video.py
│   └── README.md
└── video_collector
    ├── capture_video_cv2.py
    ├── capture_video.py
    ├── combine_images2video.py
    └── README.md
```
