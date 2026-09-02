import socket

def classify_port(port):
	if 0 <= port <= 1023:
		return "Well-Know"
	elif 1024 <= port <= 49151:
		return "Registered"
	else:
		return "Dynamic/Private"

def main():
	host = input("Hostname: ")
	port = int(input("Port: "))
	ip = socket.gethostbyname(host)
	print(f"{host} resolves to {ip}")
	print(f"Port {port} is classified as: {classify_port(port)}")

if __name__ == "__main__":
	main()
