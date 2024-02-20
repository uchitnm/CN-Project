import threading
import socket

ip = "127.0.0.1"
port = [1234,1235,1236,1237]
server_sockets = [socket.socket(socket.AF_INET, socket.SOCK_STREAM) for i in range(4)]

for i, server_socket in enumerate(server_sockets):
    server_socket.bind((ip, port[i]))
    server_socket.listen()



class ServerConnect:
    def __init__(self, server):
        self.server = server
        self.clients = {}

    def broadcast(self, message):
        for client in self.clients:
            client.send(message)

    def handle(self, client):
        while True:
            try:
                message = client.recv(1024)
                self.broadcast(message)  

            except socket.error:
                if client in self.clients:
                        self.broadcast(f'{self.clients[client]["nickname"]} left the Chat!'.encode('ascii'),client)
                        del self.clients[client]
                        break

    def receive(self):
        while True:

            client, address = self.server.accept()
            if len(self.clients) == 5 :
                client.send("Room Full".encode('ascii'))
                break

            client.send('NICK'.encode('ascii'))
            nickname = client.recv(1024).decode('ascii')
            
            if nickname in self.clients.values():
                client.send("Username Present".encode('ascii'))
                break

            print(f"Connected with {str(address)}")

            self.clients[client] = nickname 
            
            print(f'Nickname of the client is {nickname}')
            self.broadcast(f'{nickname} joined the Chat'.encode('ascii'))
            client.send('Connected to the Server!'.encode('ascii'))

            thread = threading.Thread(target=self.handle, args=(client,))
            thread.start()

print('Server is Listening ...')


servers = [ServerConnect(server_socket) for server_socket in server_sockets]


server_threads = [threading.Thread(target=server.receive) for server in servers]
for thread in server_threads:
    thread.start()


for thread in server_threads:
    thread.join()
