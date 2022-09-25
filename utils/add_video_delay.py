# eaf のメディア情報のうち、mp4 の分をずらし、ブランクを入れたmp4ファイルに変更する
# usage: python add_video_delay.py <delay(sec)> <ブランクを入れたmp4> <元のeaf> <出力eaf>

import sys
import pympi.Elan
from urllib.parse import urlparse
from pathlib import Path

sys.argv.pop(0)
delay = int(sys.argv.pop(0))
file_mp4 = sys.argv.pop(0)
infile = sys.argv.pop(0)
outfile = sys.argv.pop(0)

eaf = pympi.Elan.Eaf(infile)
medias = eaf.media_descriptors
for media in medias:
    mime = media['MIME_TYPE']
    if mime == 'video/mp4':
        media['MEDIA_URL'] = file_mp4
        media['RELATIVE_MEDIA_URL'] = './' + file_mp4
        if 'EXTRACTED_FROM' in media:
            del media['EXTRACTED_FROM']

        if 'TIME_ORIGIN' in media:
            origin = int(media['TIME_ORIGIN'])
        else:
            origin = 0
        origin += delay * 1000
        media['TIME_ORIGIN'] = origin

eaf.to_file(outfile)
