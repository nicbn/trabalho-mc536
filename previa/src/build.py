import timeit
import pandas as pd
from parse import dgidb, disgenet
from statistics import mean

start = timeit.default_timer()

print('Parsing DGIDB')
drug_gene = dgidb.parse()

print('Parsing DISGENET')
dis_gene = disgenet.parse(drug_gene.keys(), 5000)

drug_gene = {x: drug_gene[x] for x in dis_gene.keys()}

print('Generating drugs')
drugs = pd.DataFrame(columns=['DrugId', 'Name'])
for ls in drug_gene.values():
    for x in ls:
        drugs.append([x.drug, x.drug_name])

print('Generating diseases and interactions')
diseases = pd.DataFrame(columns=['DiseaseId', 'Name', 'Class'])
interactions = pd.DataFrame(columns=[
    'InteractionId',
    'DrugId',
    'DiseaseId',
    'Score',
    'Gene',
    'Type'
])
evidences = pd.DataFrame(columns=['DiseaseId', 'Name', 'Class'])
total = len(dis_gene)
for (number, (g, dislist)) in enumerate(dis_gene.items()):
    print(f'\r{((number + 1) * 100 // total):d}% ({number + 1}/{total})', end='')

    for dis in dislist:
        diseases.append([dis.dis, dis.dis_class, dis.dis_name])

        for drug in drug_gene[g]:
            # Create interaction
            interaction_id = len(interactions)
            disgenet_score = mean([x.score for x in dis.evidences])
            interactions.append([
                interaction_id,
                drug.drug,
                dis.dis,
                drug.score * disgenet_score,
                g,

            ])

            # Create evidences


print()

print(f'Completed in {timeit.default_timer() - start:.1f} s')
