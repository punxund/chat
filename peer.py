#from asyncio.windows_events import NULL
from operator import length_hint
import socket
import threading
import time
import os.path


# list of connections
connections = []


# dictionary of connected peers (through chats) 
# ID : IP-Address
chats = {}


host = '0.0.0.0'

sock_recv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_recv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

sock_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_send.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

sock_group = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock_group.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

sock_group_peer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock_group_peer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

sport = 50001
dport = 50002


# private chat
def init_chat():
     # bind sockets
    sock_recv.bind((host, sport))

    ip_peer = input('enter the address of the peer you want to connect to: ')

    # start the thread for listening to messages
    listener = threading.Thread(target=chat_listener)
    listener.start()

    sock_send.bind((host, dport))

    readHistory(ip_peer)

    while True:
        msg = input()
        sock_send.sendto(msg.encode(), (ip_peer, sport))
        msg = recv_message(msg, host)
        print(msg)
        saveHistory(msg, ip_peer)

def chat_listener():
    while True:      
        data = sock_recv.recvfrom(1024)
        adr = data[1][0]
        msg = recv_message(data[0].decode(), adr)
        print(msg)
        saveHistory(msg, adr)

        
    
# group chat
def init_group_chat():
    is_super = False

    # bind sockets
    sock_group.bind((host, sport))

    sock_group.listen(5)

    super_peer = str(input('enter the address of the superpeer (or leave blank): '))

    if super_peer == '':
        is_super = True

    if is_super:
        # start the thread for accepting connections
        listener = threading.Thread(target=handler)
        listener.start()
    else:
        sock_group_peer.connect((super_peer,sport))
        print("connected to the superpeer")

        # start the thread for listening to messages
        listener = threading.Thread(target=group_listener_peer, daemon = True)
        listener.start()

        sender = threading.Thread(target=group_sender_peer)
        sender.start()
     

def handler():
    while True:
        print('waiting for connections...')
        c, a = sock_group.accept()
        connections.append(c)
        connected = str(a) + ' has connected'
        print(connected)


        for c in connections:          
            c.send(connected.encode())

         # start the thread for listening to messages
        listener = threading.Thread(target=group_listener_super, daemon=True, args=(c, a))
        listener.start()

        sender = threading.Thread(target=group_sender_super, daemon=True, args=(c, a))
        sender.start()

       


def group_listener_super(c, a):
    while True:
        msg = c.recv(1024)
        recvd = recv_message(msg.decode(), a[0])
        print(recvd)
        for c in connections:
            c.sendall(recvd.encode())

def group_sender_super(c, a):
    while True:
        msg = input()    
        recvd = recv_message(msg, a[0])
        print(recvd)
        for c in connections:
            c.sendall(recvd.encode())
        


def group_listener_peer():
    while True:
        data = sock_group_peer.recv(1024)
        print(data.decode())


def group_sender_peer():
    while True:
        msg = input()
        sock_group_peer.sendall(msg.encode())

# called when a message is received
def recv_message(message, address):
    return(time.strftime('%Y-%m-%d %H:%M:%S ') + address + ' said: ' + message)

# save History as txt file @Sik
def saveHistory(message, ip_peer):
    path = os.path.join('.', 'src', 'cache', 'history_'+str(ip_peer)+'.txt')
    if os.path.exists(path):         
        with open(path, 'a') as file:
            file.write(message + '\n')
            #print(now.strftime('%Y-%m-%d %H:%M:%S')+' "'+message+'"')
    else: 
        f = open(path, 'w')
        f.write(message + '\n')
        f.close()

# read History
def readHistory(ip_peer):
    path = os.path.join('.', 'src', 'cache', 'history_'+str(ip_peer)+'.txt')
    if os.path.exists(path):
        with open(path, 'r') as file:
            for line in file:
                print(line, end='')
def main():
    not_selected = True
    while not_selected:
        chat = input('enter \'c\' for private chat or \'g\' for group chat: ')

        if chat == 'c':
            not_selected = False
            init_chat()
        elif chat == 'g':
            not_selected = False
            init_group_chat()
    
    #ip_peer = "10.5.38.50"
    #ip_peer = 'localhost'
    #start_chat(ip_peer)


if __name__ == "__main__":
    main()
