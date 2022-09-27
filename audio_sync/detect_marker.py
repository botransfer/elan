import argparse
from DetectMarker import DetectMarker

parser = argparse.ArgumentParser(description='detect marker wave pattern',
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('marker')
parser.add_argument('infiles', nargs='+')
args = parser.parse_args()

d = DetectMarker()
d.set_marker(args.marker)

delays = []
for filename in args.infiles:
    delay, _, _ = d.detect(filename)
    print("%s: marker found at: %.3f sec" % (filename, delay))
    delays.append(delay)
    if len(delays) > 1:
        print("  diff: %.3f sec" % (delay - delays[0]))

