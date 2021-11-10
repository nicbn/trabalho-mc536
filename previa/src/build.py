import pandas as pd

drug_alias = pd.DataFrame(columns = ['DrugAlias', 'DrugId'])
drug = pd.DataFrame(columns = ['DrugId', 'Name', 'Class'])
source = pd.DataFrame(columns = [
    'InteractionId',
    'TrustLevel',
    'Gene',
    'GeneDrugInteraction',
    'GeneDrugInteractionMechanism',
    'GeneDiseaseInteraction',
    'Source'
])
disease_alias = pd.DataFrame(columns = ['DiseaseAlias', 'DiseaseId'])
disease = pd.DataFrame(columns = ['DiseaseId', 'Name', 'Class'])
interaction = pd.DataFrame(columns = [
    'InteractionId',
    'DrugId',
    'DiseaseId',
    'InteractionType'
])

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

print(drug_alias)
