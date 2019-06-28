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

For å kjøre denne lambdaen så trenger du disse environment keysene:
```DATAPLATTFORM_AURORA_FETCH_API_URL``` er URLen til der du henter rå data, så APIet til get_docs.  
```DATAPLATTFORM_AURORA_FETCH_KEY``` er api-keyen som man trenger for å hente ut data fra APIet til get_docs.  
```DATAPLATTFORM_AURORA_HOST``` er host til Aurora databasen.  
```DATAPLATTFORM_AURORA_PORT``` er porten til Aurora db.  
```DATAPLATTFORM_AURORA_DB_NAME``` er navnet til Aurora db.  
```DATAPLATTFORM_AURORA_USER``` er brukernavnet til en user på Aurora db.  
```DATAPLATTFORM_AURORA_PASSWORD``` er passordet til Aurora db.  
```DATAPLATTFORM_AURORA_SLACK_TOKEN``` er oAuth tokenet til Slack.  