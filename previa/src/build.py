import pandas as pd

dgidb_interactions = pd.read_csv(
    '../data/external/dgidb/interactions.tsv.gz',
    sep = '\t',
    compression = 'gzip',
    encoding = 'utf-8')

disgenet_interactions = pd.read_csv(
    '../data/external/disgenet/all_gene_disease_associations.tsv.gz',
    sep = '\t',
    compression = 'gzip',
    encoding = 'utf-8'
)

print(disgenet_interactions)
