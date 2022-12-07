import socket
import os
from datetime import datetime
import random
import logging

sock = socket.socket()
logging.basicConfig(filename="sample.log", level=logging.INFO)

try:
    with open('settings.txt', 'r') as f:
        settings = f.read().split('\n')
    port = int(settings[0])
    dirname = settings[1]
    max_size = int(settings[2])
    type_list = settings[3].split()
except:
    settings = open('settings.txt', 'w')
    for i in ['80', os.getcwd(), '8192',' '.join(['html', 'jpeg', 'png'])]:
        settings.write(i + '\n')
    settings.close()
    port = 80
    dirname = os.getcwd()
    max_size = 8192
    type_list = ['html', 'jpeg', 'png']

try:
    sock.bind(('', port))
except:
    port = random.randint(8080, 8300)
    sock.bind(('', port))
sock.listen()

print('Порт: {}'.format(port))


def cret(msg_name, dirname):
    with open(os.path.join(dirname, msg_name), 'rb') as f:
        data = f.read()
    return data


while True:
    conn, addr = sock.accept()
    msg = conn.recv(max_size).decode()
    if msg.split()[1] == '/' or msg.split()[1] == '/index.html':
        msg_name = 'index.html'
    else:
        if not os.path.isfile(os.path.join(dirname, msg.split()[1][1:])):
            logging.error("{}, {}, {}, {}".format(addr[0], str(datetime.now()), msg.split()[1][1:], '404'))
            msg_name = '404.html'
        else:
            msg_name = msg.split()[1][1:]

    if msg_name.split('.')[-1] in type_list:
        if msg_name.split('.')[-1] == 'html':
            data_type = 'text/html'
            logging.info("{}, {}, {}, {}".format(addr[0], str(datetime.now()), msg_name, '202'))
        elif msg_name.split('.')[-1] == 'png':
            data_type = 'image/png'
            logging.info("{}, {}, {}, {}".format(addr[0], str(datetime.now()), msg_name, '202'))
        elif msg_name.split('.')[-1] == 'jpeg':
            data_type = 'image/jpeg'
            logging.info("{}, {}, {}, {}".format(addr[0], str(datetime.now()), msg_name, '202'))
    else:
        logging.error("{}, {}, {}, {}".format(addr[0], str(datetime.now()), msg_name, '403'))
        msg_name = '403.html'
        data_type = 'text/html'
    data = cret(os.path.join(dirname, msg_name), dirname)

    answ = """HTTP/1.1 200 OK
Server: SelfMadeServer v0.0.1
Date: {}
Content-type: {}
Content-length: {}
Connection: close

""".format(str(datetime.now()).split('.')[0], data_type, os.path.getsize(os.path.join(dirname, msg_name)))
    conn.send(answ.encode() + data)

sock.close()