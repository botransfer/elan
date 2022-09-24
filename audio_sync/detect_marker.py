import sys
import os
from DetectMarker import DetectMarker

if __name__ == '__main__':
    args = sys.argv
    args.pop(0)
    if len(args) != 3:
        msg = "usage: %s <marker> <wav 1> <wav 2>" % args[0]
        raise SystemExit(msg)

    d = DetectMarker()

    filename_marker = args.pop(0)
    d.set_marker(filename_marker)

    delays = []
    for filename in args:
        delay, _, _ = d.detect(filename)
        fname = os.path.basename(filename).replace('_mp4.wav', '.mp4')
        print("%s: marker found at: %.3f sec" % (fname, delay))
        delays.append(delay)
    print("diff: %.3f sec" % (delays[0] - delays[1]))

