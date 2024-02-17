#! /usr/bin/env python
# -*- coding: utf-8 -*-
__all__ = ('time_stamp', 'load_pkl', 'save_pkl', 'load_json', 'save_json', 'calculate_str_similarity',
           'save_list2txt', 'load_txt2list',
           'read_excel_with_header', 'text2qrimg',
           'image_float2uint', 'prename_from_abs_path', 'name_from_abs_path',
           'mkdir', 'rmdir', 'clear_mkdir', 'check_command', 'filter_df_column_with_list', 'pd_column_to_list')

import difflib
import errno
import imghdr
import json
import logging
import os
import pickle as pkl
from shutil import rmtree
from time import strftime

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image


def time_stamp():
    """时间戳：年月日时分"""
    return strftime('%Y%m%d%H%M%S')


def load_pkl(path):
    with open(path, 'rb') as f:
        pkl_file = pkl.load(f)
    return pkl_file


def save_pkl(pkl_file, path):
    with open(path, 'wb') as f:
        pkl.dump(pkl_file, f)


def load_json(path):
    with open(path, 'r') as f:
        json_file = json.load(f)
    return json_file


def save_json(json_file, path):
    json.dump(json_file, open(path, 'w'))


def calculate_str_similarity(str1, str2):
    """检测两个字符串有多相似"""
    seq = difflib.SequenceMatcher(None, str1, str2)
    return seq.ratio()


def load_txt2list(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        return [line.strip() for line in lines]


def save_list2txt(content_list, txt_path):
    """将list内容写入txt，每个元素之间换行"""
    with open(txt_path, 'w') as f:
        for content_i in content_list:
            f.write(content_i)
            f.write('\n')


def read_excel_with_header(file_path, header=0):
    """header是列名，=0表示首行是各项，=1表示第二行是各项，=[0, 1]表示前两行都是"""
    df = pd.read_excel(file_path, header=header)
    return df


def text2qrimg(text, save_path):
    """
    # 要生成二维码的字符串
    text = "臭宝宝"
    """
    # 生成二维码
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(text)
    qr.make(fit=True)
    
    # 生成二维码图片
    img = qr.make_image(fill_color="black", back_color="white")
    
    # 保存二维码图片
    img.save(save_path)


def split_list_into_n_lists(primary_list, n):
    """将primary_list n 尽可能等分，返回一个含有n个列表的列表"""
    primary_length = len(primary_list)
    assert primary_length > n
    length_n, reminder = divmod(primary_length, n)  # 基本长度和余数
    list_of_lists = []
    start = 0
    for i in range(n):
        if i < reminder:
            end = start + length_n + 1
        else:
            end = start + length_n
        list_i = list(primary_list[start:end])
        list_of_lists.append(list_i)
        start = end
    return list_of_lists


def image_float2uint(nd_arr):
    """将0~1范围的float 图片准换为0~255的uint8格式"""
    return (nd_arr * 255).astype(np.uint8)


def prename_from_abs_path(path):
    """从绝对路径获取文件名"""
    name = os.path.split(path)[1]
    prename = os.path.splitext(name)[0]
    return prename


def name_from_abs_path(path):
    """从绝对路径获取带有后缀的文件名"""
    name = os.path.split(path)[1]
    return name


def mkdir(path):
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


def rmdir(path):
    """递归删除，path所指的文件夹也删除"""
    try:
        rmtree(path)
    except:
        pass


def clear_mkdir(path):
    """更新建立文件夹"""
    rmdir(path)
    mkdir(path)


def check_command(command):
    """对有问题的命令进行调整"""
    focus_chars = ['(', ')']
    for focus_char in focus_chars:
        valid_statement = '\\' + focus_char
        # print(valid_statement)
        if (focus_char in command) and (valid_statement not in command):
            command = command.replace(focus_char, valid_statement)
    return command


def filter_df_column_with_list(df, column_name, filter_list):
    """过滤得到新的df，要求column_name这一列的内容在filter_list里面"""
    df_wanted = df[df[column_name].isin(filter_list)]
    return df_wanted


def pd_column_to_list(df, column_name):
    return df[column_name].values.tolist()


def copy_image(source_path, target_folder):
    # work_dir = os.getcwd()
    # # 先进入源文件夹
    # os.chdir(source_folder)
    # 图片复制
    copy_command = f'cp {source_path} {target_folder}'
    copy_command = check_command(copy_command)
    os.system(copy_command)
    
    # 回到原工作路径
    # os.chdir(work_dir)


def what_type_image(image_file):
    """接受图片路径或数据流作为输入，返回图片类型或None"""
    if os.path.isdir(image_file):
        return None
    return imghdr.what(image_file)


def fetch_image_paths(folder):
    """获取文件夹中所有图片的路径"""
    image_paths = []
    for file_name in os.listdir(folder):
        file_path = os.path.join(folder, file_name)
        if what_type_image(file_path):
            image_paths.append(file_path)
    return image_paths


def subplot_images(subplot_size, images, save_path=None, show=True):
    """subplot several images
    Args:
        subplot_size (tuple, list): e.g. (2, 2) or (1, 3)
        images (tuple, list): a tuple of ndarray images
        save_path (str): path to save plot
        show (bool): whether show this plot or not
    """
    height, width = subplot_size
    for image_index in range(height * width):
        plt.subplot(height, width, image_index + 1)
        plt.imshow(images[image_index])
    if save_path is not None:
        plt.savefig(save_path)
    if show:
        plt.show()


def pil_read_image(image_path, to_array=True):
    """比opencv还快"""
    image = Image.open(image_path)
    if to_array:
        image = np.array(image)
    return image


def pil_save_image(ndarray, image_path):
    """图片的后缀可以自行设置"""
    im = Image.fromarray(ndarray)
    im.save(image_path)


def mask2box(mask):
    """may be not efficient
    Args:
        mask (nd): e.g.(1024, 1024, ...), not necessarily to be 2d

    Returns:
        box
    """
    rows = np.any(mask, axis=1)
    cols = np.any(mask, axis=0)
    rmin, rmax = np.where(rows)[0][[0, -1]]
    cmin, cmax = np.where(cols)[0][[0, -1]]
    
    return rmin, cmin, rmax + 1, cmax + 1  # x1, y1, x2, y2


def box_iou(bb1, bb2):
    """
    Calculate the Intersection over Union (IoU) of two bounding boxes.
    Parameters
    ----------
    bb1 : nd1d [x1, y1, x2, y2]
        The (x1, y1) position is at the top left corner,
        the (x2, y2) position is at the bottom right corner
    bb2 : the same
    Returns
    -------
    float
        in [0, 1]
    """
    assert bb1[0] < bb1[2]
    assert bb1[1] < bb1[3]
    assert bb2[0] < bb2[2]
    assert bb2[1] < bb2[3]
    
    # determine the coordinates of the intersection rectangle
    x_left = max(bb1[0], bb2[0])
    y_top = max(bb1[1], bb2[1])
    x_right = min(bb1[2], bb2[2])
    y_bottom = min(bb1[3], bb2[3])
    
    if x_right < x_left or y_bottom < y_top:
        return {'bool_intersect': False}
    
    # The intersection of two axis-aligned bounding boxes is always an
    # axis-aligned bounding box
    intersection_area = (x_right - x_left) * (y_bottom - y_top)
    
    # compute the area of both AABBs
    bb1_area = (bb1[2] - bb1[0]) * (bb1[3] - bb1[1])
    bb2_area = (bb2[2] - bb2[0]) * (bb2[3] - bb2[1])
    
    # compute the intersection over union by taking the intersection
    # area and dividing it by the sum of prediction + ground-truth
    # areas - the interesection area
    iou = intersection_area / float(bb1_area + bb2_area - intersection_area)
    assert iou >= 0.0
    assert iou <= 1.0
    return {'bool_intersect': True, 'iou': iou,
            'intersection': intersection_area, 'intersection_coord': [x_left, y_top, x_right, y_bottom],
            'box1': bb1_area, 'box2': bb2_area}


def box_match(box1, box2, threshold=0.5):
    """根据两个框左上角和右下角的坐标，判断是否能认为是同一个框，标准见机行事
    Args:
        box1 (nd1d):
        box2 (nd1d):
        threshold (float 0~1): 据此判断是否可认为是一个框

    Returns:
        bool
    """
    iou_dict = box_iou(box1, box2)
    if isinstance(iou_dict, dict):
        iou, intersection, box1_area, box2_area = iou_dict['iou'], iou_dict['intersection'], \
            iou_dict['box1'], iou_dict['box2']
        if ((intersection / box1_area) > threshold) or ((intersection / box2_area) > threshold):
            return 1
        else:
            return 0
    else:
        return 0


def plain_logger(log_path, log_name):
    """init logger"""
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    logging.basicConfig(filename=log_path, level=logging.INFO, filemode='w', format=LOG_FORMAT)
    logger = logging.getLogger(log_name)
    return logger
