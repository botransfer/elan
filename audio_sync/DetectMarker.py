from scipy.io import wavfile
from scipy import signal
import numpy as np

class DetectMarker:
    def __init__(self, n_secs = 60, n_chunk = 128, n_perseg = 1024):
        # number of seconds to check in the target audio file
        self.n_secs = n_secs
        # DFT window size
        self.n_perseg = n_perseg
        # overwrap
        if n_chunk is None:
            self.n_overwrap = None
        else:
            self.n_overwrap = n_perseg - n_chunk
        # frequencies to be checked
        self.DTMF_freqs = [697, 770, 852, 941, 1209, 1336, 1477, 1633]

        self.fs_marker = None
        self.marker = None
        
    def set_marker(self, filename = "marker.wav"):
        x_m, self.fs_marker = self.read_wav(filename)
        f, t, Sxx = self.get_spectrogram(x_m, self.fs_marker)
        # threshold, and add penalty for 'blank' areas
        marker = (Sxx > 0.5) * 2.0 - 1.0
        #marker = (Sxx > 0.5).astype(int) * 2.0 - 1.0

        # flip for convolution
        self.marker = np.flipud(np.fliplr(marker))

    def detect(self, filename):
        x, fs = self.read_wav(filename)
        if self.fs_marker != fs:
            msg = "sampling rate mismatch %d / %d: %s"
            raise SystemExit(msg % (self.fs_marker, fs, filename))

        t_offset = 0
        if self.n_secs > 0:
            x = x[:fs * self.n_secs]
        elif self.n_secs < 0:
            len_cut = fs * self.n_secs
            t_offset = (len(x) + len_cut) / fs
            x = x[len_cut:]
        f, t, data = self.get_spectrogram(x, fs)

        res = signal.convolve(self.marker, data, mode='valid')[0]
        i_max = np.argmax(res)
        t += t_offset
        delay = t[i_max]
        return delay, t, res

    def get_spectrogram(self, x, fs):
        f, t, Sxx = signal.spectrogram(x, fs,
                                       nperseg = self.n_perseg,
                                       noverlap = self.n_overwrap)
        #freq_slice = np.where((f >= self.DTMF_freqs[0]-50) & (f <= self.DTMF_freqs[-1]+50))
        freq_slice = np.where(f >= 500)
        f = f[freq_slice]
        Sxx = Sxx[freq_slice,:][0]
        Sxx = Sxx / np.max(Sxx)
        return f, t, Sxx

    def read_wav(self, filename):
        try:
            fs, signal = wavfile.read(filename)
        except Exception:
            msg = 'Failed to open wav file "%s"'
            raise SystemExit(msg % filename)

        if signal.dtype != 'int16':
            msg = 'expected `int16` data in .wav file %s'
            raise AttributeError(msg % filename)
        # use Ch2 if stereo
        if len(signal.shape) == 2 and signal.shape[1] == 2:
            signal = signal.transpose()
            signal = signal[1]

        return signal, fs


if __name__ == '__main__':
    import argparse
    import matplotlib.pyplot as plt

    parser = argparse.ArgumentParser(description='detect marker and plot likelihood',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('marker', help='marker wavefile')
    parser.add_argument('infile', help='wavefile(s) to detect marker')
    parser.add_argument('-dur',
                        default=0,
                        type=int,
                        help='''\
    duration to check marker pattern (in seconds).
    x > 0: check first x seconds of target file.
    x == 0: check the whole file.
    x < 0: check last x seconds of target file.''')
    args = parser.parse_args()

    # check whole audio
    d = DetectMarker(n_secs=args.dur)
    d.set_marker(args.marker)

    infile = args.infile
    delay, t, res = d.detect(infile)
    print("%s: marker found at: %.3f sec" % (infile, delay))

    t_ = t[:len(res)]
    plt.plot(t_, res)
    plt.show()
