import argparse
import numpy as np
from scipy.io import wavfile

parser = argparse.ArgumentParser(description='generate marker wave file',
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-freq', default=44100, type=int,
                    help='sampling frequency')
parser.add_argument('-dur', default=0.25, type=float,
                    help='duration of single tone in seconds')
tp = lambda x:list(map(int, [*x]))
parser.add_argument('-seq', default='1738', type=tp,
                    help='DTMF sound sequence to use as marker (0-9 only)')
args = parser.parse_args()

fs = args.freq
dur_marker = args.dur
sequence = args.seq
outfile = 'marker_%s.wav' % ''.join(map(str, sequence))

user_freq = [697, 770, 852, 941,
             1209, 1336, 1477, 1633]

user_tones = {
    '0': (user_freq[3], user_freq[5]),
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

signals = []

for pat in sequence:
    f1, f2 = gen_freq(user_freq, user_tones, pat)
    signal = gen_sig(dur_marker, f1, f2, fs)
    signals.append(signal)

signal_blank = np.zeros_like(signals[0])
signals_w_blank = [signal_blank] * (len(signals) * 2 - 1)
signals_w_blank[0::2] = signals
signal_all = np.concatenate(signals_w_blank)

#signal_all *= 15000
signal_all /= np.max(np.abs(signal_all))
s16int_max = 2 ** 15 - 1
signal_all *= s16int_max
signal_all = np.int16(signal_all)

wavfile.write(outfile, fs, signal_all)
