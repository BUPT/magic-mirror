
# 帮助文档
使用指定相机进行视频数据采集

> 本文档输出一个视频文件,一个图像文件夹,一个图像文件所对应时间戳文件夹


## 0.安装依赖
```
# 安装v4l2capture
sudo apt-get install libv4l-dev
git clone https://github.com/cgpeter96/python-v4l2capture.git
cd python-v4l2capture
python3 setup.py build
sudo python3 setup.py install

# 安装opencv
pip install opencv-python
```

## 1.使用相机采集数据

参数说明

```
usage: capture_video.py [-h] --device-id DEVICE_ID [--auto-mode AUTO_MODE]
                        [--exp EXP] [--is-show IS_SHOW]
                        [--save-file SAVE_FILE] [--width WIDTH]
                        [--height HEIGHT]

optional arguments:
  -h, --help            show this help message and exit
  --device-id DEVICE_ID
                        /dev/videoX，这个x，也就是设备号
  --auto-mode AUTO_MODE 
                        是否自动曝光
  --exp EXP             曝光时间：1ms=10 10ms=100
  --is-show IS_SHOW     是否为显示模式，默认否
  --save-file SAVE_FILE
                        是否存图，默认否
  --width WIDTH         图像宽度(默认1920)
  --height HEIGHT       图像高度（默认1080）
```


例子
```
python3 capture_video.py --device-id 0 --is-show True --auto-mode True --save-file True 
#调用/dev/video0,以默认分辨率，自动曝光，可显示模式进行数据采集并保存数据
python3 capture_video.py --device-id 0 --is-show True --auto-mode True --save-file True --width 1920 --height 1080 
#根据需求设置图像分辨率
```
> 本程序会数量两个文件夹,1.图像文件夹video-save-file 2.图像对应的时间戳文件夹timelog



## 2.将存储为视频

参数说明
```
usage: combine_images2video.py [-h] [--image-path IMAGE_PATH] [--fps FPS]
                               [--target-file TARGET_FILE]

optional arguments:
  -h, --help            show this help message and exit
  --image-path IMAGE_PATH
                        需要合并的图片集合
  --fps FPS             目标视频的帧率
  --target-file TARGET_FILE
                        输出视频文件名字

```

例子
```
python3 combine_images2video.py --image-path video-save-file --fps 29 --target-file 1.mp4 
# 将图片文件夹video-save-file以29fps形式合并为1.mp4文件
```

