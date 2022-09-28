import socket
import sys
import threading
import os
import subprocess

HEADER = 64
FORMAT = 'utf-8'
PORT = 5050
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "192.168.0.209"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_lenght = len(message)
    send_length = str(msg_lenght).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

def receive(client):
    msg_length = client.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length)
        msg = client.recv(msg_length).decode(FORMAT)
        return msg

def main():
    user_nr = socket.gethostbyname(socket.gethostname())
    send(f"[USER {user_nr}]Conected")#sys.argv[1]
    #cmd_proc = subprocess.Popen(['ls', '-l'], stdout=subprocess.PIPE)
    while True:
        msg = receive(client)
        print(f"[SERVER] {msg}")
        if msg == "end":
            send(DISCONNECT_MESSAGE)
            break
        
        message = "TO DO:"
        send(message)
        

if __name__ == "__main__":
    main()
    