"""
File: input.py
Author: Duan-JM
Email: vincent.duan95@outlook.com
Github: https://github.com/Duan-JM
Description:
    Input Module is used to receive data from hardware or somewhere else, the
    ouput of the module will be used in Process Module

    Install:
    >>> # 安装v4l2capture
    >>> sudo apt-get install libv4l-dev
    >>> git clone https://github.com/cgpeter96/python-v4l2capture.git
    >>> cd python-v4l2capture
    >>> python3 setup.py build
    >>> sudo python3 setup.py install

    >>> # 安装opencv
    >>> pip3 install opencv-python
"""
import os
import time
import select
import shutil
import logging

import numpy as np
import cv2 as cv
import v4l2capture

def create_dir(dpath):
    """
    create dirs
    """
    if os.path.exists(dpath):
        shutil.rmtree(dpath)
        os.mkdir(dpath)
    else:
        os.mkdir(dpath)

class BaseInput:
    """
    BaseClass for all module in InputModule
    """
    def set_device(self, data_source_device):
        """
        Point of the device number like `/dev/xxx`,
        check if the device is available, if true,
        set the device to the self.device
        """

    def raw_output(self, save_path):
        """
        Use the setted `self.device` to output the stream from the hardware

        params: save_path(string): where to save the data
        """
        raise NotImplementedError


class VideoRecord(BaseInput):
    """
    Record Video from the hardware.
    """
    def __init__(self, window_size, data_source_device, exposure_type=3, exposure_absolute=None):
        """
        params: exposure_type (int) : 3 auto, 1 manual
        params: exposure_absolute (int): manually set exposure
        params: window_size (tuple): (width, height)
        """
        super(VideoRecord, self).__init__()
        self.device = data_source_device
        self.exposure_type = exposure_type
        self.exposure_absolute = exposure_absolute
        self.window_size = window_size


    def _set_device(self):
        """
        Set the video source input device

        params: width(int)
        params: height(int)

        return: flag(boolen): check if device exist
        """
        if os.path.exists(self.device):
            video = cv.VideoCapture(self.device)
            video.set(3, self.window_size(0))
            video.set(4, self.window_size(1))
        else:
            raise ValueError(f"{self.device} you choose is not exists")
        return video


    def device_avalible(self):
        """
        Output all video availabe in current system
        """
        print(os.popen('ls /dev/video*').read())


    def raw_output(self, save_path=None, visual=False, multilog=False):
        """
        Output video, timelog and images to the save_path.

        params: save_path(string): choose which type to output, if None no savefiles
        params: visual(string): check whether open a window to display
        """
        video = self._set_device()
        video.create_buffers(2)
        video.queue_all_buffers()
        video.start()

        if visual:
            cv.namedWindow(f"video_device_{self.device}", cv.WINDOW_NORMAL)

        # ====> capture time
        start = time.time()
        cur_start = time.time()
        index = 0
        cur_index = 0
        error_count = 0
        while True:
            try:
                ret, frame = video.read()
                fname = f"video-save-file/{str(index)}.jpg"
                shape = frame.shape
                index += 1
                cur_index += 1

                if index % 300 == 0:
                    print('now capture:{} images'.format(index + 1))

                if save_path:
                    create_dir(f"{save_path}/video-save-file")
                    create_dir(f"{save_path}/timelog")

                    fp_count = 0
                    fp = open(f'{save_path}/timelog/timestamp-{fp_count}.log', 'w')

                    cv.imwrite(fname, frame)
                    fp.write('{}:{}\n'.format(fname, time.time() - start))
                    if multilog and index % 100 == 0:
                        fp.close()
                        fp_count += 1
                        fp = open(f'{save_path}/timelog/timestamp-{fp_count}.log', 'w')

                if visual:
                    cv.imshow(f'video_device_{self.device}', frame)

                if cur_index > 1000:
                    interval = time.time() - cur_start
                    now_fps = cur_index / interval
                    cur_start = time.time()
                    cur_index = 0
                    print(f'index:{index} device:{self.device}--->now fps:{now_fps}')

                # ====> use q to quit
                if cv.waitKey(10) & 0xff == ord('q'):
                    break

            except Exception as e:
                error_count += 1
                now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                logging.info('{}-->第{}帧报错:{}出错比:{}'.format(now_time, index, str(e), error_count / (index + 1)))
                print('出错继续下一帧')
            except KeyboardInterrupt:
                break
        fp.close()

        end = time.time()
        cost_time = end - start
        print(f'device:{self.device}--->final fps:{index/cost_time} cost-time:{cost_time}')
        if save_path:
            counts = len(os.listdir(f"{save_path}/video-save-file"))
            print(f"save {counts} images")

        video.close()
        if visual:
            cv.destroyAllWindows()


class AudioRecord(BaseInput):
    """
    Record Video from the hardware.

    Need have audio-recorder
    >>> sudo apt-get install audio-recorder
    """
    def __init__(self, card_num, device_num):
        """
        params: card_num(int): choose the number of the card for the audio
        params: device(int): choose the number of the device for the audio
        """
        super(AudioRecord, self).__init__()
        self.device = None
        self.card_num = card_num
        self.device_num = device_num

    def device_avalible(self):
        """
        Output all audio availabe in current system
        """
        os.system("arecord -l")

    def raw_output(self, save_path):
        """
        Output raw audio

        params: save_path(string): choose which type to output
        """
        print("Start logging, ctrl-c to stop")
        os.system(f"arecord -Dhw:{self.card_num},{self.device_num} -c 2 -r 44100 -f S16_LE {save_path}")
