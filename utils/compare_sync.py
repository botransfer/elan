# 与えられた二つのeaf ファイルのメディア・同期情報を比較

import sys
import pympi.Elan
from urllib.parse import urlparse
from pathlib import Path

def get_name(url):
    a = urlparse(url)
    path = Path(a.path)
    return path.name

sys.argv.pop(0)
desc = {}

infile = sys.argv.pop(0)
eaf = pympi.Elan.Eaf(infile)
medias = eaf.media_descriptors
for media in medias:
    mime = media['MIME_TYPE']
    desc[mime] = {}
    desc[mime]['name'] = get_name(media['MEDIA_URL'])
    if 'TIME_ORIGIN' in media:
        desc[mime]['origin'] = media['TIME_ORIGIN']
infile1 = infile

infile = sys.argv.pop(0)
eaf = pympi.Elan.Eaf(infile)
medias = eaf.media_descriptors
for media in medias:
    mime = media['MIME_TYPE']
    if mime not in desc:
        print(mime, 'not in ', infile1)
        continue

    name = get_name(media['MEDIA_URL'])
    if name != desc[mime]['name']:
        print(mime, ': name differ:', name, desc[mime]['name'])

    if 'origin' in desc[mime]:
        if 'TIME_ORIGIN' in media:
            if media['TIME_ORIGIN'] != desc[mime]['origin']:
                print(mime, ': origin differ')
        else:
            print(mime, 'TIME_ORIGIN only in', infile1, '->', desc[mime]['TIME_ORIGIN'])
    else:
        if 'TIME_ORIGIN' in media:
            print(mime, 'TIME_ORIGIN only in', infile, '->', media['TIME_ORIGIN'])
        


