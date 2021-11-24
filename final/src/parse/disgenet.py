from typing import Dict, List
from collections import defaultdict
import csv


class Evidence:
    def __init__(self, pmid: str, score: float):
        self.pmid = pmid
        self.score = score


class DisGeneInteraction:
    def __init__(self, dis: str, evidences: List[Evidence], ty: int):
        self.evidences = evidences
        self.dis = dis
        self.ty = ty


class Dis:
    def __init__(self, name: str, c: List[str]):
        self.name = name
        self.classes = c


class Disgenet:
    interactions: Dict[str, List[DisGeneInteraction]] = defaultdict(list)
    dis: Dict[str, Dis] = {}


def parse() -> Disgenet:
    r = Disgenet()

    classes: Dict[str, List[str]] = {}
    names = {}

    with open('../data/external/disgenet/diseases.tsv', 'r') as f:
        for row in csv.DictReader(f, delimiter='\t'):
            classes[row['Id']] = []
            names[row['Id']] = row['Name']

    with open('../data/external/disgenet/classes.tsv', 'r') as f:
        for row in csv.DictReader(f, delimiter='\t'):
            classes[row['DiseaseId']].append(row['Class'])

    for dis in classes.keys():
        r.dis[dis] = Dis(names[dis], classes[dis])

    ty: Dict[(str, str), int] = {}
    evidence: Dict[(str, str), List[Evidence]] = defaultdict(list)

    with open('../data/external/disgenet/interactions.tsv', 'r') as f:
        for row in csv.DictReader(f, delimiter='\t'):
            gene = row['Gene']
            dis_id = row['DiseaseId']
            score = row['Score']
            pmid = row['PMID']
            this_ty = 1
            if row['Type'] == 'Therapeutic':
                this_ty = 0

            if pmid == 'None':
                continue

            if (dis_id, gene) not in ty:
                ty[(dis_id, gene)] = this_ty
            elif this_ty != ty[(dis_id, gene)]:
                ty[(dis_id, gene)] = None

            evidence[(dis_id, gene)].append(Evidence(pmid, float(score)))

    for (dis_id, gene), this_ty in ty.items():
        if this_ty != None:
            r.interactions[gene].append(DisGeneInteraction(
                dis_id, evidence[(dis_id, gene)], this_ty))

    return r
