"""
File: process.py
Author: Duan-JM
Email: vincent.duan95@outlook.com
Github: https://github.com/Duan-JM
Description:
    The module here is used the AI/none methods to process the data
    then give the actions' params
"""
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

    def take_action(self, params):
        """
        params: params: the params for the actions

        return: flag(boolen): check if action have done properly
        """
        raise NotImplementedError

class BaseDetectronProcess(BasicProcess):
    """
    Using Detectron2 to detect some object
    """
    NotImplementedError


class PeopleExistTimeProcess(BaseDetectronProcess):
    """
    Use output of the detectron2, to accomplish some function
    """
    NotImplementedError
