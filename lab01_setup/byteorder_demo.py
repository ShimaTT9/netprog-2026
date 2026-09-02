# byteorder_demo.py
import sys, socket, struct
value = 0x12345678
print("This machine's native byte order:", sys.byteorder)
print("Big-endian bytes: ", value.to_bytes(4, "big").hex())
print("Little-endian bytes:", value.to_bytes(4, "little").hex())
port = 8080
print(f"Port {port} in network byte order (htons): {socket.htons(port)}")
print("Packed with struct ('!H' = network-order unsigned short):",
struct.pack("!H", port))
