import librosa
import librosa.display
import matplotlib.pyplot as plt
from scipy import signal
import numpy as np
import sys
import pympi.Elan
from pathlib import Path
import json
from statistics import mean 

infile = sys.argv[1]
listfile = sys.argv[2]
markers = sys.argv[3:]

timestamps = []
with open(listfile) as f:
    for line in f:
        line = line.strip()
        [count, t_start, t_end] = line.split(',')
        timestamps.append([float(t_start) / 1000, float(t_end) / 1000])

# target audio
y, sr = librosa.load(infile, sr=None)
len_shift = sr // 1000
S = librosa.feature.melspectrogram(y=y,
                                   sr=sr,
                                   n_fft=512,
                                   hop_length=len_shift)
S = librosa.power_to_db(S, ref=np.max)
#S[S < -20] = -80
S = (S + 80) / 80

count = 0
delays = []
for marker in markers:
    ym, srm = librosa.load(marker, sr=None)
    if srm != sr:
        print('sampling rate mismatch')
        sys.exit(1)

    Sm = librosa.feature.melspectrogram(y=ym,
                                       sr=sr,
                                       n_fft=512,
                                        hop_length=len_shift)
    Sm = librosa.power_to_db(Sm, ref=np.max)
    Sm[Sm < -20] = -80
    Sm = (Sm + 80) / 80
    Sm_ = np.flipud(np.fliplr(Sm))

    res_ = signal.fftconvolve(Sm_, S, mode='valid')
    res = res_[0]
    i_max = np.argmax(res)
    offset = i_max * len_shift / sr
    a_start = timestamps[count][0]
    delay = float(offset - a_start)
    print(count, 'delay', delay, 'offset', offset, 'a_start', a_start)

    f_done = False
    for d in delays:
        dd = d[0]
        if abs(delay - dd) < 0.1:
            d[1].append(delay)
            d[0] = mean(d[1])
            f_done = True

    if not f_done:
        delays.append([delay, [delay] ])
    count += 1

    # X = np.arange(res.shape[0]) * len_shift / sr
    # plt.plot(X, res)
    # plt.show()

basename = infile.replace('_mp4.wav', '')
path_mp4 = basename + '.MP4'
path_wav = basename + '.wav'

delays_sorted = sorted(delays, key=lambda x: len(x[1]), reverse=True)
count_out = 0
for d in delays_sorted:
    n = len(d[1])
    if n == 1 and count_out > 0: continue
    delay = d[0]

    # generate elan file
    eaf = pympi.Elan.Eaf()
    eaf.remove_tier('default')
    eaf.add_tier('テレノイド対話')
    eaf.add_tier('発話')
    eaf.add_linked_file(path_mp4, relpath='./' + path_mp4, mimetype='video/mp4')
    eaf.add_linked_file(path_wav, relpath='./' + path_wav, mimetype='audio/x-wav')

    delay = int(round(delay * 1000.0))
    medias = eaf.media_descriptors
    for media in medias:
        mime = media['MIME_TYPE']
        if mime == 'audio/x-wav':
            if delay < 0: media['TIME_ORIGIN'] = -delay
        else:
            if delay > 0: media['TIME_ORIGIN'] = delay

    if count_out == 0:
        path_eaf = basename + '.eaf'
    else:
        path_eaf = basename + '%d.eaf' % count_out
    eaf.to_file(path_eaf)
    count_out += 1
    
