# slack_ingest
Denne lambdaen blir brukt som et endepunkt for Slack. Lambdaen sjekker at requesten
faktisk er sendt fra Slack ved å regne ut en signatur.
Dette må vi gjøre fordi Slack web hooks ikke kan sende en custom header med en api key slik som
andre datakilder.

Denne lambdaen trenger ikke å være beskyttet av en api key i AWS API gatewayen, men må ha en
gyldig URL og api key til ingest-apiet i environment variables ```DATAPLATTFORM_INGEST_URL```
og ```DATAPLATTFORM_INGEST_APIKEY```.

TODO skriv om slack app setup

Man trenger også en forhåndsdelt ```Signing Secret``` som er hentet fra konfigurasjonssiden
til slack appen, der du også legger inn URLen til dette endepunktet. Secreten må legges som en
environment variable ```DATAPLATTFORM_SLACK_SECRET```.