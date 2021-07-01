import socket
import json

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 9999
client.connect((host, port))
msg = -1  # 退出指示符

msg_json = {"signal": msg}
r = client.send(bytes(json.dumps(msg_json), encoding="utf-8"))
if msg == 3:
    display_raw = client.recv(1024 * 1024)
    display = json.loads(display_raw.decode('utf-8'))
    print(display)
client.close()

print("record->end")
