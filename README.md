# Dataplattform

## Mappestruktur
  * ```lambda/```
      * Denne inneholder alle lambda-funksjonene som ble skrevet for AWS lambda.
  * ```event_knapp/```
      * Kode for fysisk feedback-knapp

## Oppsett
Se ```lambda/``` for oppsett av lambda-funksjoner i AWS.
### DynamoDB i AWS
  * Lag et DynamoDB table med navn ```dataplattform```
      * Partition key ```type``` (String)
      * Sort key ```timestamp_random``` (Binary)

### Aurora i AWS
  * Lag en Aurora-instans basert på MySQL 5.7 eller nyere
  * Legg inn nøklene som miljøvariable som beskrevet i  ```lambda/batch_job_aurora```
  * Importer databasen i QuickSight

## Disse datakildene inneholder persondata:
  * github
      * Github har potensielt sensitiv informasjon, her blir det lagret både navn, e-post addresse
      og commit-melding, men vi filtrerer ut alt som ikke kommer fra offentlige repoer. Se
      ```lambda/ingest/filters.py```.
  * slack
      * Slack webhooks kan inneholde alt, avhengig av hvordan integrasjons-appen er konfigurert.
      Vi tar bare vare på tidspunkt og kanal. Se ```lambda/ingest/filters.py```.
