## Pergunta 1
query1 = "SELECT Dr.Name, Di.Name, I.Type, I.Score FROM Interaction as I, Drug as Dr, Disease  as Di WHERE Dr.Id = I.DrugId AND Di.Id = I.DiseaseId ORDER BY I.Score DESC LIMIT 10;"

## Pergunta 2
query2 = "SELECT D.Id, D.Name  FROM INTERACTION as I, DRUG as D, Disease  as Di  WHERE Di.id ='C0023449'  LIMIT 10;"

## Pergunta 3
query3 = ""