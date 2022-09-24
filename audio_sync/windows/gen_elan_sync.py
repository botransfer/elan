import sys
import os
import subprocess
import glob
from DetectMarker import DetectMarker

# duration to check
duration = 60 * 5

args = sys.argv
args.pop(0)

d = DetectMarker(n_secs = duration)
d.set_marker()

f = open('template_older_panel.eaf', "r", encoding='utf-8')
elan_template = f.read()
f.close()

# expand glob for Windows cmd
files = []
for f in args:
    files.extend(glob.glob(f))
    print(files)

for path in files:
    path = os.path.abspath(path)
    targetdir, filename = os.path.split(path)
    basename = os.path.splitext(filename)[0]
    print("processing syncronization", basename)

    f_mp4 = basename + ".MP4"
    f_wav = basename + ".wav"
    path_mp4 = os.path.join(targetdir, f_mp4)
    path_wav = os.path.join(targetdir, f_wav)
    path_tmp = "tmp.wav"

    # generate wav from mp4
    cmd = "ffmpeg -y -i %s -vn -ac 1 -ar 44100 -acodec pcm_s16le -f wav -t %d %s" % (path_mp4, duration, path_tmp)
    try:
        #print('running: ', cmd)
        result = subprocess.run(cmd,
                                shell=True,
                                check=True,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                universal_newlines=True)
    except subprocess.CalledProcessError:
        print('FFmpeg error for ', f)
        print(file=sys.stderr)
        exit(1)

    delay_wav, _, _ = d.detect(path_wav)
    delay_mp4, _, _ = d.detect(path_tmp)
    delay = delay_wav - delay_mp4
    print("%s: %.3f (MP4: %.3f sec, wav: %.3f sec)" % (basename,
                                                       delay,
                                                       delay_mp4,
                                                       delay_wav))
    os.remove(path_tmp)

    # generate elan file
    d_mp4 = 0
    d_wav = 0
    delay = int(round(delay * 1000.0))
    if delay > 0:
        d_wav = delay
    else:
        d_mp4 = -delay

    txt = elan_template
    txt = txt.replace('__BASENAME__', basename)
    txt = txt.replace('__DELAY_MP4__', str(d_mp4))
    txt = txt.replace('__DELAY_WAV__', str(d_wav))
    
    path_elan = os.path.join(targetdir, basename + "_sync.eaf")

    if os.path.exists(path_elan):
       msg = "Error: ELAN file exists: %s"
       raise SystemExit(msg % (path_elan))
        
    f = open(path_elan, "w", encoding='utf-8')
    f.write(txt)
    f.close()
