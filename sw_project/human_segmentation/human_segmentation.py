import sys
import ast
import argparse
import cv2
import numpy as np
import torch

sys.path.append('BLSeg/')
from blseg import model

MEAN = (0.485, 0.456, 0.406)
STD = (0.229, 0.224, 0.225)
TARGET_IDX = 1

parser = argparse.ArgumentParser()
parser.add_argument('--input-file', type=str, required=True, help='选择输入文件')
parser.add_argument('--threshold', type=float, default=0.2, help='人体在图片中占比的阈值')
parser.add_argument('--model-params', type=str, required=True, help='加载的分割模型参数')
parser.add_argument('--seg-model',
                    type=str,
                    default='unet',
                    help='选择分割模型，默认：unet')
parser.add_argument('--backbone-model',
                    type=str,
                    default='resnet34',
                    help='选择骨干模型，默认：resnet34')
parser.add_argument('--gpu',
                    type=ast.literal_eval,
                    default=False,
                    help='是否使用GPU， 默认：否')
parser.add_argument('--gpu-id', type=int, default=0, help='选择使用哪块GPU')
args = parser.parse_args()
print(args)


def parse_input_file(input_file_path):
    ''' parse input file
    params input_file_path: str, input file path

    return image_path_list: list, list of image path
    return timestamp_list: list, list of timestamp
    '''
    image_path_list = list()
    timestamp_list = list()

    with open(input_file_path, 'r') as f:
        # TODO: need some sample of the input file
        pass
    return image_path_list, timestamp_list


def normalize(img, mean, std, max_pixel_value=255.0):
    mean = np.array(mean, dtype=np.float32)
    mean *= max_pixel_value

    std = np.array(std, dtype=np.float32)
    std *= max_pixel_value

    denominator = np.reciprocal(std, dtype=np.float32)

    img = img.astype(np.float32)
    img -= mean
    img *= denominator
    return img


def initialization():
    net = model.ModernUNet()
    net.load_parameters(args.model_params)

    if args.gpu:
        net = net.cuda()
    return net


def get_timestamp(image_path_list, timestamp_list, net):
    for image_path, timestamp in zip(image_path_list, timestamp_list):
        image = cv2.imread(image_path)
        image = normalize(image, MEAN, STD)
        image = np.transpose(image, (2, 0, 1))
        image = np.expand_dims(image, 0)
        image = torch.from_numpy(image)
        if args.gpu:
            image = image.cuda(args.model_params)
        with torch.no_grad():
            mask = net(image)
            mask = torch.argmax(mask, dim=1)
            num_target = (mask.long() == TARGET_IDX).sum().item()
            num_all = mask.nelement()
        if num_target / num_all >= args.threshold:
            return timestamp


# init model
net = initialization()
# parse input file
image_path_list, timestamp_list = parse_input_file(args.input_file)
# segmentation
timestamp = get_timestamp(image_path_list, timestamp_list, net)
print(timestamp)