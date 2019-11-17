"""
File: process_video.py
Author: VDeamoV
Email: vincent.duan95@outlook.com
Github: https://github.com/VDeamoV
Description:
    Direct use ffmpeg command to sperate the video. The corresponding timestamp
    are saved in the relevant files
"""
import os
import subprocess


class StreamProcessor:
    """
    StreamProcessor is used to cut the video or audio by the config file
    >>> process = StreamProcessor('./config', './input', './output')
    >>> process.start()
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

    def start(self):
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


def test():
    """
    test function
    """
    process = StreamProcessor('./example_config.txt', './', './output')
    process.start()

if __name__ == "__main__":
    test()
