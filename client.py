import socket
import sys
import time

IP = socket.gethostbyname(socket.gethostname())
PORT = 4000
ADDR = (IP, PORT)

SIZE = 1024
FORMAT = "utf-8"

def main():
    time.sleep(1)
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    
    while True:
        request = input("> ")
        
        client.send(request.encode(FORMAT))

        response = client.recv(SIZE).decode(FORMAT)
        if(response == "Exit"):
            client.close()
            sys.exit()
        elif(response.isdigit()):
            time.sleep(int(response))
        else:
            print(response)

if __name__ == "__main__":
    main()