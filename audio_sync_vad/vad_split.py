from pyannote.audio import Pipeline
from pathlib import Path
from pydub import AudioSegment
import sys
import shutil

#AudioSegment.converter = "C:/home/Downloads/ffmpeg/bin/ffmpeg.exe"

sys.argv.pop(0)
infiles = sys.argv
for infile in infiles:
    print('processing', infile)
    path_in = Path(infile)
    dir_out = path_in.stem
    #shutil.rmtree(dir_out, ignore_errors=True)
    #Path(dir_out).mkdir(exist_ok=True)

    pipeline = Pipeline.from_pretrained("pyannote/voice-activity-detection")
    wav = AudioSegment.from_wav(path_in)

    # pyannote.core.annotation.Annotation
    vad_res = pipeline(path_in)
    # pyannote.core.timeline.Timeline
    timeline = vad_res.get_timeline()
    support = timeline.support()

    count = 0
    fo = open('%s_list.txt' % dir_out, 'w')
    # pyannote.core.segment.Segment
    for seg in support:
        # convert to ms
        t_start = seg.start * 1000
        t_end = seg.end * 1000

        # export to file
        a_seg = wav[t_start:t_end]
        outfile = '%s_seg%02d.wav' % (dir_out, count)
        a_seg.export(outfile, 
                     format='wav', parameters=['-sample_fmt', 's16', '-ar', '16000'])
        fo.write('%d,%f,%f\n' % (count, t_start, t_end))
        count += 1
    fo.close()
