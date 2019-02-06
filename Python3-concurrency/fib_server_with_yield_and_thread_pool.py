from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from collections import deque
from select import select
from concurrent.futures import ThreadPoolExecutor as Pool

pool = Pool(4)

tasks = deque()
recv_wait = {}
send_wait = {}

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
        yield "Recv", sock
        client, addr = sock.accept()
        print("Connection", addr)
        tasks.append(handle_client(client))

def handle_client(client):
    while True:
        yield "Recv", client
        recv = client.recv(100)
        if not recv:
            break
        future = pool.submit(fib, int(recv))
        result = future.result()
        response = str(result).encode("ascii") + b"\n"
        yield "Send", client
        client.send(response)
        # print("Closed")


def run():
    while any([tasks, recv_wait, send_wait]):
        while not tasks:
            # Not active tasks to run.
            # Wait of I/O.
            can_recv, can_send, _ = select(recv_wait, send_wait, [])
            for s in can_recv:
                tasks.append(recv_wait.pop(s))
            for s in can_send:
                tasks.append(send_wait.pop(s))
        try:
            task = tasks.popleft()
            why, what = next(task)
            if why == "Recv":
                recv_wait[what] = task
            elif why == "Send":
                send_wait[what] = task
            else:
                return RuntimeError
        except StopIteration:
            print("Task Done!")

tasks.append(fib_server(("", 2500)))
run()
