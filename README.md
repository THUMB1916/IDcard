# 批量制作队员证说明文档

2020.5.24 by 内联后勤副紫红


* [安装](#安装)
* [使用方法](#使用方法)
* [其他事项](#其他事项)
    + [检查做好的队员证](#检查做好的队员证)
    + [重新设计](#重新设计)

## 安装
clone或download此项目。除了python3.6之外，还需要以下包：
1. numpy
2. opencv (cv2)
3. pillow (PIL)

## 使用方法
1. 让队员们按照`姓名-性别-声部-院系-学号-入队年份`的命名方式交上 **竖版人像居中** 的照片，格式为`jpg`或`png`，如`xxx-男-打x声部-xxxx学院-201xxxxxxx-201x.jpg`。由于程序可以自适应调整，所以图片尺寸没有严格要求，保持类似于证件照即可。

2. 将已命名好的照片放入`input`文件夹（允许多级目录）
    >然后删除此示例照片。
    <div  align="center">
    <img src="input\军x乐-x-xx声部-xx学院-20xxxxxxxx-20xx.PNG" width = 20% alt="图片名称"/>
    </div>
3. 直接运行代码，在`output`文件夹中收获队员证~
    >然后删除此示例队员证
    <div  align="center">
    <img src="output\军x乐.jpg" width = 40% alt="图片名称"/>
    </div>

## 其他事项
### 检查做好的队员证
1. 观察照片是否合适。有可能出现几个问题：

    | 可能的问题 | 解决方式 | 
    | :-----:| :----: | 
    | 纵横比出问题 | 重新上交照片，或用ps或ppt大致拉回正常纵横比 | 
    | 人脸在照片中占比过小或太偏 | 用微信截图等方式重新构图，保持人像居中 | 
> 程序可以将较“矮胖”的照片按照居中对齐裁剪，将较“高瘦”的照片按照靠上对齐裁剪，然后缩放到307*377，但并没有利用人脸识别来调整，所以面对人脸比例较小的全身照或风景照需要手动重新构图。

2. 观察文字是否合适。有可能出现的问题是：

    | 可能的问题 | 解决方式 | 
    | :-----:| :----: | 
    | 院系名称太长，挡住照片 | 将文件名中的 **电机工程与应用电子技术系** 改为 **电机系** | 

### 重新设计
1. 背景图片。可以用文件夹中自带的`empty_ID.jpg`，也可以在百度网盘中搜索“队员证”利用psd重新制作。

2. 调整文字的字体、字号、位置，照片的位置。将代码第26行的变量`is_designing`的值改为1即可进入设计模式，调整第25~第51行的参数即可调节上述内容。在设计时，会输出字块所占的实际像素数，还会在当前目录下生成名为`a_designing_IDcard.jpg`的样张，可以观察它的效果不断修改参数直到满意为止。然后把`is_designing`的值改回0，重新运行即可。

