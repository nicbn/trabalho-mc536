import os

os.system(
    'neo4j-admin import --database neo4j --nodes '
    + os.path.abspath('../data/processed/neo4j/nodes.csv')
    + ' --relationships '
    + os.path.abspath('../data/processed/neo4j/edges.csv'))
