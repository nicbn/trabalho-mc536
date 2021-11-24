# Requisitos

* Python 3
* pandas
* sklearn

# Execução

## Para gerar `external/disgenet`

Fazer download do SQLite do DisGeNET ([aqui](https://www.disgenet.org/downloads)) e salvar em `data/raw/disgenet.db`.

Executar `disgenet2tsv` na pasta `src`.

## Para gerar dados processados

### TSV

Necessita que `external/disgenet` exista.

Executar `generate_tsv` na pasta `src`.

### SQLite

Necessita que os dados TSV existam.

Executar `tsv2sqlite` na pasta `src`.

O arquivo fica disponível em `data/processed/sqlite`.

### Neo4j

Necessita que os dados TSV existam.

Executar `tsv2neo4j` na pasta `src`.

Para importar execute `import_neo4j`.
