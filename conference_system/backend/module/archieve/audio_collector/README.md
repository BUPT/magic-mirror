# 使用说明

## 安装
```
sudo apt-get install audio-recorder
```

## 录音
```
# 查看音频设备
arecord -l  # 不同设备不一定相同
>>>
**** List of CAPTURE Hardware Devices ****
card 1: Generic_1 [HD-Audio Generic], device 0: CX8200 Analog [CX8200 Analog]
  Subdevices: 0/1
  Subdevice #0: subdevice #0

# 录制音频，按ctrl+c结束，
arecord -Dhw:1,0 -c 2 -r 44100 -f S16_LE test.wav
#      -Dhw:1,0 表示 card1，device0

# 录制10秒音频，与上面变化就是-d参数
arecord -Dhw:1,0 -d 10 -f S16_LE  -r 44100 -c 2  test.wav
```

## 播放
```
aplay test.wav
```

## TODO
- [] pyalsaaudio:一个对alsa进行包装的python工具库，可能会更适合后面的工作
