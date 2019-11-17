<h1 id="conference" align="center">ConferenceSystem</h1>

<p align="center">
    <a href="https://www.python.org/">
        <img src="https://img.shields.io/badge/python-3.5%20%7C%203.6%20%7C%203.7-blue" alt="Pyhton 3">
    </a>
    <a href="http://www.apache.org/licenses/">
        <img src="https://img.shields.io/badge/license-Apache-blue" alt="GitHub">
    </a>
    <a href="#">
        <img src="https://img.shields.io/static/v1.svg?label=Contributions&message=Welcome&color=0059b3&style=flat-square" alt="welcome">
    </a>
</p>

<p align="center">
    <a href="#clipboard-getting-started">Getting Started</a> •
    <a href="#table-of-contents">Table of Contents</a> •
    <a href="#about">About</a> •
    <a href="#acknowledgment">Acknowledgment</a> •
    <a href="#speech_balloon-faq">FAQ</a> •
</p>

<h6 align="center">Made by Duan-JM  • :milky_way: 
<a href="https://Duan-JM.github.io/">https://Duan-JM.github.io/</a>
</h6>
<h6 align="center">Made by ximing Xing • :milky_way: 
<a href="https://ximingxing.github.io/">https://ximingxing.github.io/</a>
</h6>

<h6 align="center">Available Service List</h6>

-  Lecture Video Generator (WIP)
    * 自动生成演讲者演讲视频
    * Relavent Service Link [here](link).

-  Take a selfie
    * 大声喊 "Cheeeeers" 就能自动使用会议室摄像头进行合影
    * Relavent Service Link [here](link).

-  Who are they
    * 只需要给系统发信息，便可自动生成当前会议室内的参会人员信息
    * Relavent Service Link [here](link).

Open Source runs on love, laughter and a whole lot of coffee. Consider buying me one if you find this content useful ☕️😉.

<h2 align="center">:clipboard: Getting Started</h2>

- 安装v4l2capture for input mudule
  * sudo apt-get install libv4l-dev
  * git clone https://github.com/cgpeter96/python-v4l2capture.git
  * cd python-v4l2capture
  * python3 setup.py build
  * sudo python3 setup.py install

- 安装opencv
  * pip3 install opencv-python

- 安装ffmpeg

  * 需要添加ffmpeg到“环境变量”，ffmpeg下载地址可以[点击这里](https://ffmpeg.zeranoe.com/builds/)。（下载static包解压即可）

<h2 align="center">Table of Contents</h2>
<p align="right"><a href="#conference"><sup>▴ Back to top</sup></a></p>

- Directory 

└── jarvis
    ├── README.md
    ├── module
    │   ├── action.py
    │   ├── archieve
    │   │   ├── audio_collector
    │   │   │   └── README.md
    │   │   ├── merge
    │   │   │   ├── configuration.txt
    │   │   │   ├── merge.py
    │   │   │   └── README.md
    │   │   ├── split_video
    │   │   │   ├── example_config.txt
    │   │   │   ├── process_video.py
    │   │   │   └── README.md
    │   │   └── video_collector
    │   │       ├── capture_video.py
    │   │       ├── combine_images2video.py
    │   │       └── README.md
    │   ├── configs
    │   │   └── detectron2
    │   │       ├── Base-RCNN-C4.yaml
    │   │       ├── Base-RCNN-DilatedC5.yaml
    │   │       ├── Base-RCNN-FPN.yaml
    │   │       ├── Base-RetinaNet.yaml
    │   │       ├── Cityscapes
    │   │       ├── COCO-Detection
    │   │       ├── COCO-InstanceSegmentation
    │   │       ├── COCO-Keypoints
    │   │       ├── COCO-PanopticSegmentation
    │   │       ├── Detectron1-Comparisons
    │   │       ├── LVIS-InstanceSegmentation
    │   │       ├── Misc
    │   │       ├── PascalVOC-Detection
    │   │       └── quick_schedules
    │   ├── __init__.py
    │   ├── input.py
    │   ├── process.py
    │   ├── README.md
    │   └── utils.py
    └── service
        └── lecture_generate_service.py


<h2 align="center">About</h2>

## Who are we?
一群对生活有热情，想要用所学的知识做些什么的小伙伴。

<h2 align="center">Acknowledgment</h2>
<p align="right"><a href="#conference"><sup>▴ Back to top</sup></a></p>

We want to thanks :

- ffmpeg

  ffmpeg version 3.4.6-0ubuntu0.18.04.1 Copyright (c) 2000-2019 the FFmpeg developers built with gcc 7 (Ubuntu 7.3.0-16ubuntu3)

- opencv
<h2 align="center">:speech_balloon: FAQ</h2>
<p align="right"><a href="#conference"><sup>▴ Back to top</sup></a></p>
