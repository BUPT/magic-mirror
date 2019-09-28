import os
import subprocess
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--image-path", type=str,
                    default="video-save-file", help="需要合并的图片集合")
parser.add_argument("--fps", type=int, default=25, help="目标视频的帧率")
parser.add_argument("--target-file", type=str,
                    default="output.mp4", help="输出视频文件名字")
args = parser.parse_args()


image_path = args.image_path
fps = args.fps
target_file = args.target_file

# 对图片文件名字进行重命名,按照0-n的顺序进行排序,方便ffmpeg进行合并
imgs = sorted([path for path in os.listdir(image_path)],
              key=lambda x: int(x.split('.')[0]))

new_imgs = [os.path.join(image_path, '{}.jpg'.format(i))
            for i in range(len(imgs))]

for old, new in zip(imgs, new_imgs):
    os.rename(os.path.join(image_path, old), new)

print('>>>>>>>开始合并...')
command = "ffmpeg -start_number 0 -i '{}/%d.jpg' -r {} -vcodec mpeg4 -b:v 4000k  {}".format(
    image_path, fps, target_file)
subprocess.call(command, shell=True)
print('<<<<<<<合并结束')
