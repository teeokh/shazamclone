import numpy as np
import pyaudio 
import wave
import matplotlib.pyplot as plt 

# Instance variables

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
filename = 'output.wav'


#Capture audio recording

def record_audio(seconds):

    RECORD_SECONDS = seconds

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
    frames_array = np.frombuffer(byte_frames, dtype=np.int16) # Converts bytes object into np array (for input into FFT)
    
    duration = len(frames_array) / RATE
    time = np.linspace(0, duration, num=len(frames_array))

    stream.stop_stream() 
    stream.close() # Stops and closes stream

    p.terminate() # Terminates PortAudio

    print('Finished recording')

    '''
    # Write the data to the wave file (this will also confirm that the data in byte_frames is correct)
    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setframerate(RATE)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.writeframes(byte_frames) # Needs to be bytes (readable buffer as input)
    wf.close()
    '''
    
    return frames_array, RATE, time, CHUNK

    # Minor discrepancy in number of frames recorded - 44032 frames for a 44100 sr over 1 second


# Export and playback audio

def playback_audio(array, sample_rate):

    with wave.open('output.wav', 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(array.tobytes())
        wf.close()


# Produce waveform 

def show_waveform(array,time):

    plt.title('Waveform')
    plt.xlabel('Time')
    plt.ylabel('Amplitude')
    plt.plot(time, array)
    plt.show()


# Create and visualise fft for recorded audio

from numpy.fft import fft

def show_fft(array,sr):
   X = fft(array) 
   N = len(X)
   n = np.arange(N)
   T = N/sr
   freq = n/T

   plt.figure().set_figwidth(12)
   plt.plot(freq, np.abs(X))
   plt.title('Fast Fourier Transform (FFT) of Output')
   plt.xlabel('Frequency (Hz)')
   plt.ylabel('Amplitude (dB)')
   plt.xscale('log')
   plt.show()


# Create and visualise spectrogram for recorded audio using STFT

from scipy.signal import stft
from scipy.signal.windows import gaussian

def show_spectrogram(array,sr,window,nperseg,noverlap):
    # nperseg = segment size / window size (larger = more frequency resolution, smaller = more time resolution)
    # stft_array will be half of chunk size + 1 (as Nyquist frequency is half of sampled frequency + the first DC component (0 Hz))
    freqs, times, stft_array = stft(array,sr,window=window,nperseg=nperseg,noverlap=noverlap) #stft_array = ndarray

    max_power = np.max(np.abs(stft_array)**2)
    stft_power_db = 10 * np.log10((np.abs(stft_array)**2 + 1e-10) / max_power)

    # Create colormesh (for time against frequency) and colorbar (for amplitude)
    plt.figure().set_figwidth(12)
    plt.pcolormesh(times, freqs, stft_power_db, shading='gouraud', vmin=-80,cmap='inferno') # Spectrogram is the magnitude of STFT array, squared
    plt.colorbar(label='Intensity (dB)')

    plt.xlabel('Time')
    plt.ylabel('Frequency (Hz)')
    plt.title('Spectrogram')
    plt.ylim(0, sr/2)
    plt.show()