import socket
import time
import datetime
import threading

PORT = 5050
SERVER = "localhost"
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"


def connect():
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(ADDR)
        return client
    except Exception as e:
        print("Error: ",e)


def send(client, msg):
    message = msg.encode(FORMAT)
    client.send(message)


def receive_messages(client):
    while True:
        try:
            msg = client.recv(1024).decode(FORMAT)
            if msg:
                print(f"\n[{datetime.datetime.now().strftime('%H:%M')}] {msg}" )
            else:
                break
        except Exception as e:
            print(f"An error occurred!: {e}")
            client.close()
            break


def start():
    answer = input('Would you like to connect (yes/no)? ')
    if answer.lower() != 'yes':
        return

    connection = connect()

    thread = threading.Thread(target=receive_messages, args=(connection,))
    thread.start()
    first = True
    while True:
        if first == True:
            msg = input("Message (q for quit): ")
            first = False
        else:
            msg = input("Message: ")

        if msg == 'q':
            break

        send(connection, msg)

    send(connection, DISCONNECT_MESSAGE)
    time.sleep(1)
    print('Disconnected')


start()