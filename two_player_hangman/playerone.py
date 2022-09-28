import time
import numpy as np
import pandas as pd
class PlayerOne:
    def __init__(self,pipe_output, pipe_input):
        self.pipe_output = pipe_output
        self.pipe_input = pipe_input
        self.letters = [i for i in "abcdefghijklmnopqrstuvwxyz"]
        #self.data = pd.read_csv('dictionary1.txt', sep=" ", header=None)
        #self.data.columns = ["a"]
        
        pass
    def send(self, message):
        pass
    def receive(self, message):
        pass
    
    def filter(self, fill , char):
        data_filter = self.data['a'].str[fill[0]] == char
        for i in fill[1:]:
            data_filter = data_filter & (self.data['a'].str[i] == char)
        self.data = self.data[data_filter]
        pass

    def filter_without(self,char):
        self.data = self.data[~(self.data['a'].str.contains(char, regex=False))]
        pass

    def pick_next_letter(self):## można dodać usprawnienie wycinając ostatnie litery których statystycznie jest mało
        if self.data['a'].size<6: ## sterować tym
            #print("poniżej 6")
            siz = self.data['a'].size
            char = '_'
            count = 0
            for i in self.letters:
                t = len(self.data[self.data['a'].str.contains(i,regex=False)])
                if count < t and t < siz//2 + 1:
                    count = t 
                    char = i
            pass
        char = '_'
        count = 0
        for i in self.letters:
            t = len(self.data[self.data['a'].str.contains(i,regex=False)])
            if count < t:
                count = t 
                char = i
        return char


    def start(self):
        self.word_lenght = self.pipe_input.recv()
        self.data = pd.read_csv('player1data/data'+str(self.word_lenght-1)+".csv", sep=",")
        self.pipe_output.send('e') ## this is the most probable value
        t = self.pipe_input.recv()
        char = 'e'
        counter = 0
        
        if self.data['a'].size == 1:
                self.pipe_output.send(self.data['a'].values[0])
                t = self.pipe_input.recv()
                if t == 'END':
                    return 0
        while t != 'END':
            self.letters.remove(char)
            if t == []:
                self.filter_without(char)
                pass
            else:
                self.filter(t,char)
            if self.data['a'].size == 1:
                self.pipe_output.send(self.data['a'].values[0])
                t = self.pipe_input.recv()
                if t == 'END':
                    break
            if self.data['a'].size == 2:
                self.pipe_output.send(self.data['a'].values[0])
                t = self.pipe_input.recv()
                if t == 'END':
                    break
                self.pipe_output.send(self.data['a'].values[1])
                t = self.pipe_input.recv()
                if t == 'END':
                    break
            char = self.pick_next_letter()
            self.pipe_output.send(char)
            t = self.pipe_input.recv()
        pass

def player_one_process(pipe_output, pipe_input):
    print("player one active")
    p = PlayerOne(pipe_output,pipe_input)
    p.start()
    print("player one closed")
    pipe_output.send("CONNECTION END")
    pass

