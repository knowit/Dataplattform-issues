# Dataplattform

## Mappestruktur
  * ```lambda/```
      * Denne inneholder alle lambda-funksjonene som ble skrevet for AWS lambda.
  * ```test_data_source/```
      * Blir brukt for manuell testing.

### Disse datakildene inneholder persondata:
  * github
      * Github har sensitiv informasjon, her blir det lagret både navn, e-post addresse og commit-melding. 
  * slack
      * Slack kan inneholde alt, avhengig av hvordan integrasjons-appen er konfigurert.
