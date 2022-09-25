import spacy
import sys
from pathlib import Path
import json
import string

sys.argv.pop(0)
infiles = sys.argv

spacy.prefer_gpu()
#spacy.require_gpu()
#spacy.require_cpu()

#nlp = spacy.load('ja_ginza')
nlp = spacy.load('ja_ginza_electra')

def get_anon():
    global ind_anon
    s = string.ascii_uppercase[ind_anon]
    ind_anon += 1
    return s

for infile in infiles:
    path_in = Path(infile)
    path_out = path_in.stem + "_ner.txt"

    persons = {}
    list_doc = []
    ind_anon = 0

    with open(path_in) as f:
        for line in f:
            header, line = line.split(': ', 1)
            line = line.strip()
            doc = nlp(line)
            list_doc.append([header, doc])
            for ent in doc.ents:
                if ent.label_.lower() == 'person': # and ent.text != 'タロウ':
                    _name = '//'.join([token.text for token in ent])
                    if _name not in persons: persons[_name] = 0
                    persons[_name] += 1

    fo = open(path_out, 'w')
    fo.write(json.dumps(persons, ensure_ascii=False, sort_keys=True, indent=4) + '\n')

    person_conv = {}
    for person in persons:
        # XXX: '5' は特に根拠なく決めている
        if persons[person] < 5: continue
        person_conv[person] = get_anon()

    for person in person_conv:
        del persons[person]

    for person in persons:
        p_new = None
        for pp in person_conv:
            if pp in person:
                # 山田太郎 -> ['山田', '']
                _list = person.split(pp)
                _rep = get_anon()
                # ['山田', ''] -> ['B', '']
                _list = [_rep if x != '' else x for x in _list]
                # ['B', ''] -> 'BA'
                p_new = person_conv[pp].join(_list)
        if p_new is not None:
            person_conv[person] = p_new

    fo.write(json.dumps(person_conv, ensure_ascii=False, sort_keys=True, indent=4) + '\n')

    for header, doc in list_doc:
        line_new = header + ': '
        list_token = [token for token in doc]
        for ent in doc.ents:
            if ent.label_.lower() == 'person':
                _name = '//'.join([token.text for token in ent])
                if _name not in person_conv: continue
                _name_anon = person_conv[_name] + doc[ent.end - 1].whitespace_
                list_token[ent.start:ent.end] = [ _name_anon ]
        for token in list_token:
            if type(token) == str:
                line_new += token
            else:
                line_new += token.text_with_ws

        a = []
        for person in person_conv:
            if person in line_new:
                a.append(person)
        if len(a) > 0:
            print(infile, a, line_new)
            for ent in doc.ents:
                print('  ', ent.text, ent.label_)

        fo.write('xx: ' + line_new + '\n')

    fo.close()

    # with open(path_out, 'w') as f:
    #     for item in persons:
    #         line, person = item
    #         f.write(line + "\n")
    #         f.write('- ' + person + "\n")
