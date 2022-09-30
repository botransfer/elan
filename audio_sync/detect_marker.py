import argparse
import textwrap
from DetectMarker import DetectMarker

parser = argparse.ArgumentParser(description='detect marker wave pattern',
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('marker', help='marker wavefile')
parser.add_argument('infiles', nargs='+', help='wavefile(s) to detect marker')
parser.add_argument('-dur',
                    default=60,
                    type=int,
                    help='''\
duration to check marker pattern (in seconds).
x > 0: check first x seconds of target file.
x == 0: check the whole file.
x < 0: check last x seconds of target file.''')
args = parser.parse_args()

d = DetectMarker(n_secs=args.dur)
d.set_marker(args.marker)

delays = []
for filename in args.infiles:
    delay, _, _ = d.detect(filename)
    print("%s: marker found at: %.3f sec" % (filename, delay))
    delays.append(delay)
    if len(delays) > 1:
        print("  diff: %.3f sec" % (delay - delays[0]))

