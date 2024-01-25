from time import *
from threading import Thread

def red():
    while True:
        print('Red On')
        sleep(1)
        print('Red Off')
        sleep(1)

def yellow():
    while True:
        print('........Yellow On')
        sleep(2)
        print('........Yellow Off')
        sleep(2)

def green():
    while True:
        print('................Green On')
        sleep(3)
        print('................Green Off')
        sleep(3)

redThread=Thread(target=red)      
yellowThread=Thread(target=yellow)   
greenThread=Thread(target=green) 

redThread.daemon=True
yellowThread.daemon=True
greenThread.daemon=True

redThread.start()
yellowThread.start()
greenThread.start()

while True:
    pass