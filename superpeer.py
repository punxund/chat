import socket
import threading
import sys
import time
from random import randint
import tkinter as tk

global p2p_peers 
p2p_peers = []

def initpeer():
    ip = input("write your IP address or superpeer's IP: ")
    p2p_peers.append(ip)
    nickname = input("what is your nickname?>>")

    return nickname

class Superpeer:
    
    connections = []
    peers = []

    def __init__(self):

        try :
            Client.win.destroy()
        except:
            pass
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        port = 50000
        sock.bind(('0.0.0.0', port))        
        sock.listen(1)
        print('You are a superpeer. You can just see the chat window.')
        print('If you want to write something in the chat window, please log in to an new console.')

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
                print(str(data, 'utf-8'))
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
    def setWindow(self):
        self.win = tk.Tk()
        self.win.title('p2p chat on '+str(p2p_peers[0]))
        self.win.geometry('400x500+100+100')
        self.chatCont = tk.Label(self.win, width=50, height=30, text='welcome to p2p chat')
        self.myChat = tk.Entry(self.win, width=40)
        self.sendBtn = tk.Button(self.win, width=10, text='send', command=self.sendMsg)

        self.chatCont.grid(row=0, column=0, columnspan=2)
        self.myChat.grid(row=1, column=0, padx=10)
        self.sendBtn.grid(row=1, column=1)

    def sendMsg(self):
        try:
            msg = self.myChat.get()
            self.myChat.delete(0, tk.END)
            self.myChat.config(text='')
            self.sock.send(bytes(self.nickname+">>" + msg + '\n', 'utf-8'))
        except:
            print("reconnect...")
            self.win.destroy()    

    def __init__(self, ip, nickname):
        self.win = None
        self.chatCont = None
        self.myChat = None
        self.sendBtn = None
        self.allChat =''

        self.setWindow()        

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        port = 50000
        self.sock.connect((ip,port))
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        print("connected to the superpeer")
        self.nickname = nickname
              

        iThread = threading.Thread(target=self.recvMsg)
        iThread.daemon = True
        iThread.start()
                
        self.win.mainloop()

    def recvMsg(self):
        
        while True:
            data = self.sock.recv(1024)
            if not data:
                pass
            if data[0:1] == b'\x11' :
                self.updatePeers(data[1:])
            else:
                msg = str(data, 'utf-8')
                self.allChat += msg
                self.chatCont.config(text=self.allChat)
            

    def updatePeers(self, peerData):
        p2p_peers = str(peerData, "utf-8").split(",")[:-1]
        #print(p2p_peers)

def main():
    nickname = initpeer()
    while True:
        try : 
            print("Trying to connect ...")
            time.sleep(randint(1,5))
            for peer in p2p_peers:
                try:
                    client = Client(peer, nickname)               
                except KeyboardInterrupt:
                    sys.exit(0)
                except :
                    raise
                    pass    
                if randint(1, 5) == 1:
                    try :
                        #Client.win.destroy()
                        superpeer = Superpeer()
                    except KeyboardInterrupt:
                        sys.exit(0)
                    except:
                        print("couldn't start the superpeer ...")
            
            
        except KeyboardInterrupt:
            sys.exit(0)

        
    
if __name__ == '__main__':
    #nickname=initpeer()
    #client = Client(p2p_peers[0],nickname)
    main()
