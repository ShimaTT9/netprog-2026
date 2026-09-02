# connect_demo.py
import socket, time

client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_sock.settimeout(1)
client_sock.connect(("192.0.2.1", 80))
print("Connected:", client_sock.getpeername())
time.sleep(5)
client_sock.close()
