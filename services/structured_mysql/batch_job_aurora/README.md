# batch_job_aurora
Disse filene er laget for å kunne hente alle datapunktene som er lagret som rå data i DynamoDB
via ```fetch_docs```-APIet og så filtrere ut relevante attributter og lagre det i et fint format
i en SQL-database (Aurora).
Lambdaens standardoppførsel er å hente dataen fra de siste 1t10m, og kan derfor settes opp
til å kjøre hver time i aws ved hjelp av et CloudWatch Event med rate-uttrykk ```rate(1 hour)```.
Det skader ikke å kjøre lambdaen for ofte, da duplikatdata ignoreres, men da burde den
konfigureres til å hente data fra DynamoDB for kortere intervaller enn 1t10m for å senke
disk/nettverkstrafikk.

For å støtte en ny datatype må man lage en ny python-modul som heter det samme som typen og som
har en klasse som også heter det samme som den nye typen. Denne klassen må arve fra
```AbstractType``` og må ha en ```attributes_keep``` dictionary hvor du kan beskrive hva du vil
lagre av rå-dataen, og hva den kolonnen skal hete i SQL.
Se ```data_types/EventRatingType``` for et eksempel med enkel uthenting fra et datapunkt.
Se ```data_types/GithubType``` og ```data_types/SlackType``` for eksempler med litt mer avansert
oppsett.

For å bruke lambdaen kan du lage et ```test event``` i AWS-panelet og i test-dataen som blir sendt
har du noe slikt:
```json
{
  "types": [
    "GithubType",
    "SlackType",
    "EventRatingType"
  ],
  "timestamp_from": 0,
  "timestamp_to": 100000000000
}
```

For å kjøre denne lambdaen så trenger du disse environment-variablene:
* ```DATAPLATTFORM_AURORA_FETCH_API_URL``` er URLen til der du henter rå data, så APIet til get_docs.
* ```DATAPLATTFORM_AURORA_FETCH_KEY``` er api-keyen som man trenger for å hente ut data fra APIet til get_docs.
* ```DATAPLATTFORM_AURORA_PORT``` er porten til Aurora db.
* ```DATAPLATTFORM_AURORA_HOST``` er host til Aurora databasen.
* ```DATAPLATTFORM_AURORA_DB_NAME``` er navnet til Aurora db.
* ```DATAPLATTFORM_AURORA_USER``` er brukernavnet til en user på Aurora db.
* ```DATAPLATTFORM_AURORA_PASSWORD``` er passordet til Aurora db.
* ```DATAPLATTFORM_AURORA_SLACK_TOKEN``` er oAuth tokenet til Slack.
* ```DATAPLATTFORM_EVENT_CODE_TABLE``` er table-navnet som holder styr på events m/ slack-botten
