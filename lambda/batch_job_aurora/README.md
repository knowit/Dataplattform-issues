# batch_job_aurora
Disse filene er laget for å kunne hente alle filene som er lagret som rå data i DynamoDB og så filtrere ut relevante attributter og lagre det i et fint format i en SQL database (aurora).

For å støtte en ny datatype så må man lage en ny python modul som heter det samme som typen og som har en klasse som også heter det samme som den nye typen. Denne klassen må arve fra ```AbstractType``` og må ha en ```attributes_keep``` dictionary hvor du kan beskrive hva du vil lagre av rå-dataen, og hva den kolonnen skal hete i SQL.

For å bruke lambdaen så kan du lage en test og i test-dataen som blir sendt har du noe slikt:
```
{
  "types": [
    "GithubType",
    "EventRatingType"
  ],
  "timestamp_from": 0,
  "timestamp_to": 100000000000
}
```
