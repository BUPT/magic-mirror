'''
运行环境 ubuntu16.04
使用说明 请先安装python3以及相应的库
程序功能 使用单个相机进行相关相机测试
        1. 使用制定UVC相机
        2. 设置曝光时间
        3. 是否保存图片
        4. 是否GUI显示
'''

import os
import ast
import time
import shutil
import argparse
import select
import logging

import v4l2capture
import cv2 as cv
import numpy as np
from PIL import Image


parser = argparse.ArgumentParser()
parser.add_argument('--device-id', type=int, required=True,
                    help='/dev/videoX，这个x，也就是设备号',)
parser.add_argument('--auto-mode', type=ast.literal_eval,
                    default=False, help='是否自动曝光')
parser.add_argument('--exp', type=int, default=15, help='曝光时间：1ms=10 10ms=100')
parser.add_argument('--is-show', type=ast.literal_eval,
                    default=False, help='是否为显示模式，默认否')
parser.add_argument('--save-file', type=ast.literal_eval,
                    default=False, help='是否存图，默认否')
parser.add_argument('--width', type=int, default=1920, help='图像宽度')
parser.add_argument('--height', type=int, default=1080, help='图像高度')
parser.add_argument('--multilog', type=str, default='false', help='时间日志文件是否存成多份')



args = parser.parse_args()
if args.multilog=='false':
    args.multilog=False
else:
    args.multilog=True
print(args)

log_file = 'video{}-error.log'.format(args.device_id)

if os.path.exists(log_file):
    print(os.popen('tail -100 {}'.format(log_file)).read())
    os.remove(log_file)

logging.basicConfig(filename=log_file, level=logging.INFO)

cams = os.popen('ls /dev/video*').read().split()

# Open the video device.

video = v4l2capture.Video_device(cams[args.device_id])
# config
if args.auto_mode:
    video.set_exposure_auto(3)  # 设置为手动曝光模式 1是手动 3是自动
else:
    video.set_exposure_auto(1)
    video.set_exposure_absolute(args.exp)  # 设置曝光参数
video.set_auto_white_balance(1)  # 设置白平衡
size_x, size_y = video.set_format(
    args.width, args.height, fourcc='MJPG')  # 设置图像分辨率


# dpath = "video{}-save-file".format(args.device_id)
dpath = "video-save-file"


def create_dir(dpath):
    if os.path.exists(dpath):
        shutil.rmtree(dpath)
        os.mkdir(dpath)
    else:
        os.mkdir(dpath)


def join(img1, img2, flag='horizontal'):
    """合并两张图片
    :param png1: path
    :param png2: path
    :param flag: horizontal or vertical
    :return:
    """
    # img1, img2 = Image.open(png1), Image.open(png2)
    img1, img2 = Image.fromarray(img1), Image.fromarray(img2)
    img2 = img2.resize([600, 300])
    size1, size2 = img1.size, img2.size
    # print(size1)
    if flag == 'horizontal':
        joint = Image.new('RGB', (size1[0] + size2[0], size1[1]))
        loc1, loc2 = (0, 0), (size1[0], 0)
        joint.paste(img1, loc1)
        joint.paste(img2, loc2)
        return np.asarray(joint)
    elif flag == 'vertical':
        joint = Image.new('RGB', (size1[0], size1[1] + size2[1]))
        loc1, loc2 = (0, 0), (0, size1[1])
        joint.paste(img1, loc1)
        joint.paste(img2, loc2)
        return np.asarray(joint)


if args.save_file:
    create_dir(dpath)
    create_dir('timelog')
    fp_count = 0
    fp = open('timelog/timestamp-{}.log'.format(fp_count), 'w')

video.create_buffers(2)
video.queue_all_buffers()
video.start()

if args.is_show:
    cv.namedWindow("video{}".format(args.device_id), cv.WINDOW_NORMAL)
start = time.time()
cur_start = time.time()
index = 0
cur_index = 0
error_count = 0

while True:
    try:
        select.select((video,), (), ())
        image_data = video.read_and_queue()
        frame = cv.imdecode(np.frombuffer(
            image_data, dtype=np.uint8), cv.IMREAD_COLOR)
        fname = dpath + '/' + str(index) + '.jpg'
        shape = frame.shape
        index += 1
        cur_index += 1

        if index % 300 == 0:
            # print('index:{} shape:{}'.format(index, shape))
            print('now capture:{} images'.format(index + 1))

        if args.save_file:
            cv.imwrite(fname, frame)
            fp.write('{}:{}\n'.format(fname, time.time() - start))
            if args.multilog and index % 100 == 0:
                fp.close()
                fp_count += 1
                fp = open('timelog/timestamp-{}.log'.format(fp_count), 'w')

        if args.is_show:
            cv.imshow('video{}'.format(args.device_id), frame)
        if cv.waitKey(10) & 0xff == ord('q'):
            break
        if cur_index > 1000:
            interval = time.time() - cur_start
            now_fps = cur_index / interval
            cur_start = time.time()
            cur_index = 0
            print(
                'index:{} device:{}--->now fps:{}'.format(index, cams[args.device_id], now_fps))

    except Exception as e:
        error_count += 1
        now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        logging.info('{}-->第{}帧报错:{}出错比:{}'.format(
            now_time, index, str(e), error_count / (index + 1)))
        print('出错继续下一帧')
    except KeyboardInterrupt:
        break
fp.close()

end = time.time()
cost_time = end - start
print('device:{}--->final fps:{} cost-time:{}'.format(
    cams[args.device_id], index / cost_time, cost_time))
if args.save_file:
    counts = len(os.listdir(dpath))
    print("save {} images".format(counts))

video.close()
if args.is_show:
    cv.destroyAllWindows()
