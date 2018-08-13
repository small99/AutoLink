## 安装与启动

1. 安装Python3版本，确保加入环境变量，pip命令可用

2. 从[AutoLink Github项目](https://github.com/small99/AutoLink)下载源码

3. 执行以下命令安装AutoLink依赖

> pip install -r requirements.txt

4.1 执行以下命令启动AutoLink服务

> python AutoLink.py runserver

4.1.1 访问以下网址，即可

http://127.0.0.1:5000

4.2 执行以下命令可外网访问

> python AutoLink.py runserver -h 0.0.0.0 -p 8000
通过

4.2.1 即可通过你的IP地址来访问

http://ip:8000

注： 
- -h选项指定为0.0.0.0即为绑定本机ip启动，网络其他用户通过你的ip和-p指定的端口即可访问AutoLink

- -p指定AutoLink服务启动时的端口

默认账号: AutoLink
默认密码: 123456