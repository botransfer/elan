# eaf ファイルに同期情報 (TIME_ORIGIN) が入っているかどうかをチェックする

# usage: python check_origin.py <eaf> <eaf> ...

import sys
import pympi.Elan
from urllib.parse import urlparse
from pathlib import Path

sys.argv.pop(0)
infiles = sys.argv
for infile in infiles:
    eaf = pympi.Elan.Eaf(infile)
    medias = eaf.media_descriptors
    has_origin = False
    for media in medias:
        if 'TIME_ORIGIN' in media:
            origin = int(media['TIME_ORIGIN'])
        else:
            origin = 0
        if origin > 0: has_origin = True

    if not has_origin:
        print(infile, ': no origin')
