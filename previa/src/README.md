# Requisitos

* Python 3
* pandas
* sklearn

# Execução

## Para gerar `external/disgenet`

Fazer download do SQLite do DisGeNET e salvar em `data/raw/disgenet.db`.

Executar `disgenet2tsv` na pasta `src`.

## Para gerar dados processados

Necessita que `external/disgenet` exista.

Executar `process` na pasta `src`.
