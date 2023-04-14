import socket
import threading
from hashlib import sha256

IP = socket.gethostbyname(socket.gethostname())
PORT = 4000
ADDR = (IP, PORT)

SIZE = 1024
FORMAT = "utf-8"

Blockchain = []

class Block:
    def __init__(self, sender = None, receiver = None, amount = None, hash = None):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.hash = hash
        self.nonce = None
        
    def __str__(self):
        return "(P{sender}, P{receiver}, ${amount}, {hash})".format(sender = self.sender, receiver = self.receiver, amount = self.amount, hash = self.hash)
    
    def __repr__(self):
        return str(self)
    
    def get_transaction(self):
        return "P{sender}P{receiver}${amount}".format(sender = self.sender, receiver = self.receiver, amount = self.amount)

def parse_client_request(handle, request):
    split_request = request.split()
    
    if (request == "Exit"):
        return "E"
    
    elif (len(split_request) == 2 and split_request[0] == "Balance"):
        if (len(split_request[1]) == 2 and split_request[1].startswith("P") and split_request[1][1].isdigit()):
            client = int(split_request[1][1])
            if (1 <= client <= 3):
                return "B", client

    elif (len(split_request) == 3 and split_request[0] == "Transfer"):
        if (len(split_request[1]) == 2 and split_request[1].startswith("P") and split_request[1][1].isdigit()):
            receiver = int(split_request[1][1])
            if (1 <= receiver <= 3):
                if (len(split_request[2]) >= 2 and split_request[2].startswith("$") and split_request[2][1:].isdigit()):
                    amount = int(split_request[2][1:])
                    return "T", handle, receiver, amount
    elif (len(split_request) == 2 and split_request[0] == "Wait" and split_request[1].isdigit()):
        return "W", split_request[1]
    return 0

def handle_client_request(parsed_request):
    if not parsed_request:
        return "Invalid Input"
    
    command = parsed_request[0]
    
    if (command == "E"):
        return "Exit"
    
    elif command == "B":
        return f"${balance_request(parsed_request[1])}"
    
    elif command == "T":
        if transfer_request(*parsed_request[1:]) != 0:
            return "Success"
        else:
            return "Insufficient Balance"
    
    elif command == "W":
        return str(parsed_request[1])
    
    return "Error Handling Request"

def balance_request(client):
    balance = 10
    for block in Blockchain:
        if (block.sender == client):
            balance -= block.amount 
        
        if (block.receiver == client):
            balance += block.amount
            
    return balance
            

def transfer_request(sender, receiver, amount):
    if (balance_request(sender) >= amount):
        if (Blockchain):    
            previous_block = Blockchain[-1]
            hash = compute_hash(previous_block.hash, previous_block.get_transaction(), previous_block.nonce)
        else:
            hash = "".zfill(256)

        block = Block(sender = sender, receiver = receiver, amount = amount, hash = hash)
        
        nonce = 0
        while (compute_hash(hash, block.get_transaction(), nonce)[:2] != "00"):
            nonce += 1
        block.nonce = nonce
        
        Blockchain.append(block)    
        return 1
    else:
        return 0
    
def compute_hash(hash, transaction, nonce):
    return bin(int(sha256((hash + transaction + str(nonce)).encode('utf-8')).hexdigest(), 16))[2:].zfill(256)

def client_request_handler(conn, addr, handle):
    while True:
        request = conn.recv(SIZE).decode(FORMAT)
        parsed_request = parse_client_request(handle, request)
        response = handle_client_request(parsed_request)
        conn.send(response.encode(FORMAT))
        
        if(response == "Exit"):
            return
        
def client_connection_handler(server):
    while True:
        conn, addr = server.accept()
        client_request_thread = threading.Thread(target=client_request_handler, args=(conn, addr, threading.activeCount() - 1,))
        client_request_thread.start()
        
        
        
def handle_server_request(request):
    if (request == "Blockchain"):
        return Blockchain
    elif (request == "Balance"):
        return f"P1: ${balance_request(1)}, P2: ${balance_request(2)}, P3: ${balance_request(3)}"
    return "Invalid Input"

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen(3)
    
    client_connection_thread = threading.Thread(target=client_connection_handler, args=(server,))
    client_connection_thread.start()
     
    while True:
        request = input("> ")
        response = handle_server_request(request)
        print(response)
        
if __name__ == "__main__":
    main()