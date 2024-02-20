import socket
import threading
import json



def enter_server():

    with open('servers.json', ) as f:
        data = json.load(f)
    print("Rooms Avaliable: ")
    for servers in data:
        print(servers, end=" ")
    # Ask user for the name of the server to join

    server_name = input("\nEnter the server name:")
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
    while True:
        global stop_thread
        if stop_thread:
            break
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            else:
                print(message)
        except socket.error:
            print('Error Occured while Connecting')
            client.close()
            break


def write():
    while True:
        if stop_thread:
            break
        # Getting Messages
        message = f'{nickname}: {input("")}'

        client.send(message.encode('ascii'))


receive_thread = threading.Thread(target=receive)
receive_thread.start()
write_thread = threading.Thread(target=write)
write_thread.start()

