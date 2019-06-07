import threading
from abc import ABC, abstractmethod

#internal Definition
THREAD=threading.Thread

class node_base(ABC, threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        ABC.__init__(self)
        print(__class__.__name__,'inherited')

    def _send(self, local=True):
        pass

    def _recv(self, local=True):
        pass

    @abstractmethod
    def run(self):
        pass
