from typing import *
import pandas as pd

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
    encoding = 'utf-8')

interactions = pd.DataFrame(columns = [
    'InteractionId',
    'DrugId',
    'DiseaseId',
    'Score',
    'Gene',
    'Type'])
sources = pd.DataFrame(columns = [
    'InteractionId',
    'Kind',
    'Score',
    'Source'])

# Id => Name
drugs = {}
# Id => (Name, Class)
diseases = {}

all_interaction_types = ['inhibitor', 'activator', 'antagonist', 'inducer']

for _, dgidb_row in dgidb_interactions.iterrows():
    gene_name = dgidb_row['gene_name']
    dgidb_interaction_types = list(filter(lambda x : x in all_interaction_types, str(dgidb_row['interaction_types']).split(',')))
    if not dgidb_interaction_types:
        continue

    disease_interactions = disgenet_interactions.loc[disgenet_interactions['geneSymbol'] == gene_name]
    if disease_interactions.empty:
        continue

    dgidb_score = dgidb_row['interaction_group_score']
    drug_id = dgidb_row['drug_concept_id']
    drug_name = dgidb_row['drug_name']

    drugs[drug_id] = drug_name

    for _, disgenet_row in disease_interactions.iterrows():
        disease_id = disgenet_row['diseaseId']
        disease_name = disgenet_row['diseaseName']
        disease_class = disgenet_row['diseaseClass']
        disgenet_score = disgenet_row['score']

        diseases[disease_id] = (disease_name, disease_class)

        ty = ''

        id = interactions.size
        interactions.append([
            id,
            drug_id,
            disease_id,
            dgidb_score * disgenet_score,
            gene_name,
            ty
        ])

        sources.append([
            id,
            'DGIDB',
            dgidb_score,
            f'https://dgidb.org/api/v2/interactions.json?genes={gene_name}&drugs={drug_id}'
        ])

    # drug_name = dgidb_row['drug_name']
