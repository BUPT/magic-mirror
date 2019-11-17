"""
File: lecture_generate_service.py
Author: Duan-JM
Email: vincent.duan95@outlook.com
Github: https://github.com/Duan-JM
Description:
    Lecuture generate service is used to record
    and merge lecuture video
"""
from ..module.input import VideoRecord
from ..module.input import AudioRecord
from ..module.process import PeopleExistTimeProcess
from ..module.action import PicToVideo
from ..module.action import SplitAction
from ..module.action import MergeMediaAction

class LectureGenerateService:
    """
    How to use

    params: video_dev(string)
    params: audio_dev(string)
    params: screen_dev(string)
    params: cache_dir(string): the place to store interval files

    >>> lecture_generate_service = LectureGenerateService(
            video_dev='/dev/video0',
            screen_dev='/dev/video1',
            audio_dev='/dev/xxx',
            cache_dir='/tmp/lecutre_cache_file',
            output_dir='./',
            merge_config='./merge_config.json')
    >>> lecture_generate_service.record() # record audio video screen
    >>> lecture_generate_service.video_parse() # use AI to detect timestamp
    >>> lecture_generate_service.generate_video() # generate video
    >>> lecture_generate_service.clean_up() # clean the interval files to free up
    """

    def __init__(self, video_dev, screen_dev, audio_dev,
                 cache_dir, output_dir, merge_config,):
        self.video_dev = video_dev
        self.screen_dev = screen_dev
        self.audio_dev = screen_dev
        self.cache_dir = cache_dir
        self.output_dir = output_dir
        self.merge_config = merge_config

    def __config_check(self):
        """
        check if all input is legal

        if cache_dir none exist then create one
        """
        pass

    def record_video(self):
        """
        use input model to output files to cache_dir
        """
        video_record = VideoRecord((1920, 1080), self.video_dev)
        video_record.raw_output(self.cache_dir)


    def record_audio(self):
        audio_record = AudioRecord(self.audio_dev, 0)
        audio_record.raw_output(self.cache_dir)


    def video_parse(self):
        """
        use process model to parse video and get timestamp
        """
        pass

    def generate_video(self):
        """
        use video autio screen_record to generate video
        """
        pass

    def clean_up(self):
        """
        clean up the cache_dir
        """
        pass
