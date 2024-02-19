## 介绍

ImgWebp是一个简单的webp转换工具，基于[libwebp包](https://developers.google.cn/speed/webp?hl=sv)，可以将图片转换为webp格式，也可以将webp转换为图片。

## 功能：

- 封装libwebp的命令为界面操作 

## 安装使用：

- 安装：

  - 第一步：先使用`pip install ImgWebp`命令安装ImgWebp。
  - 第二步：使用`imgc download`命令下载安装libwebp包。
  
- 使用：

  - `imgc` 查看命令
  ![imgc查看命令](./doc/01.webp)
  
  - `imgc download` 下载libwebp包
  ![download操作界面](./doc/02.webp)
  
  - `imgc version` 查看libwebp版本
  
  - `imgc cwebp` 将png、jpeg、jpg、tiff图片转换为webp图片
  ![cwebp操作界面](./doc/03.webp)
  
  - `imgc dwebp` 将webp图片转换为png、pam、ppm、pgm图片
  ![dwebp操作界面](./doc/04.webp)
  
  - `imgc gif2webp` 将动画gif图片转换为动画webp图片
  ![gif2webp操作界面](./doc/05.webp)
  
  - `imgc img2webp` 将批量的PNG、JPEG、TIFF、WebP图片转换为动画webp图片
  ![img2webp操作界面](./doc/06.webp)
