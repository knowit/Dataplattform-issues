# slack_ingest

## Slack app
En Slack app må lages og legges til i workspacet. Gå inn på appens innstillinger og skru på
event subscriptions.
Legg inn URLen til lambdaen som ```Request URL```.
Subscribe til eventet ```message.channels```, som gir tilgang til meldinger sendt
i offentlige kanaler.

## Lambda
Denne lambdaen blir brukt som et endepunkt for Slack. Lambdaen sjekker at requesten
faktisk er sendt fra Slack ved å regne ut en signatur.
Dette må vi gjøre fordi Slack web hooks ikke kan sende en custom header med en api key slik som
andre datakilder.

Lambdaen skal ikke legges bak en api key i AWS API gatewayen, men må ha en
gyldig URL og api key til ingest-APIet i environment variables ```DATAPLATTFORM_INGEST_URL```
og ```DATAPLATTFORM_INGEST_APIKEY```.
Man trenger også en forhåndsdelt ```Signing Secret``` som hentes fra
```Basic settings/App credentials```
til appen. Secreten må legges som en environment variable ```DATAPLATTFORM_SLACK_SECRET```.
