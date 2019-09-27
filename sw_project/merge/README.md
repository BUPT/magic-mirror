* [Introduction](#introduction)
* [Usage](#usage)


# Introduction
code to merge two video and add a audio to video.
# Usage
## Dependency
- Python3
- ffmpeg

need add ffmpeg to *environmental variable*, download ffmpeg [here](https://ffmpeg.zeranoe.com/builds/). (*remember to dwonload the **static** one and unzip*)

## Use
```python
import merge 
merge(video_path1="", cut_position="", cut_time_during="",  # human video args
          video_path2="", merge_position="",  # speech video args
          audio_name="", output_path="")
```

-  function paramter:   
    video_path1: human video's path  
    cut_position: human video's cut position, the format is (width,height,x1,y1)  
    cut_time_during: how long should the human video be cutted  
    video_path2: speech video's path  
    merge_position: two video's merge position, position that we need to overlay (x1,y1)  
    audio_name: audio name  
    output_path: the final audio's output path  
    return: None  
- default param you can see code