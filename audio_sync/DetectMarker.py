from scipy.io import wavfile
from scipy import signal
import numpy as np

class DetectMarker:
    def __init__(self, n_secs = 60, n_chunk = 128, n_perseg = 1024):
        # number of seconds to check in the target audio file
        self.n_secs = n_secs
        # chunk size
        self.n_chunk = n_chunk
        # DFT window size
        # overwrap = nperseg - n_chunk
        self.n_perseg = n_perseg
        # frequencies to be checked
        self.DTMF_freqs = [697, 770, 852, 941, 1209, 1336, 1477, 1633]

        self.fs_marker = None
        self.marker = None
        
    def set_marker(self, filename = "marker.wav"):
        x_m, self.fs_marker = self.read_wav(filename)
        f, t, Sxx = self.get_spectrogram(x_m, self.fs_marker)
        # threshold, and add penalty for 'blank' areas
        marker = (Sxx > 0.5) * 2.0 - 1.0
        self.marker = np.flip(marker)

    def detect(self, filename):
        x, fs = self.read_wav(filename)
        if self.fs_marker != fs:
            msg = "sampling rate mismatch %d / %d: %s"
            raise SystemExit(msg % (self.fs_marker, fs, filename))
        if self.n_secs > 0:
            x = x[:fs * self.n_secs]
        f, t, data = self.get_spectrogram(x, fs)

        res = signal.fftconvolve(self.marker, data, mode='valid')[0]
        i_max = np.argmax(res)
        delay = t[i_max]
        return delay, t, res

    def get_spectrogram(self, x, fs):
        f, t, Sxx = signal.spectrogram(x, fs,
                                       nperseg = self.n_perseg,
                                       noverlap = self.n_perseg - self.n_chunk)
        freq_slice = np.where((f >= self.DTMF_freqs[0]-50) & (f <= self.DTMF_freqs[-1]+50))
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
    import sys
    import matplotlib.pyplot as plt

    args = sys.argv
    args.pop(0)
    if len(args) < 1:
        msg = "usage: %s [<duration>] <wav>" % args[0]
        raise SystemExit(msg)

    duration = 60
    if len(args) > 1:
        duration = int(args.pop(0))

    d = DetectMarker(n_secs=duration)
    d.set_marker()

    filename = args.pop(0)
    delay, t, res = d.detect(filename)
    print("%s: marker found at: %.3f sec" % (filename, delay))

    t_ = t[:len(res)]
    plt.plot(t_, res)
    plt.show()
