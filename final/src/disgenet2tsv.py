import sqlite3
from typing import Dict
from parse import dgidb
import os

try:
    os.mkdir('../data/external/disgenet')
except FileExistsError:
    pass

genes = list(dgidb.parse().keys())

with sqlite3.connect('../data/raw/disgenet.db') as conn:
    diseases_id: Dict[int, str] = {}

    print('Generating diseases')
    with open('../data/external/disgenet/diseases.tsv', 'w') as f:
        f.write('Id\tName\n')
        for nid, id, name in conn.execute(
                'SELECT diseaseNID, diseaseId, diseaseName FROM diseaseAttributes'):
            diseases_id[nid] = id
            f.write(f'{id}\t{name}\n')

    print('Generating classes')
    with open('../data/external/disgenet/classes.tsv', 'w') as f:
        f.write('DiseaseId\tClass\n')
        for disease, c in conn.execute(
            'SELECT d2c.diseaseNID, dc.diseaseClass'
            + ' FROM disease2class AS d2c, diseaseClass AS dc'
                + ' WHERE d2c.diseaseClassNID = dc.diseaseClassNID'):
            f.write(f'{diseases_id[disease]}\t{c}\n')

    print('Generating interactions')
    with open('../data/external/disgenet/interactions.tsv', 'w') as f:
        f.write('DiseaseId\tGene\tScore\tPMID\tType\n')
        for (number, gene) in enumerate(genes):
            print(f'\r{(number + 1) * 100 // len(genes)} % ({number + 1} / {len(genes)})', end='')
            for disease, type, pmid, score in conn.execute(
                'SELECT d.diseaseNID, d.associationType, d.pmid, d.score'
                    + ' FROM geneDiseaseNetwork AS d, geneAttributes as g'
                    + ' WHERE g.geneName = ? AND g.geneNID = d.geneNID', [gene]):
                f.write(f'{diseases_id[disease]}\t{gene}\t{score}\t{pmid}\t{type}\n')
