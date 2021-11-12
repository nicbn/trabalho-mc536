import timeit
import gzip
from parse import dgidb, disgenet
from statistics import mean
import os

try:
    os.mkdir('../data/processed')
except FileExistsError:
    pass

start = timeit.default_timer()

print('Parsing DGIDB')
dgidb_ = dgidb.parse()

print('Parsing DISGENET')
disgenet_ = disgenet.parse()

dgidb_.interactions = {x: dgidb_.interactions[x]
                       for x in disgenet_.interactions.keys()}

print('Generating drugs')
with gzip.open('../data/processed/drugs.tsv.gz', 'wt') as f:
    f.write('Id\tName\n')
    for x_id, x in dgidb_.drug_names.items():
        f.write(f'{x_id}\t{x}\n')

print('Generating diseases')
with gzip.open('../data/processed/diseases.tsv.gz', 'wt') as f:
    f.write('Id\tName\tClass\n')
    for x_id, x in disgenet_.dis.items():
        f.write(f'{x_id}\t{x.name}\t{";".join(x.classes)}\n')

print('Generating interactions, evidences')
with gzip.open('../data/processed/interactions.tsv.gz', 'wt') as fi:
    with gzip.open('../data/processed/evidences.tsv.gz', 'wt') as fe:
        fi.write('Id\tDrugId\tDiseaseId\tScore\tGene\tType\n')
        fe.write('InteractionId\tPmid\tScore\n')

        ii = 0

        for g, dis_ls in disgenet_.interactions.items():
            drug_ls = dgidb_.interactions[g]

            for disi in dis_ls:
                for drugi in drug_ls:
                    disgenet_score = mean([evidence.score for evidence in disi.evidences])
                    score = drugi.score * disgenet_score
                    type = int(drugi.ty == disi.ty)

                    # Generate evidences

                    for pmid in drugi.pmids:
                        fe.write(f'{ii}\t{pmid}\t{drugi.score}\n')

                    for evidence in disi.evidences:
                        fe.write(f'{ii}\t{evidence.pmid}\t{evidence.score}\n')

                    fi.write(f'{ii}\t{drugi.drug}\t{disi.dis}\t{score}\t{type}\n')

                    ii += 1

print(f'Completed in {timeit.default_timer() - start:.1f} s')
