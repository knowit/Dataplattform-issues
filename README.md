# Dataplattform

## Mappestruktur
  * ```lambda/```
      * Denne inneholder alle lambda-funksjonene som ble skrevet for AWS lambda.

## Oppsett
Se ```lambda/``` for oppsett av lambda-funksjoner i AWS.
### DynamoDB i AWS
  * Lag et DynamoDB table med navn ```dataplattform```
      * Partition key ```type``` (String)
      * Sort key ```timestamp_random``` (Binary)

## Disse datakildene inneholder persondata:
  * github
      * Github har sensitiv informasjon, her blir det lagret både navn, e-post addresse og commit-melding. 
  * slack
      * Slack kan inneholde alt, avhengig av hvordan integrasjons-appen er konfigurert.
