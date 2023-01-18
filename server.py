import threading
import socket
import rsa

host = '127.0.0.1'
port = 7777



# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()  #param 5 max number of users waiting for accept before declining others

clients = []
nicknames = []
keys = []

# Sending Messages To All Connected Clients
def broadcast(message):
    for client in clients:
        print(keys[0])
        i = clients.index(client)
        if(isinstance(message, str)):

           client.send(rsa.encrypt(message.encode(),keys[i]))

        else:
            client.send(rsa.encrypt(message, keys[i]))

# Handling Messages From Clients
def handle(client):
    while True:
        try:
            # Broadcasting Messages
            message = client.recv(1024)
            broadcast(message)
        except:
            # Removing And Closing Clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} left!'.format(nickname).encode('ascii'))
            nicknames.remove(nickname)
            key = keys[index]
            keys.remove(key)
            break


def receive():
    while True:
        # Accept Connection
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        # Request And Store Nickname
        client.send('Username'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)
        client.send('key'.encode('ascii'))
        key = rsa.PublicKey.load_pkcs1(client.recv(1024))
        keys.append(key)

        # Print And Broadcast Nickname
        print("Username is {}".format(nickname))
        broadcast("{} joined!".format(nickname))
        #client.send('Connected to server!'.encode('ascii'))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


receive()

