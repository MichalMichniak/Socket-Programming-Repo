import time
class PlayerTwo:
    def __init__(self):
        pass


def player_two_process(pipe_output, pipe_input):
    print("player two active")
    for i in range(5):
        time.sleep(0.01)
        pipe_output.send("l")
        receive = pipe_input.recv()
        if receive == "END":
            break
        #print( "2: recived " ,receive)
    print("player two closed")
    pipe_output.send("CONNECTION END")
    pass