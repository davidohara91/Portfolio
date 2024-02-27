from threading import Thread
import time

def func1():
    for i in range(10):
        print ("T1: ",i)
        time.sleep(1)

def func2():
    for i in range(5):
        print ("T2: ",i)
        time.sleep(1)

thread1 = Thread(target = func1)        
thread2 = Thread(target = func2)        

thread1.start()
thread2.start()