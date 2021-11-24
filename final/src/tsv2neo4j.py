from collections import defaultdict
import csv
import gzip
from typing import Dict, List

disease_classes: Dict[str, List[str]] = defaultdict(list)

print('Generating nodes.csv')
with open('../data/processed/neo4j/nodes.csv', 'w', newline='') as fout:
    out = csv.writer(fout)
    out.writerow(['id:ID', 'name', ':LABEL'])

    with gzip.open('../data/processed/tsv/drugs.tsv.gz', 'rt') as f:
        dict = csv.DictReader(f, delimiter='\t')
        out.writerows([[row['Id'], row['Name'], 'Drug'] for row in dict])

    with gzip.open('../data/processed/tsv/diseases.tsv.gz', 'rt') as f:
        dict = csv.DictReader(f, delimiter='\t')
        for row in dict:
            out.writerow([row['Id'], row['Name'], 'Disease'])
            for class_ in row['Class'].split(';'):
                disease_classes[class_].append(row['Id'])
    
    out.writerows([[x, x, 'Class'] for x in disease_classes])

print('Generating edges.csv')

activate: Dict[str, Dict[str, float]] = defaultdict(lambda : defaultdict(lambda : 0))
inhibit: Dict[str, Dict[str, float]] = defaultdict(lambda : defaultdict(lambda : 0))

with gzip.open('../data/processed/tsv/interactions.tsv.gz', 'rt') as f:
    dict = csv.DictReader(f, delimiter='\t')
    for row in dict:
        if row['Type'] != 1:
            inhibit[row['DiseaseId']][row['DrugId']] += float(row['Score'])
        else:
            activate[row['DiseaseId']][row['DrugId']] += float(row['Score'])

with open('../data/processed/neo4j/edges.csv', 'w', newline='') as fout:
    out = csv.writer(fout)
    out.writerow([':START_ID', ':END_ID', 'weight', ':TYPE'])

    for dis in inhibit:
        for drug in inhibit[dis]:
            out.writerow([drug, dis, inhibit[dis][drug], 'inhibits'])

    for dis in activate:
        for drug in activate[dis]:
            out.writerow([drug, dis, inhibit[dis][drug], 'activates'])

    for class_ in disease_classes:
        for dis in disease_classes[class_]:
            if dis and class_:
                out.writerow([dis, class_, None, 'belongs'])
