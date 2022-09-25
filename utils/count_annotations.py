# TIER ごとのannotation を数える

import sys
import pympi.Elan
from urllib.parse import urlparse
from pathlib import Path

name_conv = {
    'テレノイド発話': 'Op',
    '発話': 'Sj',
}

sys.argv.pop(0)
infiles = sys.argv

for infile in infiles:
    eaf = pympi.Elan.Eaf(infile)
    for tier_name in eaf.tiers.keys():
        # if tier_name not in name_conv: continue
        tier = eaf.tiers[tier_name][0]
        n = len(list(tier.keys()))
        if n > 0:
            print(infile, tier_name, n)
