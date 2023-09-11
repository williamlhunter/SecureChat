import zmq
import threading
import sys

isServer = False

def error():
    print("Error")
    quit()

context = zmq.Context()
if len(sys.argv) == 1:
    isServer = True
    print("Binding server to port 5555")
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")

elif len(sys.argv) == 2:
    isServer = False
    print("Connecting to server at: " + sys.argv[1])
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://" + sys.argv[1] + ":5555")

if isServer:
    while True:
        try:
            message = socket.recv()
        except:
            error()

        print("them: %s" % message)
        socket.send(b"World")

else:
    for request in range(10):
        print("Sending request %s …" % request)
        socket.send(b"Hello")

        #  Get the reply.
        message = socket.recv()
        print("Received reply %s [ %s ]" % (request, message))
