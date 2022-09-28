import socket
import threading

HEADER = 64
FORMAT = 'utf-8'
PORT = 5050
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "192.168.20.1"
ADDR = (SERVER, PORT)
WORKING = True
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

def receive_thread(clientt,WORKING):
    while WORKING:
        msg = receive(clientt)
        print(f"[SERVER] {msg}")
        if msg == "end":
            send(DISCONNECT_MESSAGE)
            WORKING=False

def main():
    user_nr = socket.gethostbyname(socket.gethostname())
    send(f"[USER {user_nr}]Conected")#sys.argv[1]
    #cmd_proc = subprocess.Popen(['ls', '-l'], stdout=subprocess.PIPE)
    thread = threading.Thread(target=receive_thread, args=(client,WORKING))
    thread.start()
    while WORKING:
        message = input()
        send(message)
        

if __name__ == "__main__":
    main()
    