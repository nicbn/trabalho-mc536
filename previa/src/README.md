# Requisitos

* Python 3
* pandas
* sklearn

# Execução

## Para gerar `interim/disgenet`

Fazer download do SQLite do DisGeNET e salvar em `data/external/disgenet.db`.

Executar `disgenet2tsv` na pasta `src`.

## Para gerar dados processados

Necessita que `interim/disgenet` exista.

Executar `build` na pasta `src`.
