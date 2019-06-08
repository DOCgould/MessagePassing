
import threading
from communicationUtils import network
from communicationUtils import local
from abc import ABC, abstractmethod


class node_base(ABC, threading.Thread):
    def __init__(self, volatile_memory, ip_route):
        threading.Thread.__init__(self)
        ABC.__init__(self)
        print(__class__.__name__,'inherited')

        self._publisher=network.publisher(ip_route)
        self._subscriber=network.subscriber(ip_route)

        self._reader=local.reader(volatile_memory)
        self._writer=local.writer(volatile_memory)

    def _send(self, msg, local_address, foreign_address=None):
        '''
            Sends your message to the address(s) provided, either foreign local, or both

            :param byte msg: the message you are sending, could be a byte string
            :param str local_address: a unique key to write to the local volatile_memory
            :param tuple foreign_address: a tuple containing an ip_address and port, pair
            :rtype: int
            :returns: 0 on sucess 1 on error, errors are logged to outputbuffer
        '''

        if foreign_address:
            self._publisher.publish(foreign_address, msg)

        self._writer.write(address=local_address, msg)

        return 0;

    def _recv(self, address, local=True):
        '''
            Gets your message from the addresses provided, either local or foreign
        '''
    if not local:
        return self._subscriber.subscribe(address)
    else:
        return self._reader.read(address)

    @abstractmethod
    def run(self):
        pass

if __name__=='__main__':
    import time

    class PrintNode(node_base):
        def __init__(self, IP, MEM):
            node_base__init__(self, IP, MEM)
            self._memory = IP
            self._ip_route = MEM
            self.MSG='uninitialized'
            self.baud=.128

        def set_message(message):
            self.MSG=message
        def set_baudrate(baudrate):
            self.baud=baudrate

        def run(self):
            start_time = time.time
            while True:
                if (time.time - start_time) >= self.baud:
                    self._send('Encrypted_dat', msg=self.MSG)
                    print(self._recv('Encrypted_dat')) # Local True By Default
                    start_time=time.time
                else:
                    time.sleep(0)
