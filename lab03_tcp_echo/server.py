import socket
import threading

HOST = "0.0.0.0"
PORT = 5000

def handle_client(conn, addr):
	print(f"Connected by {addr}")
	with conn:
		while True:
			data = conn.recv(1024)
			if not data:
				break
			conn.sendall(data.decode("utf-8").upper().encode("utf-8"))
		print(f"Connection with {addr} closed")

def main():
	server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	server_sock.bind((HOST, PORT))
	server_sock.listen(1)
	print(f"Echo server listening on {HOST}:{PORT}")

	while True:
		conn, addr = server_sock.accept()
		t = threading.Thread(target=handle_client, args=(conn, addr), daemon=True) 
		t.start()

if __name__ == "__main__":
	main()
