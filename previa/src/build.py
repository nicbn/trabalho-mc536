import pandas as pd

dgidb_interactions = pd.read_csv(
    '../data/dgidb/interactions.tsv',
    sep = '\t',
    encoding = 'utf-8')

disgenet_interactions = pd.read_csv(
    '../data/disgenet/all_gene_disease_associations.tsv',
    sep = '\t',
    encoding = 'utf-8'
)

print(disgenet_interactions)
