"""
    Multiplayer BlackJack Game, with chat feature. using Socket Programming and SSL for secure connection.
    Client Side Code.

    Student Details:
    Name : U Sanjeev ; SRN : PES1UG22CS660
    Name : Uchit N M ; SRN : PES1UG22CS661

    Code Description:
    This is the client side code, which connects to the server and sends and receives messages.
    The client can choose the server to connect to and also choose a nickname.
    The client can perform differnt action by sending diffrent commands.
"""


import socket
import threading
import json
import sys
import ssl


def enter_server():
    with open('servers.json', ) as f:
        data = json.load(f)
    print("Rooms Avaliable: ")
    for servers in data:
        print(servers)

    # Ask user for the name of the server to join
    server_name = input("Enter the server name:")
    global nickname
    nickname = input("Choose Your Nickname:")

    # Store the ip and port number for connection
    try:
        ip = data[server_name]["ip"]
        port = data[server_name]["port"]
    except KeyError:
        print("Server not found.")
        print("Please enter a valid server name.")
        print("+--------------------------------+")
        enter_server()

    global client

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client = ssl.wrap_socket(
        client, cert_reqs=ssl.CERT_NONE, ssl_version=ssl.PROTOCOL_TLS)
    client.connect((ip, port))


# Menu loop, it will loop until the user choose to enter a server
while True:
    enter_server()
    break

stop_thread = False


def receive():

    while True:
        global stop_thread
        if stop_thread:
            break
        try:
            message = client.recv(1024).decode()

            if message == "Games has started. Try joining another room or wait till game is finished":
                print(message)
                raise socket.error

            if message == "Room Full":
                print(message)
                raise socket.error

            if message == "Username Present":
                print(message)
                sys.stdout.flush()  # Flush the output buffer
                # Ask the user to choose a different nickname

                global nickname
                nickname = ""
                nickname = input("Choose a different nickname:")

                # Retry sending the nickname
                client.send(nickname.encode('ascii'))
                continue

            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            else:
                print(message)

        except socket.error:
            if stop_thread:
                exit(0)
            stop_thread = True
            print('Error Occurred while Connecting')
            client.close()
            exit(0)


def write():
    global stop_thread
    while True:
        try:

            if stop_thread:
                break
            # Getting Messages
            if nickname != "":
                message = f'{nickname}: {input("")}'

            if "/leave" in message:
                stop_thread = True
                client.send(message.encode("ascii"))
                print("You left the server.")
                client.close()
                break

            if (nickname != ""):
                client.send(message.encode('ascii'))

        except socket.error:
            stop_thread = True
            print('Error Occurred while Sending Message')
            client.close()
            break


receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
