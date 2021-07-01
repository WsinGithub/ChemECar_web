from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404, FileResponse  # 文件下载
import json
import time
import socket
import os
import re # 用于生成标准时间字符串


def index(request):
    """获取实验数据文件信息，并渲染主页面"""
    context = get_data_path_context()
    return render(request, 'index.html', context)


def get_data(request):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    # $$$ internal port
    port = 9999
    client.connect((host, port))
    msg_json = {"signal": 3}
    client.send(bytes(json.dumps(msg_json), encoding="utf-8"))
    # $$$ display data size
    display_raw = client.recv(1024 * 1024)
    client.close()
    return HttpResponse(display_raw)


def exp_post(request):
    """开始时实验的文件名初始化;结束实验时"""
    flag = request.POST["flag"]
    flag = int(flag)
    print(flag)
    if flag == 1:
        suffix = request.POST["suffix"]
        filename = time.strftime("%Y%m%d_%H%M%S_", time.localtime()) + suffix
        print(filename)
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = socket.gethostname()
        # $$$ internal port
        port = 9999
        client.connect((host, port))
        msg_json = {"signal": flag, "filename": filename}
        client.send(bytes(json.dumps(msg_json), encoding="utf-8"))
        client.close()
        return HttpResponse(filename)
    if flag == 2:
        # end record
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = socket.gethostname()
        # $$$ internal port
        port = 9999
        client.connect((host, port))
        msg_json = {"signal": flag}
        client.send(bytes(json.dumps(msg_json), encoding="utf-8"))
        client.close()
        return HttpResponse()
    return HttpResponse()


def data_download(request, file_url):
    """文件下载"""
    try:
        response = FileResponse(open(file_url, 'rb'))
        response['content_type'] = "application/octet-stream"
        response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_url)
        return response
    except Exception:
        raise Http404


# 以下为普通函数，非视图(views)函数

def get_data_path_context():
    """返回一个包含文件信息的字典"""
    # 当前工作路径为服务器运行路径
    # 相对路径
    data_relpath = 'data'
    # 绝对路径
    data_abspath = os.path.abspath(data_relpath)
    # 设定路径模式
    # data_path = data_relpath
    data_path = data_abspath

    # 获取文件列表及urls
    file_name_list = os.listdir(data_relpath)
    files = []
    for file_name in file_name_list:
        file_url = os.path.join(data_path, file_name)
        file = {
            # 文件名(file_name)形如：20210629_230804_.csv, 20210629_230804_BZ.csv
            "name": file_name,
            "url": file_url,
            "date": file_name.split('_')[0]+file_name.split('_')[1], # yyyyMMddHHmmss, 做简单排序用
            "note": file_name.split('_')[-1].split('.')[0],
            "format_date": get_format_date(file_name), # yy-yy-MMdd HH:mm:ss, 用于创建JaveScript中的Date对象
        }
        files.append(file)

    files_dict = {
        # 数据结构说明：
        # files为数组，其元素为字典，字典有两对键-值对:
        # [
        #     {"name": file1_name, "url": file1_url},
        #     {"name": file2_name, "url": file2_url},
        #     {"name": file3_name, "url": file3_url},
        #     ...
        # ]
        "files": files,
    }
    
    context = { 
        # 键-值对中的"值"需要为字典，方便django后续转换为JSON使用
        "files_dict" : files_dict,
        }
    return context


def get_format_date(file_name):
    ''' 从文件名中获取标准时间字符串(dateString)，供JaveScript中的Date对象创建使用 '''
    yyyyMMdd = file_name.split('_')[0]
    [yyyy, MMdd] = re.findall(r'.{4}',yyyyMMdd)
    [MM, dd] = re.findall(r'.{2}',MMdd)

    HHmmss = file_name.split('_')[1]
    [HH, mm, ss] = re.findall(r'.{2}',HHmmss)

    format_date= '-'.join([yyyy, MM, dd]) + ' ' + ':'.join([HH, mm, ss])
    return format_date

