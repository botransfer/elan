# EAF ファイルのメディアパスを相対パスに変換する
# カレントディレクトリに、同じファイル名で出力するので、元のファイルは別のディレクトリに置いておくこと
# 例: python eaf_relative.py xxx/*.eaf

import sys
import pympi.Elan
from urllib.parse import urlparse
from pathlib import Path

def get_name(url):
    a = urlparse(url)
    path = Path(a.path)
    return path.name

sys.argv.pop(0)
infiles = sys.argv

for infile in infiles:
    path_in = Path(infile)
    path_out = Path(path_in.stem + ".eaf")
    if path_out.exists():
        print('output file', path_out, 'exists: skipping')
        continue

    eaf = pympi.Elan.Eaf(path_in)
    medias = eaf.media_descriptors
    for media in medias:
        name = get_name(media['MEDIA_URL'])
        media['MEDIA_URL'] = name
        media['RELATIVE_MEDIA_URL'] = './' + name
        if 'EXTRACTED_FROM' in media:
            del media['EXTRACTED_FROM']

    eaf.to_file(path_out)
