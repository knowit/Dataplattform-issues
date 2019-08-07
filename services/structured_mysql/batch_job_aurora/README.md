# batch_job_aurora
Denne lambdaen er laget for å kunne hente alle datapunktene som er lagret som rå data i DynamoDB
via ```fetch_docs```-APIet og så filtrere ut relevante attributter og lagre det i et fint format
i en SQL-database (Aurora).
Lambdaens standardoppførsel er å hente dataen fra de siste 1t10m, og kjøres hver time i aws (se
`../serverless.yml`).
Det skader ikke å kjøre lambdaen for ofte, da duplikatdata ignoreres, men da burde den
konfigureres til å hente data fra DynamoDB for kortere intervaller enn 1t10m for å senke
disk/nettverkstrafikk.

## Legge til ny datatype
Vi har en
[Wiki-side](https://github.com/knowit/Dataplattform/wiki/Sende-inn-data-til-dataplattformen)
om å legge til en ny datatype.

Se ```data_types/UBWType``` for et eksempel med enkel uthenting fra et datapunkt.
Se ```data_types/GithubType``` og ```data_types/SlackType``` for eksempler med litt mer avansert
oppsett.

For å teste lambdaen kan du lage et ```test event``` i AWS-panelet og i test-dataen som blir sendt
har du noe slikt:
```json
{
  "types": [
    "GithubType",
    "SlackType",
    "EventRatingType"
  ],
  "timestamp_from": 1564660617,
  "timestamp_to": 1565179017
}
```
