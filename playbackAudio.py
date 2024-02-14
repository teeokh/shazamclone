import wave
from recordAudio import recordAudio

def playbackAudio():
    output, rate = recordAudio()
    with wave.open('output.wav', 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(rate)
        wf.writeframes(output.tobytes())