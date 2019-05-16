import socket

class videosocket:
    '''A special type of socket to handle the sending and receiveing of fixed
       size frame strings over ususal sockets
       Size of a packet or whatever is assumed to be less than 100MB
    '''

    def __init__(self , sock=None):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create sock if none exist
        else:
            self.sock= sock #if sock exist, assign self.sock to sock

    def connect(self,host,port):
        self.sock.connect((host,port)) #connect to tcp host

    def vsend(self, framestring):
        totalsent = 0
        metasent = 0
        length =len(framestring)
        lengthstr=str(length).zfill(8)

        while metasent < 8 : #send length of frame data
            sent = self.sock.send(lengthstr[metasent:])
            if sent == 0:
                raise RuntimeError("Socket connection broken")
                # print("Error sending")
            metasent += sent


        while totalsent < length : #send frame data
            sent = self.sock.send(framestring[totalsent:])
            if sent == 0:
                raise RuntimeError("Socket connection broken")
                # print("Error sending")
            totalsent += sent

    def vreceive(self):
        # print("got into vreceive")
        totrec = 0
        metarec = 0
        msgArray = []
        metaArray = []
        while (metarec < 8):
            chunk = self.sock.recv(8 - metarec)
            print('Chunk: ', chunk)
            if chunk == '':
                raise RuntimeError("Socket connection broken")
                # print("Error receiving")
            metaArray.append(chunk)
            metarec += len(chunk)
        lengthstr= ''.join(metaArray)
        length=int(lengthstr)

        while(totrec<length) :
            chunk = self.sock.recv(length - totrec)
            if chunk == '':
                raise RuntimeError("Socket connection broken")
                # print("Error receiving")
            msgArray.append(chunk)
            totrec += len(chunk)
        # print("msgArray: ", msgArray)
        return ''.join(msgArray)
    
    # def sendAudio(self, fileObject): #send audio recording
    #     with open('./demo.wav', 'rb') as f:
    #     for l in f:
    #         s.sendall(l)
