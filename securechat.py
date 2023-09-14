import zmq
from threading import Thread
import sys

isServer = False

def sub_routine(socket):
    while True:
        message = socket.recv().decode()
        print("them> ", message)

context = zmq.Context()
pub = context.socket(zmq.PUB)
sub = context.socket(zmq.SUB)

#Are we running as a server?
if len(sys.argv) == 1:
    pub.bind("tcp://*:5555")
    sub.bind("tcp://*:5556")
else:
    pub.connect("tcp://" + sys.argv[1] + ":5556")
    sub.connect("tcp://" + sys.argv[1] + ":5555")

sub.setsockopt_string(zmq.SUBSCRIBE, "")

subber = Thread(target=sub_routine, args=[sub])
subber.start()

while True:
    message = input("> ")
    pub.send(message.encode())

"""
if isServer:
    while True:
        message = input("> ")
        pub.send(message.encode())
        message = sub.recv().decode()
        print("them> ", message)

else:
    while True:
        message = sub.recv().decode()
        print("them> ", message)
        message = input("> ")
        pub.send(message.encode())
"""


