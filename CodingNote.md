# 目录
- [目录](#目录)
- [本地conda虚拟环境介绍](#本地conda虚拟环境介绍)
  - [base](#base)
  - [godplease](#godplease)
  - [newland](#newland)
- [常见问题记事本](#常见问题记事本)
  - [1. ipynb如何连接刚配好的虚拟环境？](#1-ipynb如何连接刚配好的虚拟环境)
  - [2. vscode如何连接新的python/ipynb环境？](#2-vscode如何连接新的pythonipynb环境)
  - [3. 安装cvxpy](#3-安装cvxpy)
    - [3.1 ```pip install cvxpy```报错](#31-pip-install-cvxpy报错)
    - [3.2 安装成功后报错IDE找不到numpy](#32-安装成功后报错ide找不到numpy)
    - [3.3 新环境安装ipykernel 有奇怪的报错](#33-新环境安装ipykernel-有奇怪的报错)
  - [4. pip install的时候千万别开VPN！！！会变得不幸！！](#4-pip-install的时候千万别开vpn会变得不幸)
  - [5. vscode 配置 cpp](#5-vscode-配置-cpp)
  - [6. 安装GPU版本的PyTorch](#6-安装gpu版本的pytorch)

# 本地conda虚拟环境介绍

| environment | base  | godplease | newland | cvxpy |torch
| :---------: | :---: | :-------: | :-----: | :---: |:---:|
|   python    |   -   |    3.7    |   3.9   |  3.7  |3.8|
|     pip     |   y   |     y     |    y    |   y   |y
|   jupyter   |   n   |     y     |    y    |   n   |n
|    mxnet    |   n   |     y     |    n    |   n   |n
|    cvxpy    |   n   |     n     |    n    |   y   |n
|    numpy    |   y   |   1.21    |  1.21   | 1.21  |1.21
|pytorch|1.9.0+cpu|n | 1.10.0+cpu |n|**1.10.2+gpu**|

*表1：能力攻略一览表*
## base

>本地根环境,目前属于荒废状态.

---
## godplease

>求神拜佛迷信之作。
>彻底荒废，近期删除
>主要原因是mxnet的gpu版本不支持cuda11.0以上，所以没法用


- python3.7
  
- conda install 一般都灵，尤其是别的环境遇到轮子问题时。
![wheels.png](https://i.loli.net/2021/10/31/2SMn6j3JRWvkgrq.png)
"wheels building error"

- **cvxpy** used in Lecture *Convex Optimation*
- **mxnet** used to learn machine learning by *Li Mu*

---
## newland
>环境如其名，所有的包都尽量最新。


# 常见问题记事本
>*幸运的人的幸运是相似的，不幸的人各有各的不幸。*
*By Moss Chen*


## 1. ipynb如何连接刚配好的虚拟环境？
  - conda建立并激活虚拟环境（python3.7
  - ->安装插件nb_conda
  - ->conda install ipykernel
  - ->python -m ipykernel install --user --name godplease --display-name "godplease"
  - ->打开jupyter对已有ipynb文件切换内核到虚拟环境godplease

## 2. vscode如何连接新的python/ipynb环境？
  - ```ctrl+shift+p``` 进入设置
  - ->Python：Select Interpreter

## 3. 安装cvxpy
（握拳...)

### 3.1 ```pip install cvxpy```报错
```ERROR: Failed building wheel for scs```

- 报错缺少几个包如ecos scs，从非官方渠道下载轮子文件。参见[非官方扩展包](https://www.pythonf.cn/read/107961)
      
  *tips. 注意下载对应python版本的包，按计算机0处理位数。*

  e.g. ecos-2.0.7.post1-cp37-cp37m-win_amd64.whl 用于python37与win64

- 激活虚拟环境，在pkgs位置使用cmd命令```pip install filename.whl```

    
### 3.2 安装成功后报错IDE找不到numpy
  ```RuntimeError: module compiled against API version 0xe but this version of numpy is 0xd```
    
- 需要更新numpy版本，使用命令```(base) C:\Users\Administrator>pip install numpy --upgrade -i https://pypi.douban.com/simple --use-feature=2020-resolver```
- 或者uninstall & install numpy

- *pip安装特定版本的包的指令*：
  - ```pip install numpy==1.18.8```
  - ```conda install matplotlib=1.4.3```

### 3.3 新环境安装ipykernel 有奇怪的报错
```ImportError: no module named win32api```

- 解决方法是```pip install pypiwin32```
   
## 4. pip install的时候千万别开VPN！！！会变得不幸！！

## 5. vscode 配置 cpp
1. 安装拓展：c++ Extension
2. 安装mingw：这里使用msys2
```
  C:\Users\72310>g++ --version
  g++ (Rev5, Built by MSYS2 project) 10.3.0
  Copyright (C) 2020 Free Software Foundation, Inc.
  This is free software; see the source for copying conditions.  There is NO
  warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

  C:\Users\72310>gdb --version
GNU gdb (GDB) 10.2
Copyright (C) 2021 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
```
3. 添加bin到环境变量：```D:\CodeWorld\VS_Code\MSYS2\mingw64\bin```
4. 进行测试
![image.png](https://s2.loli.net/2022/02/06/iNvsuRkKeE4dl7G.png)
- 新建cpp文件输入代码
- 使用``` ctrl+shift+B```，选择```MSYS2\mingw64\g++```作为编译器，生成exe文件（cpp是编译性语言！）
- 在终端里使用```.\helloworld```运行该exe文件

5. debug

## 6. 安装GPU版本的PyTorch
>主要使用目的是安装GPU版本的PyTorch

>配了一个寒假最终被B站攻略指点迷津，学习网站还得看B站！激动！

参考：[B站攻略](https://www.bilibili.com/video/BV1Jg411c72R?from=search&seid=6028056825518150730&spm_id_from=333.337.0.0)
1. 安装CUDA与CuDNN
2. 测试
```C:\Users\72310>cd C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v10.2\bin

C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v10.2\bin>nvcc -V
nvcc: NVIDIA (R) Cuda compiler driver
Copyright (c) 2005-2019 NVIDIA Corporation
Built on Wed_Oct_23_19:32:27_Pacific_Daylight_Time_2019
Cuda compilation tools, release 10.2, V10.2.89
```
```
C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v10.2\extras\demo_suite>bandwidthTest.exe
[CUDA Bandwidth Test] - Starting...
Running on...

 Device 0: GeForce RTX 2060 with Max-Q Design
 Quick Mode

 Host to Device Bandwidth, 1 Device(s)
 PINNED Memory Transfers
   Transfer Size (Bytes)        Bandwidth(MB/s)
   33554432                     6116.2

 Device to Host Bandwidth, 1 Device(s)
 PINNED Memory Transfers
   Transfer Size (Bytes)        Bandwidth(MB/s)
   33554432                     6271.5

 Device to Device Bandwidth, 1 Device(s)
 PINNED Memory Transfers
   Transfer Size (Bytes)        Bandwidth(MB/s)
   33554432                     150553.9

Result = PASS

NOTE: The CUDA Samples are not meant for performance measurements. Results may vary when GPU Boost is enabled.
```

最终测试：
```python
import torch
print(format(torch.__version__))
print(torch.cuda.is_available())
```
输出：
```
1.10.2
True
```
至此，完结！！！历时2h。