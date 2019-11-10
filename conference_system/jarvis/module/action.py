"""
File: action.py
Author: Duan-JM
Email: vincent.duan95@outlook.com
Github: https://github.com/Duan-JM
Description:
    Define the Actions, such as send emails, split video/audio, merge video/audio
"""
import os
import subprocess

class BaseAction:
    """
    base action module for futuer
    """
    def process(self):
        """
        Use `self.input_data` to do some actions
        """
        raise NotImplementedError


class PicToVideo(BaseAction):
    """
    combine picture batches to video
    """
    def __init__(self, pic_batch_path):
        """
        params: pic_batch_path(string): where is the pictures

        return: mp4 video
        """
        self.pic_batch_path = pic_batch_path

    def process(self, fps, target_file):
        # sort pic by name, from 0 to n
        imgs = sorted([path for path in os.listdir(self.pic_batch_path)],
                      key=lambda x: int(x.split('.')[0]))

        new_imgs = [os.path.join(self.pic_batch_path, '{}.jpg'.format(i))
                    for i in range(len(imgs))]

        for old, new in zip(imgs, new_imgs):
            os.rename(os.path.join(self.pic_batch_path, old), new)

        print('>>>>>>>开始合并...')
        command = "ffmpeg -start_number 0 -i '{}/%d.jpg' -r {} -vcodec mpeg4 -b:v 4000k  {}".format(self.pic_batch_path, fps, target_file)
        subprocess.call(command, shell=True)
        print('<<<<<<<合并结束')


class SplitAction(BaseAction):
    """
    Direct use ffmpeg command to sperate the video. The corresponding timestamp
    >>> process = SplitAction('./config', './input', './output')
    >>> process.start()

    Example config_file:
    ```bash
    system.mp4 | test.mp4 | 00:00:00 | 00:00:01
    system.mp3 | test.mp3 | 00:00:00 | 00:00:01

    ```
    """
    def __init__(self, config_path, input_path='./', output_path='./'):
        self.config_path = config_path
        self.input_path = input_path
        self.output_path = output_path

    def _config_precheck(self):
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)

        if not os.path.exists(os.path.join(self.input_path, self.config_path)):
            raise ValueError("Input path does not exist")

        if not os.path.exists(self.config_path):
            raise ValueError("Config file does not exist")

    def _get_output_log(self):
        """
        return log file fg
        """
        runtime_log = open(os.path.join(self.output_path, "runtime.log"), 'a')
        error_log = open(os.path.join(self.output_path, "error.log"), 'a')
        return runtime_log, error_log

    def process(self):
        """
        Start processing the operation refer to the config file
        """
        self._config_precheck()
        runtime_log, error_log = self._get_output_log()

        with open(self.config_path) as f:
            for line in f.readlines():
                input_name, output_name, start, end = line.split('|')
                input_name = os.path.join(self.input_path, input_name.strip())
                output_name = os.path.join(self.output_path, output_name.strip())

                assert not os.path.exists(output_name), \
                    "Ouput_file exists! Please double check output path"

                cmd = [
                    "ffmpeg", "-i",
                    input_name,
                    "-ss",
                    start.strip(),
                    "-to",
                    end.strip(),
                    "-c", "copy",
                    output_name,
                    "-hide_banner", ]
                subprocess.run(cmd, stdout=runtime_log, stderr=error_log)
        runtime_log.close()
        error_log.close()


class MergeMediaAction(BaseAction):
    #  TODO: Plz refine the params#
    """
    author_mail: ximingxing@gmail.com

    to use:
    m = MergeMediaAction(video_path1="./human.mp4",video_path2="./speech.mp4",audio_path="./audio.mp3", output_path="./output.mp4")
    m.process() following is the use of param.

    :param video_path1: human video's path
    :param cut_position: human video's cut position, the format is (width,height,x1,y1)
    :param cut_time_during: how long should the human video be cutted
    :param scale_size:the size to scale the human video
    :param video_path2: speech video's path
    :param merge_position: two video's merge position, position that we need to overlay (x1,y1)
    :param audio_name: audio name
    :param output_path: the final audio's output path
    :param use_configuration_file: whether to use configuration file 
    """
    def __init__(self,
                 video_path1="./human.mp4", cut_position="500:500:390:220", cut_time_during=60,
                 scale_size="100:100", video_path2="./speech.mp4", merge_position="W-w:H-h",
                 audio_path="./audio.mp3", output_path="./output.mp4",
                 use_configuration_file=False):
        self.video_path1 = video_path1,
        self.cut_position = cut_position,
        self.cut_time_during = cut_time_during,
        self.scale_size = scale_size,

        self.video_path2 = video_path2,
        self.merge_position = merge_position,

        self.audio_path = audio_path,

        self.output_path=output_path

        assert os.path.exists(self.video_path1), "video1 is not exist!"
        assert os.path.exists(self.video_path2), "video2 is not exist!"
        assert os.path.exists(self.audio_path), "audio is not exis!"
        assert not os.path.exists(self.output_path), "output_path has exist!"

    def _cut_human(self):
        cut_human = "ffmpeg -i {} -vf crop={} ,scale={} ./cutted_human.mp4"\
                .format(self.video_path1, self.cut_position, self.scale_size)
        return cut_human

    def _overlay(self):
        overlay = "ffmpeg -i {} -i ./cutted_human.mp4 -filter_complex overlay={} -max_muxing_queue_size 1024 ./overlay.mp4"\
                .format(self.video_path2, self.merge_position)
        return overlay

    def _add_audio(self):
        add_audio = "ffmpeg -i ./overlay.mp4 -i  audio_name -map 0:v -map 1:a -c copy -shortest output_path"\
                .format(self.audio_path, self.output_path)
        return add_audio

    def process(self):
        # run all the command
        print("Start cut.")
        os.system(self._cut_human)
        print("cut finish.")
        print("Start merge.")
        os.system(self._overlay)
        print("merge finish.")
        print("Start add audio.")
        os.system(self._add_audio)
        print("add audio finish.")
        if os.path.exists("./cutted_human.mp4"):
            os.remove("./cutted_human.mp4")
        if os.path.exists("./overlay.mp4"):
            os.remove("./overlay.mp4")
