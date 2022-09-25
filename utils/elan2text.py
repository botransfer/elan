import pympi.Elan
import pandas as pd
import sys
from pathlib import Path
import csv

sys.argv.pop(0)
infiles = sys.argv

for infile in infiles:
    path_in = Path(infile)
    eaf = pympi.Elan.Eaf(path_in)

    def get_time(id):
        return eaf.timeslots[id]

    def correct_speech(str):
        str = str.replace('\n', '')
        str = str.replace('\r', '')
        #str = str.replace('　', ' ')
        str = str.replace('、 ', '、')
        str = str.replace(' 、', '、')
        str = str.strip()
        return str
    
    name_conv = {
        'テレノイド発話': 'Op',
        '発話': 'Sj',
    }
    dfs = []
    for tier_name in eaf.tiers.keys():
        if tier_name not in name_conv: continue
        name = name_conv[tier_name]
        tier = eaf.tiers[tier_name][0]
        vals = [ ('%s/%s' % (name, key),) + value[:-1] for key, value in tier.items() ]
        df  = pd.DataFrame(vals, columns=['id', 'start', 'end', 'speech'])
        df['start'] = df['start'].apply(get_time)
        df['end'] = df['end'].apply(get_time)
        df['speech'] = df['speech'].apply(correct_speech)
        dfs.append(df)

    df = pd.concat(dfs)
    df = df.sort_values('start')
    df = df.reset_index(drop=True)

    path_out = path_in.stem + "_id.txt"
    #df.to_csv(path_out, columns=['id', 'speech'], sep=" ", index=False, header=False, quoting=csv.QUOTE_NONE)
    with open(path_out, 'w') as fo:
        for row in df.itertuples(index=False, name='Pandas'):
            line = '%s: %s\n' % (row.id, row.speech)
            fo.write(line)
