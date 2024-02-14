import numpy as np

#Capturing audio recording

def recordAudio(seconds):
    import pyaudio 
    import wave
    import time

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
    
    frames_list = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):  # From 0 -> number of chunks
        if i % (RATE // CHUNK) == 0:
            seconds_left = RECORD_SECONDS - (i // (RATE // CHUNK))
            print(f'Time remaining: {seconds_left}')
        data = stream.read(CHUNK)
        frames_list.append(data)
    
    byte_frames = b''.join(frames_list) # Converts the frames list into bytes object
    np_frames = np.frombuffer(byte_frames, dtype=np.int16) # Converts bytes object into np array (for input into FFT)
        

    stream.stop_stream() 
    stream.close() # Stops and closes stream

    p.terminate() # Terminates PortAudio

    print('Finished recording')


    # Write the data to the wave file
    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setframerate(RATE)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.writeframes(byte_frames) # Needs to be bytes (readable buffer as input)
    wf.close()

    print(np_frames.shape[0])
    return np_frames

    # Minor discrepancy in number of frames recorded - 44032 frames for a 44100 sr over 1 second