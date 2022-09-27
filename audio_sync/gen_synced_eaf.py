import argparse
import sys
import mimetypes
from DetectMarker import DetectMarker
import pympi.Elan
from pathlib import Path

parser = argparse.ArgumentParser(description='generate synchronized ELAN file',
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-marker', default='marker.wav',
                    help='marker filename')
parser.add_argument('-dur', default=60 * 5,
                    help='duration to check marker pattern (seconds). Specify 0 to check the whole file')
parser.add_argument('infiles', nargs='+',
                    help='audio files to synchronize')
parser.add_argument('-out', default='-',
                    help='resulting eaf filename. Specify "-" for stdout')
args = parser.parse_args()

marker = args.marker
duration = args.dur
infiles = args.infiles
outfile = args.out

d = DetectMarker(n_secs=duration)
d.set_marker(marker)

# detect marker position
delays = []
for infile in infiles:
    delay, _, _ = d.detect(infile)
    delays.append([infile, delay])
infile_min, delay_min = min(delays, key=lambda x: x[1])

# generate elan file
eaf = pympi.Elan.Eaf()
delay_map = {}
for e in delays:
    infile, delay = e
    infile_conv = infile.replace('_mp4.wav', '.mp4')
    mime = mimetypes.guess_type(infile_conv)[0]
    if infile != infile_min:
        delay_ms = int(round((delay - delay_min) * 1000.0))
        eaf.add_linked_file(infile_conv, mimetype=mime, time_origin=delay_ms)
    else:
        eaf.add_linked_file(infile_conv, mimetype=mime)

eaf.to_file(outfile)
