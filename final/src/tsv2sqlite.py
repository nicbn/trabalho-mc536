import gzip
import os
import csv
import sqlite3

def compress(path):
    with gzip.open(f'{path}.gz', 'wb') as fout, open(path, 'rb') as fin:
        fout.writelines(fin)

try:
    os.remove('../data/processed/sqlite/sqlite.db')
except FileNotFoundError:
    pass
try:
    os.mkdir('../data/processed/sqlite')
except FileExistsError:
    pass

with sqlite3.connect('../data/processed/sqlite/sqlite.db') as conn:
    conn.execute('''
CREATE TABLE Disease(
    Id TEXT NOT NULL PRIMARY KEY,
    Name TEXT NOT NULL,
    Class TEXT
)
    ''')

    conn.execute('''
CREATE TABLE Drug(
    Id TEXT NOT NULL PRIMARY KEY,
    Name TEXT NOT NULL
)
    ''')

    conn.execute('''
CREATE TABLE Interaction(
    Id INTEGER NOT NULL PRIMARY KEY,
    DrugId TEXT NOT NULL REFERENCES Drug(Id),
    DiseaseId TEXT NOT NULL REFERENCES Disease(Id),
    Score REAL NOT NULL,
    Gene TEXT NOT NULL,
    Type INTEGER NOT NULL
)
    ''')

    conn.execute('''
CREATE TABLE Evidence(
    InteractionId INTEGER NOT NULL REFERENCES Interaction(Id),
    Pmid TEXT NOT NULL,
    Score REAL NOT NULL
)
    ''')

    with gzip.open('../data/processed/tsv/drugs.tsv.gz', 'rt') as f:
        dict = csv.DictReader(f, delimiter='\t')
        conn.executemany(
            'INSERT INTO Drug (Id, Name) VALUES (?, ?)',
            [[row['Id'], row['Name']] for row in dict]
        )
    with gzip.open('../data/processed/tsv/diseases.tsv.gz', 'rt') as f:
        dict = csv.DictReader(f, delimiter='\t')
        conn.executemany(
            'INSERT INTO Disease (Id, Name, Class) VALUES (?, ?, ?)',
            [[row['Id'], row['Name'], row['Class']] for row in dict]
        )
    with gzip.open('../data/processed/tsv/interactions.tsv.gz', 'rt') as f:
        dict = csv.DictReader(f, delimiter='\t')
        conn.executemany(
            'INSERT INTO Interaction (Id, DrugId, DiseaseId, Score, Gene, Type) VALUES (?, ?, ?, ?, ?, ?)',
            [[row['Id'], row['DrugId'], row['DiseaseId'], row['Score'], row['Gene'], row['Type']] for row in dict]
        )
    with gzip.open('../data/processed/tsv/evidences.tsv.gz', 'rt') as f:
        dict = csv.DictReader(f, delimiter='\t')
        conn.executemany(
            'INSERT INTO Evidence (InteractionId, Pmid, Score) VALUES (?, ?, ?)',
            [[row['InteractionId'], row['Pmid'], row['Score']] for row in dict]
        )

compress('../data/processed/sqlite/sqlite.db')
