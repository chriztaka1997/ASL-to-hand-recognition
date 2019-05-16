import socket as sock
import pyaudio
import wave

chunk = 1024

(HOST,PORT) = ('localhost',19123)
s = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
s.bind((HOST, PORT)); s.listen(1); conn, addr = s.accept()


with open('new_demo.wav','wb') as f:
  while True:
    l = conn.recv(1024)
    if not l:
        break
    f.write(l)
s.close()
