# ProcessVideo Using Manual
## Intro
This script define a module which is used to split the video refer to a config file.

## Requirements
1. ffmpeg
ffmpeg are required in the system. (Not ffmpeg pip package)
```bash
sudo apt-get install ffmpeg
```

## Example Code
```python
process_model = StreamProcessor(config_path='./cut.txt', input_path='./input', output_path='./output')
# config_path means the config's path
# input_path means where to save your raw stream
# output means where to ouput your files
process_model.start()
```
## Example Config File
```bash
# format are following
# | raw_stream name | output_name | split_start_time | split_end_time
system.mp4 | test.mp4 | 00:00:00 | 00:00:01
system.mp4 | test2.mp4 | 00:00:00 | 00:00:10
system.mp4 | test1.mp4 | 00:00:00 | 00:01:01
system.mp4 | test3.mp4 | 00:00:00 | 00:02:01
system.mp4 | test5.mp4 | 00:00:00 | 00:04:01

```
