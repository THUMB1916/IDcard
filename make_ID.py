# -*- encoding: utf-8 -*-
"""
@File        :   make_ID.py
@Time        :   2021/01/09 20:27:17
@Author      :   Yu Zihong
@Version     :   3.0
@Contact     :   yu-zh19@mails.tsinghua.edu.com
@License     :   (C)Copyright 2019-2020 YZH
@Description :   make ID card for THUMBers with formatted naming photos
"""

import os

from PIL import Image, ImageDraw, ImageFont

# ------------- 如果要改改文字字体位置之类的，可以改这部分  -------------

is_designing = 0  # 改为1就开始设计模式，0就是工作模式

# 文件路径和固定参数
PHOTOPATH = "./input/"
OUTPUT = "./output/"
BACKGROUND = "empty_ID.jpg"
HEIGHT = 377
WIDTH = 307
FIXED_TEXT = "姓　　名\n性　　别\n声　　部\n院　　系\n学　　号\n入队年份"

# 设计模式下的文字，用“一”和“3”是为了帮助判断对齐
D_FIXED_TEXT = "姓　　一\n性　　一\n声　　一\n院　　一\n学　　一\n入队年一"
D_TEXT, D_NUM = "一大乐\n一\n一一声部\n电机工程与应用电子技术系", "3017011123\n3019"

# 使用input文件夹下的某张照片进行设计，改变以下数字可更换照片
# 数字不能超过照片总数
d_photo_index = 0

# 照片在图中的位置
photo_x = 660
photo_y = 220

# 固定的文字
fixed_fontname = "/simhei.ttf"
fixed_location_x = 45
fixed_location_y = 235
fixed_fontsize = 32
fixed_spacing = 36
fixed_color = (0, 0, 0, 0)  # r g b alpha

# 可变的文字
var_fontname = "/simhei.ttf"
var_location_x = 170 + 40
var_location_y = 230
var_fontsize = 41
var_spacing = 28
var_color = (0, 0, 0, 0)

# 数字（学号和年份）
num_fontname = "/arial.ttf"
num_location_x = var_location_x
num_location_y = var_location_y + (var_fontsize - 5 + var_spacing) * 4 - 3
num_fontsize = 43
num_spacing = var_spacing - 3
num_color = (0, 0, 0, 0)
# --------------------------------------------------------------------------------


def get_info_and_photo_path(path):
    """
    遍历给定的文件夹，解析出其中所有照片的信息和路径，并返回二重list\n
    list = [[txt, number, path],]\n
    照片命名需按“姓名-性别-声部-院系-学号-入队年份”的格式\n
    排除了其中的txt文件
    """
    info_and_path = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if ".txt" not in file:
                path = root + "/" + file
                items = file.split("-")
                items[-1] = items[-1].split(".")[0]  # 去掉“.jpg”
                txt = "\n".join(items[:4])
                number = "\n".join(items[4:])
                info_and_path.append([txt, number, path])
    return info_and_path


def process_photo(img):
    """
    自适应缩放并裁剪照片：\n
    尺寸若高瘦，则将宽度调整到307，然后裁剪出上面的377像素\n
    尺寸若矮胖，则将高度调整到377，然后从中间裁剪出307像素\n
    """
    w, h = img.size
    scale = min(w / WIDTH, h / HEIGHT)
    new_w = round(w / scale)
    new_h = round(h / scale)
    img = img.resize((new_w, new_h))
    if new_w > WIDTH:
        # too wide, crop by middle
        left = (new_w - WIDTH) // 2
        img = img.crop((left, 0, left + WIDTH, HEIGHT))
    elif new_h > HEIGHT:
        # too high, crop from top
        img = img.crop((0, 0, WIDTH, HEIGHT))

    return img


def add_text(img, text, fontname, location, size, spacing, color=(0, 0, 0, 0)):
    """
    在图片中添加文字，可改变字体、字的位置、字的大小、字的行距、字的颜色（r,g,b,alpha）\n
    """
    font = ImageFont.truetype(fontname, size)
    draw = ImageDraw.Draw(img)
    if is_designing:
        print("\ntext is:")
        print("------------")
        print(text)
        print("------------")
        print("text square size is:")
        print(draw.textsize(text, font=font, spacing=spacing))
    draw.text(location, text, font=font, fill=color, spacing=spacing)
    return img


def make_one(back, photo, fix, text, number):
    """
    制作一张队员证，依次添加照片、汉字、数字
    """
    back = back.copy()
    # 照片
    back.paste(photo, (photo_x, photo_y))
    # 汉字（固定文字）
    add_text(
        back,
        fix,
        fontname=fixed_fontname,
        location=(fixed_location_x, fixed_location_y),
        size=fixed_fontsize,
        spacing=fixed_spacing,
        color=fixed_color,
    )
    # 汉字（个人信息）
    add_text(
        back,
        text,
        fontname=var_fontname,
        location=(var_location_x, var_location_y),
        size=var_fontsize,
        spacing=var_spacing,
        color=var_color,
    )
    # 数字
    add_text(
        back,
        number,
        fontname=num_fontname,
        location=(num_location_x, num_location_y),
        size=num_fontsize,
        spacing=num_spacing,
        color=num_color,
    )
    return back


def make_all():
    """
    制作所有队员证
    """
    print("start making...")
    os.makedirs(OUTPUT, exist_ok=True)
    info_and_path = get_info_and_photo_path(PHOTOPATH)
    length = len(info_and_path)
    print("%d photos in total" % length)
    background = Image.open(BACKGROUND)
    for i, item in enumerate(info_and_path):
        text, number, path = item
        photo = Image.open(path)
        photo = process_photo(photo)
        IDcard = make_one(background, photo, FIXED_TEXT, text, number)
        name = text.split()[0]
        outputname = os.path.join(OUTPUT, name + ".jpg")
        IDcard.save(outputname, quality=100, subsampling=0)
        print("making %d / %d" % (i + 1, length), end="\r")
    print()
    print("done")


def design():
    """
    开始设计，将会在当前目录下生成'a_designing_IDcard.jpg'的样张
    """
    background = Image.open(BACKGROUND)
    info_and_path = get_info_and_photo_path(PHOTOPATH)
    a_photo_path = info_and_path[d_photo_index][2]
    photo = Image.open(a_photo_path)
    photo = process_photo(photo)
    IDcard = make_one(background, photo, D_FIXED_TEXT, D_TEXT, D_NUM)
    outputname = "a_designing_IDcard.jpg"
    IDcard.save(outputname, quality=100, subsampling=0)
    print("check the image~")


if __name__ == "__main__":

    if is_designing:
        design()
    else:
        make_all()

    # Additionally, if elements are considered needing to be adjusted, please
    # refer to <line 16> ~ <line 63>, and switch is_designing on <line 18> to 1
    # to start designing, and don't forget to switch it back to 0 after designing
