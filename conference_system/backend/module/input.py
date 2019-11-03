"""
File: input.py
Author: Duan-JM
Email: vincent.duan95@outlook.com
Github: https://github.com/Duan-JM
Description:
    Input Module is used to receive data from hardware or somewhere else, the
    ouput of the module will be used in Process Module
"""
import os
import v4l2capture

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
        raise NotImplementedError

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
    def __init__(self):
        super(VideoRecord, self).__init__()
        self.device = None

    def set_device(self, data_source_device):
        """
        Set the video source input device

        params: data_source_device(string)

        return: flag(boolen): check if device exist
        """
        if os.path.exists(data_source_device):
            self.device=data_source_device
        else:
            raise ValueError(f"{data_source_device} you choose is not exists")

    def device_avalible(self):
        """
        Output all video availabe in current system
        """
        print(os.popen('ls /dev/video*').read())

    def raw_output(self, save_path):
        """
        Output video, timelog and images to the save_path

        params: save_path(string): choose which type to output
        """
        # if path exist -> output to save_path
        # elif raise error, later may change to live strea
