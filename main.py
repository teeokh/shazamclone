from functions import record_audio
from functions import playback_audio
from functions import show_waveform
from functions import show_fft
from functions import show_spectrogram

array, sample_rate, time, chunk = record_audio(5)
#playback_audio(array, sample_rate)
#show_waveform(array, time)
#show_fft(array, sample_rate)
show_spectrogram(array,sample_rate,window='hann',nperseg=512,noverlap=256)
