import socket
import threading
import json
import sys

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
    ip = data[server_name]["ip"]
    port = data[server_name]["port"]
    
    global client
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect to a host
    client.connect((ip, port))


# Menu loop, it will loop until the user choose to enter a server

while True:
    enter_server()
    break



stop_thread = False



def receive():
    local_name = ""
    while True:
        global stop_thread
        if stop_thread:
            break
        try:
            message = client.recv(1024).decode('ascii')
            if message=="Games has started. Try joining another room or wait till game is finished":
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
                nickname=""
                nickname = input("Choose a different nickname:")
                # Retry sending the nickname
                client.send(nickname.encode('ascii'))
                continue

            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            else:
                print(message)

        except socket.error:
            print('Error Occurred while Connecting')
            client.close()
            stop_thread = True
            exit(0)
            break

def write():
    global stop_thread
    while True:
        try:

            if stop_thread:
                break
            # Getting Messages
            if nickname!="":
                message = f'{nickname}: {input("")}'

            if "/leave" in message:
                    client.send(message.encode("ascii"))
                    print("Your left the server.")
                    client.close()
                    stop_thread = True
                    break
            if(nickname!=""):
                client.send(message.encode('ascii'))

        except socket.error:
            print('Error Occurred while Sending Message')
            client.close()
            stop_thread = True
            break

receive_thread = threading.Thread(target=receive)
receive_thread.start()
write_thread = threading.Thread(target=write)
write_thread.start()
