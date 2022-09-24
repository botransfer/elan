import numpy as np
from scipy.io import wavfile

filename = 'marker.wav'
fs = 44100

user_freq = [697, 770, 852, 941,
             1209, 1336, 1477, 1633]

user_tones = {
    '1': (user_freq[0], user_freq[4]),
    '2': (user_freq[0], user_freq[5]),
    '3': (user_freq[0], user_freq[6]),
    '4': (user_freq[1], user_freq[4]),
    '5': (user_freq[1], user_freq[5]),
    '6': (user_freq[1], user_freq[6]),
    '7': (user_freq[2], user_freq[4]),
    '8': (user_freq[2], user_freq[5]),
    '9': (user_freq[2], user_freq[6]),
}

# marker tone
dur_marker = 0.25

def gen_freq(freq, tones, num):
    tone = tones[str(num)]
    f1 = tone[0]
    f2 = tone[1]
    return f1, f2

# fade in/out to prevent 'pop's
def fade(signal, fs):
    hwSize = int(min(fs // 200, len(signal) // 15))
    hanningWindow = np.hanning(2 * hwSize + 1)
    signal[:hwSize] *= hanningWindow[:hwSize]
    signal[-hwSize:] *= hanningWindow[hwSize + 1:]

def gen_sig(dur, f1, f2, fs):
    n_samples = dur * fs
    samples = np.linspace(0, dur, int(n_samples), endpoint=False)
    signal = np.sin(2 * np.pi * f1 * samples)+np.sin(2 * np.pi * f2 * samples)
    fade(signal, fs)
    return signal

numbers = [1,7,3,8]
signal=[]

for i in range(len(numbers)):
    f1, f2 = gen_freq(user_freq, user_tones, numbers[i])
    signal_temp = gen_sig(dur_marker, f1, f2, fs)
    signal.append(signal_temp)

signal_blank = np.zeros_like(signal[0])
signal = np.concatenate([signal[0], signal_blank, signal[1], signal_blank, signal[2], signal_blank, signal[3]])

signal *= 15000
signal = np.int16(signal)
wavfile.write(filename, fs, signal)
