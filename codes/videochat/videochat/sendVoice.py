import socket  as sock
from voiceRecorder import VoiceRecorder
from tempfile import TemporaryFile
from struct import pack
import pyaudio
import wave

(HOST,PORT)=('localhost',19123)
s=sock.socket(sock.AF_INET,sock.SOCK_STREAM); s.connect((HOST,PORT))

mic = VoiceRecorder()

sample_width, data = mic.record()



data = pack('<' + ('h'*len(data)), *data)

RATE = 44100

temp = TemporaryFile()

af = wave.open(temp, 'wb') #audio file
af.setnchannels(1)
af.setsampwidth(sample_width)
af.setframerate(RATE)
af.writeframes(data)

af.close()
# af = wave.open(temp, 'rb')

# with open('./demo.wav', 'rb') as f:
with wave.open(temp, 'rb') as f:
  for l in f:
      s.sendall(l)
s.close()
temp.close()
