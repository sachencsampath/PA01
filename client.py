import socket
import sys

IP = socket.gethostbyname(socket.gethostname())
PORT = 4000
ADDR = (IP, PORT)

SIZE = 1024
FORMAT = "utf-8"

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    
    while True:
        request = input("> ")

        client.send(request.encode(FORMAT))

        response = client.recv(SIZE).decode(FORMAT)
        print(response)

if __name__ == "__main__":
    main()