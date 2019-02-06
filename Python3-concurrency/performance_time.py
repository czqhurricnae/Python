from socket import *
import time

sock = socket(AF_INET, SOCK_STREAM)
sock.connect(("localhost", 2500))

while True:
    start = time.time()
    sock.send(b"30")
    response = sock.recv(100)
    end = time.time()
    print(end - start)
