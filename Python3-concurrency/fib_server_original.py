from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from threading import Thread


def fib(n):
    if n <= 2:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)

def fib_server(address):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(5)
    while True:
        client, addr = sock.accept()
        print("Connection", addr)
        Thread(target=handle_client, args=(client,)).start()

def handle_client(client):
    while True:
        recv = client.recv(100)
        if not recv:
            break
        result = fib(int(recv))
        response = str(result).encode("ascii") + b"\n"
        client.send(response)
    print("Closed")


fib_server(("", 2500))
