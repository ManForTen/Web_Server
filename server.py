import socket

sock = socket.socket()

try:
    sock.bind(('', 80))
    print("Используется порт 80")
except OSError:
    sock.bind(('', 8080))
    print("Используется порт 8080")

sock.listen(5)

conn, addr = sock.accept()
print(addr)

data = conn.recv(8192)
msg = data.decode()

print(msg)

resp = """HTTP/1.1 200 OK
    Server: SelfMadeServer v0.0.1
    Content-type: text/html
    Connection: close
Hello!"""

conn.send(resp.encode())
conn.close()