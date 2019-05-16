import pyaudio  
import wave  

#define stream chunk 
chunk = 1024 

class PlayVoice:
    def __init__(self, tempFile):
        #open a wav format music  
        # f = wave.open(r"/usr/share/sounds/alsa/Rear_Center.wav","rb")  
        # f = wave.open(tempFile,"rb")
        #instantiate PyAudio  
        p = pyaudio.PyAudio()  
        #open stream  
        stream = p.open(format = p.get_format_from_width(tempFile.getsampwidth()),  
                        channels = tempFile.getnchannels(),  
                        rate = tempFile.getframerate(),  
                        output = True)  
        #read data  
        data = tempFile.readframes(chunk)  

        #play stream  
        while data:  
            stream.write(data)  
            data = tempFile.readframes(chunk)  

        #stop stream  
        stream.stop_stream()  
        stream.close()  

        #close PyAudio  
        p.terminate()

        #destroy tempfile object
        tempFile.close()