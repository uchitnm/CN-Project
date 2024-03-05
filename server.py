import threading
import socket
import ssl  # Import SSL module
import random
import colors as c

ip = "127.0.0.1"
port = [49153, 49154, 49155, 49156]
server_sockets = [ ssl.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM), certfile='./server.crt', keyfile='./server.key', server_side=True, ssl_version=ssl.PROTOCOL_TLS) for _ in range(4) ]
# server_sockets = [ socket.socket(socket.AF_INET, socket.SOCK_STREAM) for _ in range(4) ]
# server_sockets = [ssl.create_default_context(ssl.Purpose.CLIENT_AUTH).load_cert_chain(certfile='./server.crt', keyfile='./server.key') for _ in range(4) ]

for i, server_socket in enumerate(server_sockets):
    server_socket.bind((ip, port[i]))
    server_socket.listen()

def func(i):
        if i[1] == "A":
                return "Z"
        return i[1]
class ServerConnect:
    def __init__(self, server):
        self.server = server
        self.clients = {}
        self.shapes=["♠","♦","♣","♥"]
        self.numbers=["A","2","3","4","5","6","7","8","9","10","J","Q","K"]
        self.count=0
        self.started=False
        self.dealer={}
        self.deck = []
        self.another_thing = 0
        self.proprity = []

    def startgame(self):
        self.dealer = {"nickname" : "dealer" , "cards" : [] , "score" : 0 , "status" : False}
        self.deck=[(a, b) for a in self.shapes for b in self.numbers]
        random.shuffle(self.deck)
        for j in range(2): 
            self.dealer["cards"].append(self.deck.pop())
            for i in self.clients:
                self.clients[i]["cards"].append(self.deck.pop())              
        for i in self.clients:
            for card_val in self.clients[i]["cards"]:
                if card_val[1] in "2345678910":
                    self.clients[i]["score"] += int(card_val[1])
                elif card_val[1] == "A":
                    if self.clients[i]["score"] >= 11:
                        self.clients[i]["score"] += 1
                    else:
                        self.clients[i]["score"] += 11
                else:
                    self.clients[i]["score"] += 10
        dealer_cards = self.dealer["cards"]
        if dealer_cards[1][1] in "2345678910":
            self.dealer["score"] += int(dealer_cards[1][1])
        elif dealer_cards[1][1] == "A":
            self.dealer["score"] += 11
        else:
            self.dealer["score"] += 10
        self.broadcast((c.b+f'{self.dealer["nickname"]} have [ (X), {self.dealer["cards"][1]} ] Cards, Has score of {self.dealer["score"]}'+c.x).encode())
        for i in self.clients:
            self.broadcast((c.b+f'{self.clients[i]["nickname"]} have {self.clients[i]["cards"]} Cards, Has score of {self.clients[i]["score"]}\n'+c.x).encode())
        
        self.another_thing = 1 



        self.broadcast((c.y+f" Hit OR Stand : "+c.x).encode())

            
    def display_Score(self):
        self.broadcast((c.y+f'{self.dealer["nickname"]} have [ (X), {self.dealer["cards"][1]} ] Cards, Has score of {self.dealer["score"]}\n'+c.x).encode())
        for i in self.clients:
            self.broadcast((c.y+f'{self.clients[i]["nickname"]} have {self.clients[i]["cards"]} Cards, Has score of {self.clients[i]["score"]}\n'+c.x).encode())


    def hit_card(self,client):
                
                self.clients[client]["cards"].append(self.deck.pop())
                self.clients[client]["score"] = 0 
                for card_val in sorted(self.clients[client]["cards"], key = lambda x : func(x)):
                    if card_val[1] in "2345678910":
                        self.clients[client]["score"] += int(card_val[1])
                    elif card_val[1] == "A":
                        if self.clients[client]["score"] >= 11:
                            self.clients[client]["score"] += 1
                        else:
                            self.clients[client]["score"] += 11
                    else:
                        self.clients[client]["score"] += 10

                if self.clients[client]["score"] > 21:
                    self.another_thing +=1
                    self.clients[client]["status"] = False
                    self.broadcast((c.o+f'{self.clients[client]["nickname"]} is Busted.\n'+c.x).encode())

                if self.clients[client]["score"] == 21:
                    self.another_thing +=1
                    self.clients[client]["status"] = False
                    self.broadcast((c.g+f'{self.clients[client]["nickname"]} Won.\n'+c.x).encode())

                self.display_Score()

                if self.another_thing > self.count:
                    self.stand_card(client)

    def reset_vales(self):
        self.started = False
        self.count = 0

        for i in self.clients:
            self.clients[i]["score"] = 0
            self.clients[i]["cards"] = []
            self.clients[i]["status"] = True
    def end_game(self,flag):   
            if flag:
                while True:
                    self.dealer["cards"].append(self.deck.pop())
                    self.dealer["score"]=0
                    dealer_cards = sorted(self.dealer["cards"], key = lambda x : func(x))
                    for i in dealer_cards:
                        if i[1] in "2345678910":
                            self.dealer["score"] += int(i[1])
                        elif i[1] == "A":
                            if self.dealer["score"]>10:
                                 self.dealer["score"]+=1
                            else:
                                self.dealer["score"] += 11
                        else:
                            self.dealer["score"] += 10

                    if self.dealer["score"] > 21:
                            self.dealer["status"] = False
                            self.broadcast((c.r+f' Dealer is Busted.\n'+c.x).encode())
                            break

                    if self.dealer["score"] == 21:
                            self.dealer["status"] = False
                            self.broadcast((c.r+f'You Lost.'+c.x).encode())
                            self.broadcast((c.g+f'Dealer Won.\n'+c.x).encode())
                            break
                    
                    if self.dealer["score"]  >  17:
                             break
                    
                    self.display_Score()
                self.display_Score()
                for player in self.clients:
                                if self.clients[player]["score"] > self.dealer["score"] and self.clients[player]["score"] <= 21:
                                    self.broadcast((c.g+f'{self.clients[player]["nickname"]} Won!\n'+c.x).encode())
                                else:
                                    self.broadcast((c.r+f'{self.clients[player]["nickname"]} Lost.\n'+c.x).encode())

                
                self.reset_vales()

    def stand_card(self,client):
            self.another_thing +=1
            self.clients[client]["status"] = False
            flag=True
            for i in self.clients:
                 if self.clients[i]["status"]:
                      flag=False
            if flag:
                 self.end_game(flag)
    
                            
    def help(self,client):
        message = c.b+"""\n
Hi, Just here are the commands you need to know
    1) /hit   -> To hit 
    2) /stand -> To stand
    3) /start -> To notify you are ready for the game
    4) /leave -> To exit the game.
    5) /reset -> To restart/ reset the game
    6) /help  -> Get to know your commands
    """+c.x
        client.send(message.encode("ascii"))


    def broadcast(self, message):
        for client in self.clients:
            client.send(message)

    def handle(self, client):
        while True:
            try:
                message = client.recv(1024)
                try:
                    if ((f'{self.clients[client]["nickname"]}: /start') == message.decode("ascii")) or ((f'{self.clients[client]["nickname"]}: /reset') == message.decode("ascii")):
                        self.broadcast(f'{self.clients[client]["nickname"]} is ready to play!'.encode('ascii'))
                        self.count+=1
                        self.clients[client]["turn_no"] = self.count
                        self.proprity.append(client)
                        
                        if self.count==len(self.clients):
                            self.broadcast((c.b+f"Starting Game!!"+c.x).encode('ascii'))
                            self.started=True
                            self.startgame()
                        continue
                    if f'{self.clients[client]["nickname"]}: /hit' == message.decode("ascii"):
                        # if  self.clients[client]["turn_no"] == self.another_thing :
                        if client == self.proprity[0]:
                            self.hit_card(client)
                            continue
                        else:
                            client.send((c.r+"Hold on It's not you turn yet.!!\n"+c.x).encode("ascii"))
                    
                    if f'{self.clients[client]["nickname"]}: /stand' == message.decode("ascii"):

                        # if  self.clients[client]["turn_no"] == self.another_thing:
                        #     self.stand_card(client)
                        #     continue
                        # else:
                        #     client.send((c.r+"Hold on It's not you turn yet.!!\n"+c.x).encode("ascii"))

                        current_player = self.proprity[0]  # Get the player who has the current turn
                        if client == current_player:
                            self.stand_card(client)
                        else:
                            client.send((c.r + "Hold on, it's not your turn yet.\n" + c.x).encode("ascii"))


                    if "/leave" in message.decode("ascii") :
                            if self.started:
                                print(self.another_thing,self.count,self.clients[client]["turn_no"])
                                for i in self.clients:
                                    if self.clients[client]["turn_no"]<self.another_thing:
                                        self.another_thing-=1
                                    if self.clients[i]["turn_no"]>self.clients[client]["turn_no"]:
                                        self.clients[i]["turn_no"]-=1 
                            self.broadcast((c.v+f'{self.clients[client]["nickname"]} left the Chat!'+c.x).encode('ascii'))
                            print((c.v+f'{self.clients[client]["nickname"]} left the Chat!'+c.x))
                            del self.clients[client]
                            self.count -= 1
                            self.proprity.remove(client)
                            if self.another_thing==self.count:
                                self.end_game(True)

                    self.broadcast(message)  
                except Exception :
                     break          
            except socket.error:
                if client in self.clients:
                        self.broadcast((c.v+f'{self.clients[client]["nickname"]} left the Chat!'+c.x).encode('ascii'))
                        del self.clients[client]
                        break


    def receive_connection(self):
        while True:

            client, address = self.server.accept()
            if self.started:
                client.send("Games has started. Try joining another room or wait till game is finished".encode('ascii'))
                continue
            if len(self.clients) == 4 :
                client.send("Room Full".encode('ascii'))
                continue

            client.send('NICK'.encode('ascii'))
            nickname = client.recv(1024).decode('ascii')

            while nickname in self.clients.values():
                print(self.clients)
                nickname = ""
                client.send((c.r+"Username Present"+c.x).encode('ascii'))
                nickname = client.recv(1024).decode('ascii')
                

            print(f"Connected with {(address)}")
            
            self.clients[client] = { "nickname" : nickname , "cards" : [] , "score" : 0 , "status" : True , "turn_no" : None }
            print(self.clients)
            print(f'Nickname of the client is {nickname}')
            self.broadcast(f'{nickname} joined the Chat'.encode('ascii'))

            client.send(f'Connected to the Server!, {len(self.clients)} player(s) is/are in the room.'.encode('ascii'))
            self.help(client)


            thread = threading.Thread(target=self.handle, args=(client,))
            thread.start()

print('Server is Listening ...')


servers = [ServerConnect(server_socket) for server_socket in server_sockets]


server_threads = [threading.Thread(target=server.receive_connection) for server in servers]
for thread in server_threads:
    thread.start()


for thread in server_threads:
    thread.join()
