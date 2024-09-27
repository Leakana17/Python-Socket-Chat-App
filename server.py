import threading
import socket
import datetime

PORT = 5050
SERVER = "localhost"
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

clients = {}
clients_lock = threading.Lock()


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} Connected")
    client_id = str(addr)
    clients[client_id] = conn

    try:
        connected = True
        while connected:
            msg = conn.recv(1024).decode(FORMAT)
            if not msg:
                break

            if msg == DISCONNECT_MESSAGE:
                connected = False
                break

            else:
                with clients_lock:
                    for cid, c in clients.items():
                        if cid != client_id:
                            c.sendall(f"[{client_id}] {msg}".encode(FORMAT))

    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        with clients_lock:
            clients.pop(client_id, None)

        conn.close()

def listen_commands():
    while True:
        command = input()
        if command.startswith('/bc'):
            try:
                with clients_lock:
                    for cid, conn in clients.items():
                        conn.sendall(f"[Broadcast]: {command.split(' ', 1)[1]}".encode(FORMAT))
                print("Broadcast Successful")
            except Exception as e:
                print(f'Broadcast Failed: {e}')

    

def start():
    print('[SERVER STARTED]!')
    thread = threading.Thread(target=listen_commands)
    thread.start()
    server.listen()
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


start()