# -*- encoding: utf-8 -*-
'''
@File        :   make_ID.py
@Time        :   2020/05/23 20:27:17
@Author      :   Yu Zihong
@Version     :   2.0
@Contact     :   yu-zh19@mails.tsinghua.edu.com
@License     :   (C)Copyright 2019-2020 YZH
@Description :   make ID card for THUMBers with formatted naming photos
'''

import numpy as np
import cv2
from PIL import ImageFont, ImageDraw, Image
import os

# 一般不用改这些
HEIGHT = 377
WIDTH = 307
BACKGROUND = 'empty_ID.jpg'
FIXED_TEXT = '姓　　名\n性　　别\n声　　部\n院　　系\n学　　号\n入队年份'
PHOTOPATH = './input/'
OUTPUT = './output/'

# ------ 宣传副如果觉得要改改文字字体位置之类的，可以改这里  ------
is_designing = 0  # 改为1就开始设计模式，0就是工作模式
# 用“一”是为了帮助判断对齐
D_FIXED_TEXT = '姓　　一\n性　　一\n声　　一\n院　　一\n学　　一\n入队年一'
d_text, d_number = '一大乐\n一\n一一声部\n电机工程与应用电子技术系', '3017011123\n3019'
# 照片的位置
photo_x = 660
photo_y = 220
# 固定的文字
fixed_fontname = '/simhei.ttf'
fixed_location_x = 45
fixed_location_y = 235
fixed_fontsize = 32
fixed_spacing = 36
# 可变的文字
var_fontname = '/simhei.ttf'
var_location_x = 170 + 40
var_location_y = 230
var_fontsize = 41
var_spacing = 28
# 数字（学号和年份）
num_fontname = '/arial.ttf'
num_location_x = var_location_x
num_location_y = var_location_y + (var_fontsize - 5 + var_spacing) * 4 - 3
num_fontsize = 43
num_spacing = var_spacing - 3
# --------------------------------------------------------------------------------


def make_dir(path):
    '''
    如果当前目录下没有该路径，就创建一个
    '''
    if not os.path.exists(path):
        os.makedirs(path)


def cv_imread(filePath):
    '''
    读取图片，解决cv2.imread无法读取中文路径问题
    '''
    return cv2.imdecode(np.fromfile(filePath, dtype=np.uint8), -1)


def get_info_and_photo_path(path):
    '''
    遍历给定的文件夹，解析出其中所有照片的信息和路径，并返回二重list\n
    list = [[txt, number, path],]\n
    照片命名需按“姓名-性别-声部-院系-学号-入队年份”的格式\n
    排除了其中的txt文件
    '''
    info_and_path = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if '.txt' not in file:
                path = root + '/' + file
                items = file.split('-')
                items[-1] = items[-1].split('.')[0]  # 去掉“.jpg”
                txt = "\n".join(items[:4])
                number = "\n".join(items[4:])
                info_and_path.append([txt, number, path])
    return info_and_path


def cv_resize(img, scale):
    '''
    等比例放大或缩小图片，选用不同的插值方式：\n
    放大 - 三次样条 INTER_CUBIC \n
    缩小 - 区域插值 INTER_AREA
    '''
    if scale > 1:
        return cv2.resize(
            img, (0, 0), fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
    elif scale < 1:
        return cv2.resize(
            img, (0, 0), fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
    else:
        return img


def get_photo(path):
    '''
    读取照片文件，并做自适应处理：\n
    若太高瘦，则将宽度调整到307，然后裁剪出上面的377像素\n
    若太矮胖，则将高度调整到377，然后从中间裁剪出307像素\n
    若符合比例但不是307，就缩放到307
    '''
    img = cv_imread(path)
    h, w, channels = img.shape
    if channels == 4:
        # png
        img = img[:, :, 0:3]
    if h / w > HEIGHT / WIDTH:
        # too high, crop from top
        scale = WIDTH / w
        img = cv_resize(img, scale)
        img = img[0:HEIGHT, :]
    elif h / w < HEIGHT / WIDTH:
        # too wide, crop by middle
        scale = HEIGHT / h
        img = cv_resize(img, scale)
        h_new, w_new, channels_new = img.shape
        w_middle = int(w_new / 2)
        w_left = w_middle - int(WIDTH / 2)
        w_right = w_middle + int(WIDTH / 2) + 1
        img = img[:, w_left:w_right]
    elif w != WIDTH:
        # exactly the scale, such as 614*754, no need to crop
        scale = WIDTH / w
        img = cv_resize(img, scale)
    return img


def add_photo(back, photo, x, y):
    '''
    将照片photo合并到照片back上\n
    坐标x，y（像素）是photo左上角的所处的位置\n
    坐标原点在图片back左上角
    '''
    img = back
    img[y:y + HEIGHT, x:x + WIDTH] = photo
    return img


def add_text(img, text, fontname, location, size, spacing, color=(0, 0, 0, 0)):
    '''
    在图片中添加文字，可改变字体、字的位置、字的大小、字的行距、字的颜色（r,g,b,alpha）\n
    '''
    font = ImageFont.truetype(fontname, size)
    img_pil = Image.fromarray(img)
    draw = ImageDraw.Draw(img_pil)
    if is_designing:
        print('text is:')
        print('------------')
        print(text)
        print('------------')
        print('text square size is:')
        print(draw.textsize(text, font=font, spacing=spacing))
    draw.text(location, text, font=font, fill=(0, 0, 0, 0), spacing=spacing)
    img = np.array(img_pil)
    return img


def make_one(back, photo, text, number):
    '''
    制作一张队员证，依次添加照片、汉字、数字
    '''
    img1 = add_photo(back, photo, photo_x, photo_y)
    img2 = add_text(
        img1,
        text,
        fontname=var_fontname,
        location=(var_location_x, var_location_y),
        size=var_fontsize,
        spacing=var_spacing)
    img3 = add_text(
        img2,
        number,
        fontname=num_fontname,
        location=(num_location_x, num_location_y),
        size=num_fontsize,
        spacing=num_spacing)
    return img3


def make_all():
    '''
    制作所有队员证
    '''
    print('start making...')
    make_dir(OUTPUT)
    background = cv_imread(BACKGROUND)
    background = add_text(
        background,
        FIXED_TEXT,
        fontname=fixed_fontname,
        location=(fixed_location_x, fixed_location_y),
        size=fixed_fontsize,
        spacing=fixed_spacing)
    info_and_path = get_info_and_photo_path(PHOTOPATH)
    length = len(info_and_path)
    print('%d photos in all' % length)
    for i, item in enumerate(info_and_path):
        text, number, path = item
        photo = get_photo(path)
        IDcard = make_one(background, photo, text, number)
        name = text.split()[0]
        outputname = OUTPUT + name + '.jpg'
        cv2.imencode('.jpg', IDcard)[1].tofile(outputname)
        print('making %d / %d' % (i + 1, length), end='\r')
    print()
    print('done')


def design():
    '''
    开始设计，将会在当前目录下生成'a_designing_IDcard.jpg'的样张
    '''
    background = cv_imread(BACKGROUND)
    background = add_text(
        background,
        D_FIXED_TEXT,
        fontname=fixed_fontname,
        location=(fixed_location_x, fixed_location_y),
        size=fixed_fontsize,
        spacing=fixed_spacing)
    info_and_path = get_info_and_photo_path(PHOTOPATH)
    a_photo_path = info_and_path[0][2]  # [index][2] 第二维的2不能改
    photo = get_photo(a_photo_path)
    IDcard = make_one(background, photo, d_text, d_number)
    outputname = 'a_designing_IDcard.jpg'
    cv2.imencode('.jpg', IDcard)[1].tofile(outputname)
    print('check the image~')


if __name__ == "__main__":

    if is_designing:
        design()
    else:
        make_all()

    # Additionally, if xuanchuanfu thinks elements need to be adjusted, please
    # refer to <line 25> ~ <line 51>, and switch is_designing on <line 26> to 1
    # to start designing, and don't forget to switch it back to 0 after designing
