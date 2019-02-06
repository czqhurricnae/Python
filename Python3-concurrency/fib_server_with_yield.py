from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from collections import deque
from select import select


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
        # print("Before socket accept!")
        # print("tasks", tasks)
        # print("recv_wait", recv_wait)
        yield "Recv", sock
        # print("After socket accept!")
        # print("tasks", tasks)
        # print("recv_wait", recv_wait)
        client, addr = sock.accept()
        print("Connection", addr)
        tasks.append(handle_client(client))

def handle_client(client):
    while True:
        yield "Recv", client
        recv = client.recv(100)
        if not recv:
            break
        result = fib(int(recv))
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
            why, what = next(task)    # Run to the yield
            if why == "Recv":
                recv_wait[what] = task
                # print("In run function line61!", recv_wait)
            elif why == "Send":
                send_wait[what] = task
                # print("In run function line64!", recv_wait)
            else:
                raise RuntimeError
        except StopIteration:
            print("Task Done!")

tasks.append(fib_server(("", 2500)))

run()
