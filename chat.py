import socket
import threading
import sys
import time
from random import randint



class Server:
    
    connections = []
    peers = []

    def __init__(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        port = 50000
        sock.bind(('0.0.0.0', port))        
        sock.listen(1)
        print('You are a superpeer.')

        while True:
            c, a = sock.accept()
            cThread = threading.Thread(target=self.handler, args=(c, a))
            cThread.daemon = True
            cThread.start()
            self.connections.append(c)
            self.peers.append(a[0])
            print(str(a[0])+ ':' + str(a[1]),"connected")
            self.sendPeers()

    def handler(self, c, a):
        while True:
            try :
                data = c.recv(1024)
                for connection in self.connections:
                    connection.send(data)
                                   
            except :
                print(str(a[0]) + ':' + str(a[1]), "disconnected")
                self.connections.remove(c)
                self.peers.remove(a[0])
                c.close()
                self.sendPeers()
                break
                

    def sendPeers(self):
        p = ""

        for peer in self.peers:
            p = p + peer + ","

        for connection in self.connections:
            connection.send(b'\x11' + bytes(p, "utf-8"))

class Client:   

    def sendMsg(self, sock, nickname):
        while True:
            sock.send(bytes(nickname+">>"+sys.stdin.readline().strip(), 'utf-8'))

    def __init__(self, a):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        port = 50000
        sock.connect((a,port))
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        print("connected to the server")
        nickname = input("What is your nickname? >")

        

        iThread = threading.Thread(target=self.sendMsg, args=(sock, nickname, ))
        iThread.daemon = True
        iThread.start()

        while True:
            data = sock.recv(1024)
            if not data:
                break
            if data[0:1] == b'\x11' :
                self.updatePeers(data[1:])
            else:
                 print(str(data, 'utf-8'))

    def updatePeers(self, peerData):
        p2p.peers = str(peerData, "utf-8").split(",")[:-1]

class p2p:
    peers = []#146.148.45.148

ip = input("write your IP address or superpeer's IP>>")
p2p.peers.append(ip)

while True:
    try : 
        print("Trying to connect ...")
        time.sleep(5)      
        for peer in p2p.peers:           
            try:
                client = Client(peer)
            except KeyboardInterrupt:            
                sys.exit(0)
            except:            
                pass    
            if randint(1, 10) == 1:                        
                try :            
                    server = Server()
                except KeyboardInterrupt:
                    sys.exit(0)
                except:
                    print("couldn't start the server ...")
            
    except KeyboardInterrupt:
        sys.exit(0)
