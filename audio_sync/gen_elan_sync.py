import sys
from DetectMarker import DetectMarker
import pympi.Elan
from pathlib import Path

# duration to check
duration = 60 * 5

infiles = sys.argv[1:]

d = DetectMarker(n_secs = duration)
#d = DetectMarker()
d.set_marker()

for infile in infiles:
    path = Path(infile)
    basename = path.stem
    print("processing syncronization", basename, file=sys.stderr)

    path_mp4 = basename + '.MP4'
    path_mp4_wav = basename + '_mp4.wav'
    path_wav = basename + '.wav'

    if not Path(path_mp4_wav).exists():
        print(path_mp4_wav, 'does not exist')
        sys.exit(1)
    if not Path(path_wav).exists():
        print(path_wav, 'does not exist')
        sys.exit(1)

    delay_wav, _, _ = d.detect(path_wav)
    delay_mp4, _, _ = d.detect(path_mp4_wav)
    delay = delay_wav - delay_mp4
    print("%s: %.3f (MP4: %.3f sec, wav: %.3f sec)" % (basename,
                                                       delay,
                                                       delay_mp4,
                                                       delay_wav))
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
            if delay > 0: media['TIME_ORIGIN'] = delay
        else:
            if delay < 0: media['TIME_ORIGIN'] = -delay

    path_eaf = basename + '.eaf'
    eaf.to_file(path_eaf)
