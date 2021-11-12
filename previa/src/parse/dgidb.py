from typing import Dict, List
import pandas as pd
from sklearn.preprocessing import MinMaxScaler


class DrugGeneInteraction:
    def __init__(self, drug: str, drug_name: str, ty: int, score: float, pmids: List[str]):
        self.drug = drug
        self.drug_name = drug_name
        self.ty = ty
        self.pmids = pmids
        self.score = score

    def __repr__(self):
        return str({
            'drug': self.drug_name,
            'ty': self.ty,
            'pmids': self.pmids,
            'score': self.score
        })


dgidb_interaction_types = {
    'activator': 1,
    'agonist': 1,
    'binder': 1,
    'chaperone': 1,
    'inducer': 1,
    'partial agonist': 1,
    'potentiator': 1,
    'stimulator': 1,
    'substrate': 1,

    'antagonist': 0,
    'antibody': 0,
    'antisense oligonucleotide': 0,
    'blocker': 0,
    'inhibitor': 0,
    'inhibitory allosteric modulator': 0,
    'inverse agonist': 0,
    'partial antagonist': 0,
    'suppressor': 0
}


def parse() -> Dict[str, List[DrugGeneInteraction]]:
    # Indexado por gene

    dgidb = pd.read_csv(
        '../data/external/dgidb/interactions.tsv',
        sep='\t',
        encoding='utf-8')
    dgidb = dgidb.dropna()
    scaler = MinMaxScaler()
    dgidb[['interaction_group_score']] = scaler.fit_transform(
        dgidb[['interaction_group_score']])

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

        arr = []
        try:
            arr = r[gene]
        except KeyError:
            r[gene] = arr

        arr.append(DrugGeneInteraction(drug, drug_name, ty, score, pmids))
    
    return r
