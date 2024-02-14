from functions import recordAudio
from functions import playbackAudio
import matplotlib.pyplot as plt

output, sample_rate = recordAudio(5)
playbackAudio(output, sample_rate)

'''
plt.figure(1)
plt.title('Output Waveform')
plt.xlabel('Time')
plt.plot(output)
plt.show()
'''