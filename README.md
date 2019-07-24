# Dataplattform

## Hente ut data fra dataplattformen
https://knowit.github.io/Dataplattform/

## Sende inn data
https://github.com/knowit/Dataplattform/wiki/Sende-inn-data-til-dataplattformen

## Mappestruktur
  * ```services/```
      * Denne inneholder alle `serverless` services som deployes til AWS.
  * ```event_knapp/```
      * Kode for fysisk feedback-knapp

## Oppsett
Se ```services/README.md``` for deploying til AWS og oppsett av QuickSight.


## Disse datakildene kan inneholde persondata:
  * github
      * Github har potensielt sensitiv informasjon, her blir det lagret både navn, e-post addresse
      og commit-melding, men vi filtrerer ut alt som ikke kommer fra offentlige repoer. Se
      ```services/ingest/ingest/filters.py```.
  * slack
      * Slack webhooks kan inneholde alt, avhengig av hvordan integrasjons-appen er konfigurert.
      Vi tar bare vare på tidspunkt og kanal for meldinger skrevet i offentlige kanaler.
      Se ```lambda/ingest/filters.py```.
      For reactions til meldinger lagrer vi kanal, tidspunkt og hvilken emoticon som ble brukt.
  * knowitlabs (blogg)
      * Vi scraper knowitlabs.no og lagrer litt offentlig informasjon om hvert blogginnlegg, som
        tittel, undertittel, forfatter og tidspunkt.
