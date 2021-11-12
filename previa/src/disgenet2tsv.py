import sqlite3
import pandas as pd
from typing import Dict
from parse import dgidb
import os

try:
    os.mkdir('../data/interim/disgenet')
except FileExistsError:
    pass

genes = list(dgidb.parse().keys())

with sqlite3.connect('../data/external/disgenet.db') as conn:
    diseases_id: Dict[int, str] = {}
    classes = pd.DataFrame(columns=['DiseaseId', 'Class'])
    diseases = pd.DataFrame(columns=['Id', 'Name'])

    print('Generating diseases')
    for nid, id, name in conn.execute(
            'SELECT diseaseNID, diseaseId, diseaseName FROM diseaseAttributes'):
        diseases_id[nid] = id
        diseases.append([id, name])

    print('Generating classes')
    for disease, c in conn.execute(
        'SELECT d2c.diseaseNID, dc.diseaseClass'
        + ' FROM disease2class AS d2c, diseaseClass AS dc'
            + ' WHERE d2c.diseaseClassNID = dc.diseaseClassNID'):
        classes.append([diseases_id[disease], c])

    interactions = pd.DataFrame(
        columns=['DiseaseId', 'Gene', 'Score', 'PMID', 'Type'])

    print('Generating interactions')
    for gene in genes:
        for disease, type, pmid, score in conn.execute(
            'SELECT d.diseaseNID, d.associationType, d.pmid, d.score'
                + ' FROM geneDiseaseNetwork AS d, geneAttributes as g'
                + ' WHERE g.geneName = ? AND g.geneNID = d.geneNID', [gene]):
            interactions.append(
                [diseases_id[disease], gene, score, pmid, type])

    classes.to_csv('../data/interim/disgenet/classes.tsv', sep='\t')
    diseases.to_csv('../data/interim/disgenet/diseases.tsv', sep='\t')
    interactions.to_csv('../data/interim/disgenet/interactions.tsv', sep='\t')
