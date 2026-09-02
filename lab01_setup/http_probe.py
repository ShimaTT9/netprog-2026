# http_probe.py
import socket
HOST = "example.com"
PORT = 80

request = (
f"GET / HTTP/1.1\r\n"
f"Host: {HOST}\r\n"
f"Connection: close\r\n\r\n"
)
# TODO 1: create a TCP socket and connect() it to (HOST, PORT)
client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_sock.connect((HOST, PORT))

# TODO 2: send request.encode("utf-8") using sendall()
client_sock.sendall(request.encode("utf-8"))

response = b""
while True:
	chunk = client_sock.recv(4096)
	if not chunk:
		break
	response += chunk

print(response.decode("utf-8", errors="replace"))
client_sock.close()
