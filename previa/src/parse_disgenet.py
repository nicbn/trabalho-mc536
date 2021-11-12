import pandas as pd
from typing import Dict, List


class Evidence:
    def __init__(self, pmid: str, score: float):
        self.pmid = pmid
        self.score = score


class DisGeneInteraction:
    evidences: List[Evidence] = []

    def __init__(
            self,
            dis: str,
            dis_name: str,
            dis_class: List[str],
            ty: int):
        self.dis = dis
        self.dis_name = dis_name
        self.dis_class = dis_class
        self.ty = ty


def parse(genes: List[str], limit = None) -> Dict[str, List[DisGeneInteraction]]:
    # Indexado por gene

    print('Loading file', flush=True, end='')
    disgenet = pd.read_csv(
        '../data/external/disgenet/all_gene_disease_pmid_associations.tsv.gz',
        sep='\t',
        compression='gzip',
        encoding='utf-8')
    disgenet = disgenet.dropna()
    disgenet = disgenet[disgenet['geneSymbol'].isin(genes)]

    r: Dict[str, List[DisGeneInteraction]] = {}
    total = len(disgenet)

    last_pair = ('', '')
    last_interaction = None

    for number, (_, row) in enumerate(disgenet.iterrows()):
        if limit and number >= limit:
            break

        if number % 100 == 0 or number + 1 == total:
            print(f'\r{((number + 1) * 100 // total):d}% ({number + 1}/{total})', end='')

        gene = row['geneSymbol']
        dis_id = row['diseaseId']
        score = row['score']
        pmid = row['pmid']

        if last_pair == (gene, dis_id):
            last_interaction.evidences.append(Evidence(pmid, score))
            continue

        dis_n = row['diseaseName']
        dis_c = row['diseaseClass']

        arr = []
        try:
            arr = r[gene]
        except KeyError:
            r[gene] = arr

        interaction = DisGeneInteraction(dis_id, dis_n, str(dis_c).split(','))
        interaction.evidences.append(Evidence(pmid, score))

        arr.append(interaction)

        last_pair = (gene, dis_id)
        last_interaction = interaction

    print('\r')

    return r
