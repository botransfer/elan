import sys
from pathlib import Path

sys.argv.pop(0)
infiles = sys.argv

for infile in infiles:
    print(infile)
    path_in = Path(infile)
    path_out = path_in.stem.replace('anon', 'anon_noheader') + '.txt'
    if path_in.stem == path_out:
        print('BAD outfile:', path_out)
        sys.exit(1)

    fo = open(path_out, 'w')
    with open(path_in) as f:
        for line in f:
            try:
                header, content = line.split(': ', 1)
            except:
                content = '\n'
            fo.write(content)
    fo.close()
