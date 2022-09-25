# 二つのelan ファイルをマージ
# 最初のファイルに遅延情報（TIME_ORIGIN）が設定されていると仮定
# また、アノテーションは音声ファイル（audio/x-wav)に対するものと仮定
# ついでにMEDIA_URL の相対パス化も行う

# usage: python merge.py <infile1> <infile2> <outfile>

import sys
import pympi.Elan
from urllib.parse import urlparse
from pathlib import Path

sys.argv.pop(0)

def get_name(url):
    a = urlparse(url)
    path = Path(a.path)
    return path.name

origin = None
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
    if mime == 'audio/x-wav':
        if 'TIME_ORIGIN' in media:
            origin = int(media['TIME_ORIGIN'])
        else:
            print('warning: TIME_ORIGIN not found in wav track of', infile)

infile_base = infile
eaf_base = eaf

infile = sys.argv.pop(0)
eaf = pympi.Elan.Eaf(infile)
if origin is not None:
    res = eaf.shift_annotations(-origin)
    if len(res[0]) > 0:
        print(infile, len(res[0]), 'annotations squashed')
        print(res[0])
    if len(res[1]) > 0:
        print(infile, len(res[1]), 'annotations removed')
        print(res[1])

for tier_name in eaf.tiers.keys():
    eaf.copy_tier(eaf_base, tier_name)

# change order
tier_names = list(eaf_base.tiers.keys())
ordinal = 0
for tier_name in ['発話', 'テレノイド発話']:
    d = eaf_base.tiers[tier_name]
    eaf_base.tiers[tier_name] = (d[0], d[1], d[2], ordinal)
    ordinal += 1
    tier_names.remove(tier_name)
for tier_name in tier_names:
    d = eaf_base.tiers[tier_name]
    eaf_base.tiers[tier_name] = (d[0], d[1], d[2], ordinal)
    ordinal += 1

eaf_base.clean_time_slots()
outfile = sys.argv.pop(0)
eaf_base.to_file(outfile)
