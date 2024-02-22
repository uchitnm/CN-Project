import threading
import socket
import random
ip = "127.0.0.1"
port = [49153,49154,49155,49156]
server_sockets = [socket.socket(socket.AF_INET, socket.SOCK_STREAM) for i in range(4)]

for i, server_socket in enumerate(server_sockets):
    server_socket.bind((ip, port[i]))
    server_socket.listen()


class ServerConnect:
    def __init__(self, server):
        self.server = server
        self.clients = {}
        self.shapes=["♣","♦","♥","♠"]
        self.numbers=["A","2","3","4","5","6","7","8","9","10","J","Q","K"]
        self.count=0
        self.started=False
    def startgame(self):
        deck=random.shuffle([(a, b) for a in self.shapes for b in self.numbers]) 
        for j in range(2): 
            for i in self.clients:
                self.clients[i]["cards"].append(deck.pop())
        while True:
            
    def broadcast(self, message):
        for client in self.clients:
            client.send(message)

    def handle(self, client):
        while True:
            try:
                message = client.recv(1024)
                if f"{self.clients[client]["nickname"]}: /start"==message.decode("ascii"):
                    self.broadcast(f"{self.clients[client]["nickname"]} is ready to play!".encode('ascii'))
                    self.count+=1
                    if self.count==len(self.clients):
                        self.broadcast(f"Starting Game!!".encode('ascii'))
                        self.started=True
                        #startGame()
                    continue
                if "/leave" in message.decode("ascii") :
                        self.broadcast(f'{self.clients[client]["nickname"]} left the Chat!'.encode('ascii'))
                        print(f'{self.clients[client]["nickname"]} left the Chat!')
                        del self.clients[client]
                        break
                self.broadcast(message)  

            except socket.error:
                if client in self.clients:
                        self.broadcast(f'{self.clients[client]["nickname"]} left the Chat!'.encode('ascii'))
                        del self.clients[client]
                        break

    def receive_connection(self):
        while True:

            client, address = self.server.accept()
            if self.started:
                client.send("Games has started. Try joining another room or wait till game is finished".encode('ascii'))
                continue
            if len(self.clients) == 2 :
                client.send("Room Full".encode('ascii'))
                continue

            client.send('NICK'.encode('ascii'))
            nickname = client.recv(1024).decode('ascii')

            while nickname in self.clients.values():
                print(self.clients)
                nickname = ""
                client.send("Username Present".encode('ascii'))
                nickname = client.recv(1024).decode('ascii')
                

            print(f"Connected with {str(address)}")
            
            self.clients[client]= { "nickname " : nickname , "cards" : [] , "score" : 0}
            
            print(f'Nickname of the client is {nickname}')
            self.broadcast(f'{nickname} joined the Chat'.encode('ascii'))

            client.send(f'Connected to the Server!, {len(self.clients)} are in the room.'.encode('ascii'))

            thread = threading.Thread(target=self.handle, args=(client,))
            thread.start()

print('Server is Listening ...')


servers = [ServerConnect(server_socket) for server_socket in server_sockets]


server_threads = [threading.Thread(target=server.receive_connection) for server in servers]
for thread in server_threads:
    thread.start()


for thread in server_threads:
    thread.join()
