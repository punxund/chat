import socket
host='192.168.178.22'
port=10000
timeout_seconds=1
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(timeout_seconds)
result = sock.connect_ex((host,int(port)))
if result == 0:
    print("Host: {}, Port: {} - True".format(host, port))
else:
    print("Host: {}, Port: {} - False".format(host, port))
sock.close()
