import socket
import threading

HEADER = 64
FORMAT = 'utf-8'
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
#print(socket.gethostbyname(socket.gethostname()))
ADDR = (SERVER, PORT)
DISCONNECT_MESSAGE = "!DISCONNECT"


class Server:
    def __init__(self):
        print("[SERVER] starting...")
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(ADDR)
        self.client_lst = []
        pass

    def receive(self, conn : socket.socket, addr):
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            return msg

    def send(self, msg, conn : socket.socket, addr):
        message = msg.encode(FORMAT)
        msg_lenght = len(message)
        send_length = str(msg_lenght).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        conn.send(send_length)
        conn.send(message)

    def direct_send(self, conn : socket.socket, addr, *args):
        print(f"[MULTICAST][{addr}]")
        msg = ''
        for i in args[0]:
            print(i)
            msg+=i
        self.send(msg, conn, addr)

    def multicast_send(self, *args):
        print("[MULTICAST]")
        for i in self.client_lst:
            thread = threading.Thread(target=self.direct_send, args=(i[0], i[1], args))
            thread.start()
            thread.join()
        pass
    
    def handle_clinet(self, conn : socket.socket, addr):
        print(f"[SERVER][NEW CONNECTION] {addr} connected.")
        connected = True
        while connected:
            msg = self.receive(conn, addr)
            if msg == DISCONNECT_MESSAGE:
                connected = False
                break
            print(f"[{addr}] {msg}")
            msg = str(f"[{addr}] {msg}")
            thread = threading.Thread(target=self.multicast_send, args=(msg))
            thread.start()
            """msg = input()
            self.send(msg, conn, addr)"""
        pass
    
    def start(self):
        self.client_lst = []
        self.server.listen()
        print(f"[SERVER] listening at {socket.gethostbyname(socket.gethostname())}")
        while True:
            conn, addr = self.server.accept()
            thread = threading.Thread(target=self.handle_clinet, args=(conn, addr))
            thread.start()#(conn, addr)
            self.client_lst.append((conn, addr))
            print(f"[SERVER] active connections: {threading.active_count()-1}")
    pass





if __name__ == '__main__':
    server = Server()
    server.start()