import socket

IP = socket.gethostbyname(socket.gethostname())
PORT = 4000
ADDR = (IP, PORT)

SIZE = 1024
FORMAT = "utf-8"

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    print(f"[CONNECTED] Client connected to server at {IP}:{PORT}")

    while True:
        request = input("> ")

        client.send(request.encode(FORMAT))

        response = client.recv(SIZE).decode(FORMAT)
        print(f"[SERVER] {response}")

if __name__ == "__main__":
    main()