from typing import Dict, List
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

class DrugGenePair:
    def __init__(self, drug: str, gene: str, drug_name: str):
        self.gene = gene
        self.drug = drug
        self.drug_name = drug_name
    def __eq__(self, x):
        return self.gene == x.gene and self.drug == x.drug
    def __hash__(self):
        return hash(self.gene) ^ hash(self.drug)
    def __repr__(self):
        return str([self.gene, self.drug_name])

class DrugGeneInteraction:
    def __init__(self, ty: int, score: float, pmids: List[str]):
        self.ty = ty
        self.pmids = pmids
        self.score = score
    def __repr__(self):
        return str({
            'ty': self.ty,
            'pmids': self.pmids,
            'score': self.score
        })

dgidb_interaction_types = {
    "activator": 1,
    "agonist": 1,
    "binder": 1,
    "chaperone": 1,
    "inducer": 1,
    "partial agonist": 1,
    "potentiator": 1,
    "stimulator": 1,
    "substrate": 1,

    "antagonist": 0,
    "antibody": 0,
    "antisense oligonucleotide": 0,
    "blocker": 0,
    "inhibitor": 0,
    "inhibitory allosteric modulator": 0,
    "inverse agonist": 0,
    "partial antagonist": 0,
    "suppressor": 0
}

def parse() -> Dict[DrugGenePair, DrugGeneInteraction]:
    dgidb = pd.read_csv(
        '../data/external/dgidb/interactions.tsv.gz',
        sep = '\t',
        compression = 'gzip',
        encoding = 'utf-8')
    dgidb = dgidb.dropna()
    scaler = MinMaxScaler()
    dgidb[['interaction_group_score']] = scaler.fit_transform(dgidb[['interaction_group_score']])

    r = {}

    for _, row in dgidb.iterrows():
        drug = row['drug_concept_id']
        gene = row['gene_name']
        drug_name = row['drug_name']
        pmids = str(row['PMIDs']).split(',')
        score = row['interaction_group_score']

        types = str(row['interaction_types']).split(',')
        ty = None
        for x in types:
            try:
                y = dgidb_interaction_types[x]
                if ty == None or ty == y:
                    ty = y
                else:
                    ty = None
                    break
            except KeyError:
                pass
        if ty == None:
            continue

        pair = DrugGenePair(drug, gene, drug_name)
        r[pair] = DrugGeneInteraction(ty, score, pmids)
    return r
