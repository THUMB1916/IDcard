# 批量制作队员证说明文档

2020.5.24 by 内联后勤副紫红

2021.1.09 by 退休的紫红，去掉cv2和numpy依赖


- [批量制作队员证说明文档](#批量制作队员证说明文档)
  - [安装](#安装)
  - [使用方法](#使用方法)
  - [其他事项](#其他事项)
    - [检查做好的队员证](#检查做好的队员证)
    - [重新设计](#重新设计)
    - [其他问题](#其他问题)

## 安装

本程序仅在windows环境下测试，mac不保证能运行（因为似乎涉及到了系统字体，字体比较容易出问题 :(

1. `git clone https://github.com/THUMB1916/IDcard.git` 或 Download Zip
2. `pip install pillow`
> 注：不能使用`conda install pillow`，会报错。好在conda下也可以用pip :)

## 使用方法
1. 让队员们按照`姓名-性别-声部-院系-学号-入队年份`的命名方式交上 **竖版人像居中** 的类似证件照的照片，如`xxx-男-打x声部-xxxx学院-201xxxxxxx-201x.jpg`。尺寸没有严格要求，307\*377或类似的纵横比即可。

    > 一个可能的带有照片要求通知的文案：
    >  
    > 
    > ……开头略……为大家制作队员证啦，请大家在ddl前将自己的个人照片发送到xxxx@xxx.com邮箱即可~
    > 
    > 要求：
    > 
    > 1. 照片请命名为【姓名-性别-声部-院系-学号-入队年份】
    > 2. 风格不限，只要是自己满意的【竖版正脸】大头照、证件照、生活照都可以\~不过需要适当裁剪照片，以使自己占据照片的主体
    > 3. 尺寸以【307\*377】(宽*高)像素为佳，只要保持近似的纵横比即可~
    > 
    > ……结尾略……


2. 检查收到的照片命名是否准确，整理好后统一放入`input`文件夹（允许多级目录）
    <div  align="center">
    <img src="input\军x乐-x-xx声部-xx学院-20xxxxxxxx-20xx.PNG" width = 20% alt="图片名称"/>
    </div>
3. 直接运行代码：`python make_ID.py`

4. 在`output`文件夹中收获队员证~
    <div  align="center">
    <img src="output\军x乐.jpg" width = 40% alt="图片名称"/>
    </div>

## 其他事项
### 检查做好的队员证
1. 观察照片是否合适。有可能出现几个问题：

    |           可能的问题           |                       解决方式                        |
    | :----------------------------: | :---------------------------------------------------: |
    | 队员提交的照片本身纵横比有问题 | 需要让队员重新提交照片，或用ps或ppt大致拉回正常纵横比 |
    |   人脸在照片中占比过小或太偏   |    用微信截图或ps裁剪等方式重新构图，保持人像居中     |
> 程序可以将较“矮胖”的照片按照居中对齐裁剪，将较“高瘦”的照片按照靠上对齐裁剪，然后缩放到307*377，但并没有利用人脸识别来调整，所以面对人脸比例较小的全身照或风景照需要手动重新构图。

2. 观察文字是否合适。有可能出现的问题是：

    |       可能的问题       |                           解决方式                            |
    | :--------------------: | :-----------------------------------------------------------: |
    | 院系名称太长，挡住照片 | 将**文件名**中的 **电机工程与应用电子技术系** 改为 **电机系** |
> 这是已知的名字最长的系，且恰好长了一个字= =
> 
> 类似的，计算机科学与技术系 也可以简称 计算机系，等等。

### 重新设计
1. 修改背景图片。默认用文件夹中自带的`empty_ID.jpg`，也可以在百度网盘中搜索“队员证”利用psd重新制作。

2. 调整文字的字体、字号、位置、颜色，照片的位置。将代码第18行的变量`is_designing`的值改为1即可进入设计模式，调整第16~第63行的参数即可调节上述内容。在设计时，会输出字块所占的实际像素数，还会在当前目录下生成名为`a_designing_IDcard.jpg`的样张，可以观察它的效果不断修改参数直到满意为止。然后把`is_designing`的值改回0，重新运行即可。

### 其他问题
如果程序报错或者使用中遇到问题等等，欢迎直接来问我~