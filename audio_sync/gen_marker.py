import argparse
import numpy as np
from scipy.io import wavfile

freq_low = [697, 770, 852, 941]
freq_high = [1209, 1336, 1477, 1633]
tone_map = '123A456B789C*0#D'

def map_DTMF(seq_str):
    return list(map(tone_map.index, [*seq_str]))

def check_DTMF(seq_str):
    seq_str = seq_str.upper()
    map_DTMF(seq_str)
    return seq_str

parser = argparse.ArgumentParser(description='generate marker wave file',
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-freq',
                    default=44100,
                    type=int,
                    help='sampling frequency')
parser.add_argument('-dur',
                    default=0.25,
                    type=float,
                    help='duration of single tone in seconds')
parser.add_argument('seq', nargs='*',
                    default='1738',
                    type=check_DTMF,
                    help='DTMF key sequence to use as marker')
args = parser.parse_args()
fs = args.freq
dur_marker = args.dur
if not isinstance(args.seq , list):
    args.seq = [args.seq]

def get_freq(ind):
    #ind = tone_map.index(pat)
    f1 = freq_low[int(ind / 4)]
    f2 = freq_high[ind % 4]
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

for seq_str in args.seq:
    sequence = map_DTMF(seq_str)
    outfile = 'marker_%s.wav' % seq_str
    signals = []
    for ind in sequence:
        f1, f2 = get_freq(ind)
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

    print('out:', outfile)
    wavfile.write(outfile, fs, signal_all)
