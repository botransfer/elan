import sys
from pathlib import Path

sys.argv.pop(0)
infiles = sys.argv

for infile in infiles:
    path_in = Path(infile)
    path_out = path_in.stem.replace('id_ner', 'anon') + '.txt'
    if path_in.stem == path_out:
        print('BAD outfile:', path_out)
        sys.exit(1)

    fo = open(path_out, 'w')
    with open(path_in) as f:
        for line in f:
            line = line.strip()
            if line.startswith('xx: '):
                line = line.replace('xx: ', '')
                fo.write(line + '\n')
    fo.close()
