# ChemECar_web

该项目是为华东理工大学Chem-E-Car竞赛车队编写的网站。

目前，内置一个应用供控制组使用，其当前(目标)功能为：

- 提供一个API接口，供后续写入实验数据；
- 使用移动设备，操控实验数据记录的启动与停止；
- 从服务器上下载历史实验数据；
- ...

## 目录

- [安装](#安装)
- [使用说明](#使用说明)
- [参考文档](#参考文档)
- [维护者](#维护者)
- [如何贡献](#如何贡献)

## 安装

项目使用Python原生虚拟环境[venv](https://docs.python.org/zh-cn/3/library/venv.html)打包好所需库，[安装Python](https://www.python.org/downloads/)即可使用。

如Python版本过低(早于Python 3.3)没有内置venv库，或需在虚拟环境中安装新的库，请参阅[Installing packages using pip and virtual environments](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/#:~:text=Python%20source%20code.-,Installing%20pip%C2%B6,-pip%20is%20the)获取帮助。

## 使用说明

### 运行服务器

打开命令行(在开始菜单中键入`cmd`)，切换目录到项目父文件夹`ChemECar_web`，形如：

（复制`...\>`后面的内容）

```shell
...\> d:
...\> cd D:\ChemECar_web
```

激活虚拟环境

```shell
...\ChemECar_web\> min_django_env\Scripts\activate.bat
```

运行服务器

```shell
(min_django_env) ...\ChemECar_web\> python oe_site\manage.py runserver
```

至此，即可进入网页 `http://127.0.0.1:8000/app`, 即`http://localhost:8000/app`

## 实验记录

### 数据读取

> 目前使用 record.py 中的 generator 生成虚拟数据，留下接口供后续读取真实数据。

新开一个命令行窗口，进入文件夹`ChemECar_web`，运行子文件夹`oe_site\app`中的`record.py`

```
...\ChemECar_web\> python oe_site\app\record.py
```

[^]: 如果不运行`record.py`，则会出现警告，并无法生成数据图。

此时在文本框中输入数据备注（可选），点击开始按钮即可实时显示实验数据，点击结束按钮则完成数据记录。其他人此时也可进入网页观看数据，但无权控制记录的起止。

如需停止数据记录，请进入文件夹`ChemECar_web`，运行子文件夹`oe_site\app`中的`testclient.py`

```
...\ChemECar_web\> python oe_site\app\testclient.py
```

### 数据下载

傻瓜式操作。

现已加入排序功能。

## 参数设置

$$$ chart refresh interval $$$ oe_site\templates\index.html 浏览器端画图的更新间隔(ms)
$$$ chart update duration $$$ oe_site\static\js\setChart.js 浏览器端画图的速度(ms)
$$$ detect time $$$ oe_sit\app\record.py 检测的间隔时间长度
$$$ display data size $$$ oe_site\app\views.py 传输到浏览器端的用于画图的数据大小
$$$ display time $$$ oe_site\app\record.py 浏览器端显示的时间长度
$$$ internal port $$$ oe_site\app\record.py(1) oe_site\app\record.py(3) 数据记录程序与django后端通信使用的端口
$$$ process interval $$$ oe_site\app\record.py 数据记录程序根据信号执行所有操作后的不响应时间(用于节约性能)
$$$ signal receive interval $$$ oe_site\app\record.py 数据记录程序接收指令后的不响应时间(用于节约性能)

## 参考文档

### Python 

来自Python官方文档——[Python 教程](https://docs.python.org/zh-cn/3/tutorial/index.html)

### 前端(HTML+CSS+JavaScripts)

MDN Web Docs——[Web 入门](https://developer.mozilla.org/zh-CN/docs/Learn/Getting_started_with_the_web)（来自[@王世强](https://github.com/WsinGithub)的强烈安利！MDN本土化团队tql！）

无需搭建本地环境的在线web调试工具——[JS Bin](https://jsbin.com/)
### Django

采用Django3.2作为框架——[官方文档](https://docs.djangoproject.com/zh-hans/3.2/)

### 网络通信

Socket（套接字是什么辣鸡翻译？）——[套接字编程指南](https://docs.python.org/zh-cn/3/howto/sockets.html#socket-howto)，[Socket原理讲解](https://blog.csdn.net/pashanhu6402/article/details/96428887)

### 涉及到的其他相关标准库

time，时间的访问和转换——[time](https://docs.python.org/zh-cn/3/library/time.html?highlight=time#module-time)

...

## 维护者

[@蒋天诚](https://github.com/Bat-Chatillon)

[@王世强](https://github.com/WsinGithub)

## 如何贡献

- [提一个 Issue](https://github.com/WsinGithub/ChemECar_web/issues/new) 或者提交一个 Pull Request。
- 加入[技术支持群](https://qm.qq.com/cgi-bin/qm/qr?k=NcIw1kOXJUlRvF76If_RyiWnIROqrGuH&jump_from=webapi)与我们讨论！

