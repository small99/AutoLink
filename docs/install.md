## 安装

1. 安装Python3及以上版本，确保加入环境变量，pip命令可用

2. 从[AutoLink Github项目](https://github.com/small99/AutoLink)下载源码

3. cd到AutoLink目录下，执行以下命令安装AutoLink依赖

> pip install -r requirements.txt

注：在上述依赖安装过程中，如果出现任何问题，请仔细看出错信息，若因为网络超时导致无法安装的，请再次执行上述命令即可

## 本机访问启动

1. 执行以下命令启动AutoLink服务

> python AutoLink.py runserver

2. 访问以下网址，即可

http://127.0.0.1:5000

## 外网访问启动
1. 执行以下命令可外网访问

> python AutoLink.py runserver -h 0.0.0.0 -p 8000
通过

2. 即可通过你的IP地址来访问

http://ip:8000

- -h选项指定为0.0.0.0即为绑定本机ip启动，网络其他用户通过你的ip和-p指定的端口即可访问AutoLink

- -p指定AutoLink服务启动时的端口

## 默认账号

默认账号: AutoLink  

默认密码: 123456

## Selenium浏览器驱动安装

1. [下载地址](https://docs.seleniumhq.org/download/), 最好有vpn，避免被墙

2. 下载selenium webdriver对应的浏览器驱动放在driver目录即可