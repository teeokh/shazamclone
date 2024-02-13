#Capturing audio recording

def recordAudio(seconds):
    import pyaudio 
    import wave

    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    RECORD_SECONDS = seconds
    filename = 'output.wav'

    p = pyaudio.PyAudio()

    print('Recording')

    stream = p.open(
                    format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    frames_per_buffer=CHUNK,
                    input=True)
    
    frames = [] # Will hold the byte data for the recording

    for i in range(0, RATE // CHUNK * RECORD_SECONDS):  # From 0 -> number of chunks
        data = stream.read(CHUNK)
        frames.append(data)  # Reads the data for each chunk (in total of 3 seconds recording), and adds it to the frames array

    stream.stop_stream() 
    stream.close() # Stops and closes stream

    p.terminate() # Terminates PortAudio

    print('Finished recording')


    # Write the data to the wave file
    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setframerate(RATE)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.writeframes(b''.join(frames))
    wf.close()