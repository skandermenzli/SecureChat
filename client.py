import threading
import socket
import rsa

nickname = input("Choose your Username: ")
public_key, private_key = rsa.newkeys(1024)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 7777))


def receive():
    i= 2
    while True:
        try:
            # Receive Message From Server
            # If 'NICK' Send Nickname
            message = client.recv(1024)
            if(i==0):
                msg = rsa.decrypt(message, private_key).decode('ascii')
                print(msg)
                continue
            if message.decode('ascii') == 'Username':
                i-=1
                client.send(nickname.encode('ascii'))
            elif message.decode('ascii') == 'key':
                print('hiiii')
                i-=1
                client.send(public_key.save_pkcs1("PEM"))
            else:
                msg = rsa.decrypt(message,private_key).decode('ascii')
                print(message)
        except:
            # Close Connection When Error
            print("An error occured!")
            client.close()
            break


def write():
    while True:
        message = '{}: {}'.format(nickname, input(''))
        client.send( message.encode('ascii'))


receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()