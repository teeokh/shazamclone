from functions import recordAudio
from functions import playbackAudio
from functions import showWaveform

output, sample_rate, time = recordAudio(5)
playbackAudio(output, sample_rate)
showWaveform(output, time)