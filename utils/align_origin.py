# eaf ファイルのORIGIN を、mp4 もしくはwav のどちらかのTIME_ORIGIN が0 になるように調節する
# TIME_ORIGIN の変化により、アノテーションの時刻をシフトする
# アノテーションは音声ファイル（audio/x-wav)に対するものと仮定

# usage: python align_origin.py <eaf> <outfile>
import sys
import pympi.Elan
from urllib.parse import urlparse
from pathlib import Path

sys.argv.pop(0)
infile = sys.argv.pop(0)
outfile = sys.argv.pop(0)

origins = {}
eaf = pympi.Elan.Eaf(infile)
medias = eaf.media_descriptors
for media in medias:
    mime = media['MIME_TYPE']
    if 'TIME_ORIGIN' in media:
        origins[mime] = int(media['TIME_ORIGIN'])
    else:
        origins[mime] = 0
    if mime == 'audio/x-wav':
        origin_old = origins[mime]

if origins['video/mp4'] > origins['audio/x-wav']:
    origins['video/mp4'] -= origins['audio/x-wav']
    origins['audio/x-wav'] = 0
else:
    origins['video/mp4'] = 0
    origins['audio/x-wav'] -= origins['video/mp4']
for media in medias:
    mime = media['MIME_TYPE']
    media['TIME_ORIGIN'] = str(origins[mime])
origin = origins['audio/x-wav']

if origin != origin_old:
    origin_diff = origin - origin_old
    res = eaf.shift_annotations(-origin_diff)
    if len(res[0]) > 0:
        print(infile, len(res[0]), 'annotations squashed')
        print(res[0])
    if len(res[1]) > 0:
        print(infile, len(res[1]), 'annotations removed')
        print(res[1])

eaf.clean_time_slots()
eaf.to_file(outfile)
