import socket
import threading
import time
import hashlib

IP = socket.gethostbyname(socket.gethostname())
PORT = 4000
ADDR = (IP, PORT)

SIZE = 1024
FORMAT = "utf-8"

def parse_client_request(handle, request):
    split_request = request.split()

    if (split_request[0] == "Balance" and len(split_request) == 2):
        client = int(split_request[1])
        if (1 <= client <= 3):
            return "B", client

    elif (split_request[0] == "Transfer" and len(split_request) == 3):
        recipient = int(split_request[1])
        if (1 <= recipient <= 3):
            amount = int(split_request[2])
            return "T", handle, recipient, amount

    return 0

def handle_client_request(parsed_request):
    if (parsed_request == 0):
        return "Invalid Input"
    
    elif (parsed_request[0] == "B"):
        return "Balance: $TEST"
    
    elif (parsed_request[0] == "T"):
        if (transfer_request != 0):
            return "Success"
        else:
            return "Insufficent Balance"
    
    return "Error Handling Request"

def balance_request():
    return 0

def transfer_request():
    return 1

def client_request_handler(conn, addr, handle):
    print(f"[NEW CONNECTION] {addr} connected {handle}.")

    while True:
        request = conn.recv(SIZE).decode(FORMAT)
        
        # Message Passing Delay
        # time.sleep(3)
        
        print(f"[{addr}] {request}")
        
        parsed_request = parse_client_request(handle, request)
        response = handle_client_request(parsed_request)
        conn.send(response.encode(FORMAT))
        
def client_connection_handler(server):
    while True:
        conn, addr = server.accept()
        client_request_thread = threading.Thread(target=client_request_handler, args=(conn, addr, threading.activeCount() - 1,))
        client_request_thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 2}")
    

def main():
    print("[STARTING] Server is starting...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen(3)
    print(f"[LISTENING] Server is listening on {IP}:{PORT}")
    
    client_connection_thread = threading.Thread(target=client_connection_handler, args=(server,))
    client_connection_thread.start()
     
    while True:
        request = input("> ")
        print(request)
        
if __name__ == "__main__":
    main()