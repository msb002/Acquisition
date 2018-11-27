import threading
import time

running = 1

class MyThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.var = 0

    def run(self):
        while(running):
            self.var = self.var +1
            time.sleep(1)      
            self.var = self.var +1                                # Pretend to work for a second

                           # Four times...
mythread = MyThread()  # ...Instantiate a thread and pass a unique ID to it
mythread.start()                                   # ...Start the thread


# for i in range(10):
#     print(mythread.var)
#     time.sleep(0.5)

# running = 0