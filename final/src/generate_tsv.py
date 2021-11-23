import timeit
import gzip
from parse import dgidb, disgenet
from statistics import mean
import os

def compress(path):
    with gzip.open(f'{path}.gz', 'wb') as fout, open(path, 'rb') as fin:
        fout.writelines(fin)

try:
    os.mkdir('../data/processed/tsv')
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
with open('../data/processed/tsv/drugs.tsv', 'w') as f:
    f.write('Id\tName\n')
    for x_id, x in dgidb_.drug_names.items():
        f.write(f'{x_id}\t{x}\n')

print('Generating diseases')
with open('../data/processed/tsv/diseases.tsv', 'w') as f:
    f.write('Id\tName\tClass\n')
    for x_id, x in disgenet_.dis.items():
        f.write(f'{x_id}\t{x.name}\t{";".join(x.classes)}\n')

print('Generating interactions, evidences')
with open('../data/processed/tsv/interactions.tsv', 'w') as fi:
    with open('../data/processed/tsv/evidences.tsv', 'w') as fe:
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

                    fi.write(f'{ii}\t{drugi.drug}\t{disi.dis}\t{score}\t{g}\t{type}\n')

                    ii += 1

print('Compressing files')
compress('../data/processed/tsv/drugs.tsv')
compress('../data/processed/tsv/diseases.tsv')
compress('../data/processed/tsv/interactions.tsv')
compress('../data/processed/tsv/evidences.tsv')

print(f'Completed in {timeit.default_timer() - start:.1f} s')
