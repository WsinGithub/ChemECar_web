import json
import queue
import socket
import threading
import time


class generator:
    """生成虚拟数据"""

    def __init__(self):
        self.timestamp = time.time()

    def get_data(self):
        time_period = time.time() - self.timestamp
        virtual_data = int(time_period) % 10
        return [time_period, virtual_data]


print("注意：当前使用generator生成虚拟数据！")  # 后续删除
print("如需停止，请运行testclient.py")  # msg = -1
print("recording...")

control_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
# $$$ internal port
port = 9999
control_server.bind((host, port))
control_server.listen(2)

signal = 2
msg = {}
g = generator()
# $$$ display time
display_dt = 5
# $$$ detect time
detect_dt = 0.1
q = queue.Queue(maxsize=0)  # 0 means inf
clientsocket = []
filename = ''


def listen():
    global control_server
    global signal
    global msg
    global clientsocket
    global filename
    while True:
        clientsocket, addr = control_server.accept()
        msg_raw = clientsocket.recv(1024)
        msg = json.loads(msg_raw.decode('utf-8'))
        signal_next = msg.get("signal")
        signal_next = int(signal_next)
        if signal_next == 3 and signal != 1:
            # 请求数据时不处于记录状态
            clientsocket.send(bytes(json.dumps({"record_on": False}), encoding="utf-8"))
            signal_next = 2
        signal = signal_next
        if signal == 1:
            g.timestamp = time.time()
            filename = msg.get("filename")
        # -1 quit
        #  1 start record
        #  2 end record (default state)
        #  3 get data
        if signal == -1:
            break
        # $$$ signal receive interval
        time.sleep(0.2)


def record():
    global signal
    global msg
    global g
    global q
    global display_dt
    global detect_dt
    global clientsocket
    global filename
    while True:
        if signal == -1:
            break
        if signal == 1:
            with open("../../data/" + filename + '.csv', 'a+') as f:
                [t, d] = g.get_data()
                f.write(str(t))
                f.write(',')
                f.write(str(d))
                f.write('\n')
            q.put([t, d])
            time.sleep(detect_dt)
        if signal == 2:
            while not q.empty():
                q.get()
        if signal == 3:
            with open("../../data/" + filename + '.csv', 'a+') as f:
                [t, d] = g.get_data()
                f.write(str(t))
                f.write(',')
                f.write(str(d))
                f.write('\n')
            q.put([t, d])
            display_msg = []
            while not q.empty():
                temp = q.get()
                if temp[0] >= t - display_dt:
                    display_msg.append(temp)
            for item in display_msg:
                q.put(item)
            clientsocket.send(bytes(json.dumps({"record_on": True, "data": display_msg}), encoding="utf-8"))
            time.sleep(detect_dt)
            signal = 1
        # $$$ process interval
        time.sleep(0.001)


thread_listen = threading.Thread(target=listen, args=())
thread_record = threading.Thread(target=record, args=())

thread_listen.start()
thread_record.start()

thread_listen.join()
thread_record.join()
print("end")
