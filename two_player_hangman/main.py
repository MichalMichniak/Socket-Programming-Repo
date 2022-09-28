from concurrent.futures import thread
from threading import Thread,Lock,enumerate
import numpy as np
import random
from multiprocessing import Process, Pipe, parent_process
import queue
import time
import playerone
import playertwo
class Serwer:
    def __init__(self,*args) -> None:
        self.pipe_1 = args[0]
        self.pipe_2 = args[1]
        self.pipe_3 = args[2]
        self.pipe_4 = args[3]
        self.FIFO = queue.Queue(100)
        res = open("dictionary1.txt",'r')
        self.password = res.read().splitlines()[random.randint(0,57561)]
        self.player1_gueses = 0
        self.player2_gueses = 0
        self.pipe_2.send(len(self.password)+1)
        self.pipe_4.send(len(self.password)+1)
        self.loop = True
        pass
    
    def send_message(self,msg_n):
        if msg_n[1] == 1:
            self.player1_gueses += 1
            print(str(1)+";"+msg_n[0]+";"+self.password+";"+str(self.player1_gueses))
            ## msg self.pipe_2
            if len(msg_n[0]) == 1:
                self.pipe_2.send([i for i in range(len(self.password)) if self.password[i] == msg_n[0]])
                ## literka
                pass
            elif msg_n[0] == self.password:
                self.pipe_2.send("END")
                self.pipe_4.send("END")
                print("PLAYER 1 WIN")
                return 0
                pass
            else:
                self.pipe_2.send([])
                pass  
            pass
        else:
            ## msg self.pipe_4
            self.player2_gueses += 1
            print(str(2)+";"+msg_n[0]+";"+self.password+";"+str(self.player2_gueses))
            if len(msg_n[0]) == 1:
                self.pipe_4.send([i for i in range(len(self.password)) if self.password[i] == msg_n[0]])
                ## literka
                pass
            elif msg_n[0] == self.password:
                self.pipe_2.send("END")
                self.pipe_4.send("END")
                print("PLAYER 2 WIN")
                return 0
                pass
            else:
                self.pipe_4.send([])
                pass 
            pass
        pass

    def thread_1(self):
        """adding to queue"""
        print("thread 1 active")
        while self.loop:
            msg = self.pipe_3.recv()
            if msg == "CONNECTION END":
                print(msg + " thread 1")
                break
            #print(msg)
            self.FIFO.put((msg,2))
        pass

    def thread_3(self):
        print("thread 3 active")
        while self.loop:
            msg = self.pipe_1.recv()
            if msg == "CONNECTION END":
                #print(msg + " thread 3")
                break
            #print(msg)
            self.FIFO.put((msg,1))
            pass
        pass

    def thread_2(self):
        print("thread 2 active")
        while self.loop:
            #print('o')
            if not self.FIFO.empty():
                buffor = self.FIFO.get()
                #print(buffor)
                self.send_message(buffor)
                ## do sth
                pass
        pass

    

    def process(self):
        print("serwer process active")
        self.tr1 = Thread(target = self.thread_1)
        self.tr2 = Thread(target = self.thread_2)
        self.tr3 = Thread(target = self.thread_3)
        try:
            self.tr1.start()
            self.tr3.start()
            self.tr2.start()
        except:
            self.loop = False
        
        self.tr1.join()
        self.tr3.join()
        self.loop = False
        self.tr2.join()
        print("serwer closed")   

def serwer_process(*args):
    serwer = Serwer(args[0],args[1],args[2],args[3])
    serwer.process()


class Symulation:
    def __init__(self) -> None:
        pass
    
    def start(self):
        self.parent_one, self.child_one = Pipe()
        self.parent_two, self.child_two = Pipe()
        self.parent_one_sending, self.child_one_sending = Pipe()
        self.parent_two_sending, self.child_two_sending = Pipe()
        self.player_one = Process( target=playerone.player_one_process , args=(self.child_one, self.child_one_sending))
        self.player_two = Process( target=playertwo.player_two_process , args=(self.child_two, self.child_two_sending))
        self.serwer_process = Process( target=serwer_process, args = (self.parent_one,self.parent_one_sending,self.parent_two,self.parent_two_sending,))
        self.serwer_process.start()
        self.player_one.start()
        self.player_two.start()        
        self.end()

    def end(self):
        self.player_one.join()
        self.player_two.join()
        self.serwer_process.join()


def main():
    #print(Serwer().password )
    main = Symulation()
    main.start()
    pass


if __name__ == '__main__':
    main()