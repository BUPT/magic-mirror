* [介绍](#介绍)
* [使用](#使用)


# 介绍
给定一个ppt视频、一个人物视频和一个音频文件，可以实现如下功能：
- 人物的裁剪和缩放
- 人物视频和ppt视频的合成
- 给合成之后的视频添加音频
# 使用
## 依赖
- Python3
- ffmpeg

需要添加ffmpeg到“环境变量”，ffmpeg下载地址可以[点击这里](https://ffmpeg.zeranoe.com/builds/)。（下载static包解压即可）

## 代码
```python
import merge
def merge(video_path1="./human.mp4", cut_position="500:500:390:220", cut_time_during="60", scale_size="100:100",
          video_path2="./speech.mp4", merge_position="W-w:H-h",  
          audio_name="./audio.mp3", output_path="./output.mp4",
          use_configuration_file=False)
```

###  函数参数
- video_path1: 人物视频的位置，默认为"./human.mp4"
- cut_position: 裁剪视频的位置，格式是：长:宽:起始x:起始y，默认为"500:500:390:220"
- cut_time_during: 视频裁剪的长度，目前无用，默认60s
- scale_size:裁剪后视频的缩放参数，格式是：长:宽，默认是"100:100"
- video_path2: ppt视频的位置，默认是"./speech.mp4"
- merge_position: 人物视频叠加到ppt视频的位置，格式是：长:宽，默认是"W-w:H-h"
- audio_name: 音频位置，默认是"./audio.mp3"
- output_path: 输出最终视频的位置，默认是"./output.mp4"
- use_configuration_file: 是否使用配置文件"./configuration.txt",默认不使用
### 说明
传入参数的方式有两种
- 第一种是直接在调用函数的时候传入参数即可
- 第二种是在配置文件中依次写入每个参数，参数之间使用空格分开即可，然后注意需要把参数use_configuration_file设为True

## 存在问题
- 现阶段应该问题不大，还缺少一点视频、音频长度不等时的处理机制，后面可能需要处理一下
- 对实时流的处理还未实现
