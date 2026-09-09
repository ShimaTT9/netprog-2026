import socket

HOST = "127.0.0.1"
PORT = 5000

def main():
	client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		client_sock.connect((HOST, PORT))
	except ConnectionRefusedError:
		print("Could not reach server - is it running?")
		return
	print("Connected to server. Type a message and press Enter ('quit' to exit).")
	try:
		while True:
			message = input("> ")
			if message.lower() == "quit":
				break

			client_sock.sendall(message.encode('utf-8'))
			reply = client_sock.recv(1024)
			print(f"Echoed back: {reply.decode('utf-8')}")

	except KeyboardInterrupt:
		print("\nDisconnected.")

	client_sock.close()

if __name__ == "__main__":
	main()
