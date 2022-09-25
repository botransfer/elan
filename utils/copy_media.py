# eaf のメディア情報を別のeaf にコピーする
# TIME_ORIGIN の変化により、アノテーションの時刻をシフトする
# アノテーションは音声ファイル（audio/x-wav)に対するものと仮定

# usage: python copy_media.py <eaf_w_media> <eaf> <outfile>

import sys
import pympi.Elan
from urllib.parse import urlparse
from pathlib import Path

sys.argv.pop(0)

def get_name(url):
    a = urlparse(url)
    path = Path(a.path)
    return path.name

origins = {}
infile = sys.argv.pop(0)
eaf = pympi.Elan.Eaf(infile)
medias = eaf.media_descriptors
for media in medias:
    name = get_name(media['MEDIA_URL'])
    media['MEDIA_URL'] = name
    media['RELATIVE_MEDIA_URL'] = './' + name
    if 'EXTRACTED_FROM' in media:
        del media['EXTRACTED_FROM']

    mime = media['MIME_TYPE']
    if 'TIME_ORIGIN' in media:
        origins[mime] = int(media['TIME_ORIGIN'])
    else:
        origins[mime] = 0

origin = origins['audio/x-wav']

infile_base = infile
eaf_base = eaf
infile = sys.argv.pop(0)
eaf = pympi.Elan.Eaf(infile)
medias = eaf.media_descriptors
for media in medias:
    mime = media['MIME_TYPE']
    if mime == 'audio/x-wav':
        if 'TIME_ORIGIN' in media:
            origin_old = int(media['TIME_ORIGIN'])
        else:
            origin_old = 0

if origin != origin_old:
    origin_diff = origin - origin_old
    res = eaf.shift_annotations(-origin_diff)
    if len(res[0]) > 0:
        print(infile, len(res[0]), 'annotations squashed')
        print(res[0])
    if len(res[1]) > 0:
        print(infile, len(res[1]), 'annotations removed')
        print(res[1])

eaf.media_descriptors = eaf_base.media_descriptors
eaf.clean_time_slots()
outfile = sys.argv.pop(0)
eaf.to_file(outfile)
