from queue import Queue
import socket
import threading

target = ""  # IP
queue = Queue()
open_ports = []


def portscan(port):
    try:  # Return true if connection can be established at IP and Port
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((target, port))
        return True
    except:  # Return false if connection can be established at IP and Port
        return False


def get_ports(mode):
    if mode == 1:
        for ports in range(1, 1024):
            queue.put(ports)
    elif mode == 2:
        for ports in range(1, 49152):
            queue.put(ports)
    elif mode == 3:
        important_ports = [20, 21, 22, 23, 25, 53, 80, 110, 443]
        for port in important_ports:
            queue.put(port)
    elif mode == 4:
        ports = input("Enter ports separated by a space between each port")
        ports = ports.split()
        ports = list(map(int, ports))
        for port in ports:
            queue.put(port)


def worker():
    while not queue.empty():
        port = queue.get()
        if portscan(port):
            print('Port {} is open' .format(port))
            open_ports.append(port)
        else:
            print('Port {} is not open'.format(port))


def run_scanner(threads, mode):
    get_ports(mode)

    thread_list = []

    for t in range(threads):
        thread = threading.Thread(target=worker)
        thread_list.append(thread)

    for thread in thread_list:
        thread.start()

    for thread in thread_list:
        thread.join()

    print("Open ports are:", open_ports)
