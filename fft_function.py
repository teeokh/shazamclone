from functions import recordAudio
import numpy as np
import matplotlib.pyplot as plt


# Create and visualise fft for recorded audio

recorded_frames = recordAudio(3)
ftt = np.fft.fft(recorded_frames) 

