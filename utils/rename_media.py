# eaf のメディアファイル名をリネームする
# (メディアファイル自体はリネームしない）
# ついでにパスも相対化

# usage: python rename,py <infile> <outfile>
# <outfile> を上書きするので注意

import sys
import pympi.Elan
from urllib.parse import urlparse
from pathlib import Path

sys.argv.pop(0)
path_in = Path(sys.argv.pop(0))
path_out = Path(sys.argv.pop(0))

eaf = pympi.Elan.Eaf(path_in)
medias = eaf.media_descriptors
stem = path_out.stem
for media in medias:
    url = media['MEDIA_URL']
    media_path = Path(urlparse(url).path)
    suffix = media_path.suffix
    name = stem + suffix
    media['MEDIA_URL'] = name
    media['RELATIVE_MEDIA_URL'] = './' + name
    if 'EXTRACTED_FROM' in media:
        del media['EXTRACTED_FROM']

    name_orig = media_path.name
    print('mv', name_orig, name)
    
eaf.to_file(path_out)
