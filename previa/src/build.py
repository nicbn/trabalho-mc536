import pandas as pd

'''
drug_alias = pd.DataFrame(columns = ['DrugAlias', 'DrugId'])
disease_alias = pd.DataFrame(columns = ['DiseaseAlias', 'DiseaseId'])
'''

# gene_name
# gene_claim_name
# entrez_id
# interaction_claim_source
# interaction_types
# drug_claim_name
# drug_claim_primary_name
# drug_name
# drug_concept_id
# interaction_group_score
# PMIDs
dgidb_interactions = pd.read_csv(
    '../data/external/dgidb/interactions.tsv.gz',
    sep = '\t',
    compression = 'gzip',
    encoding = 'utf-8')

# geneId
# geneSymbol
# DSI
# DPI
# diseaseId
# diseaseName
# diseaseType
# diseaseClass
# diseaseSemanticType
# score
# EI
# YearInitial
# YearFinal
# NofPmids
# NofSnps
# source
disgenet_interactions = pd.read_csv(
    '../data/external/disgenet/all_gene_disease_associations.tsv.gz',
    sep = '\t',
    compression = 'gzip',
    encoding = 'utf-8'
)

disease = pd.DataFrame(columns = ['DiseaseId', 'Name', 'Class'])
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
interaction = pd.DataFrame(columns = [
    'InteractionId',
    'DrugId',
    'DiseaseId',
    'InteractionType'
])

for row in dgidb_interactions:
    pass

print(drug_alias)
