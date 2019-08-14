# slack_ingest

## Slack app
En Slack app må lages og legges til i workspacet. Gå inn på appens innstillinger og skru på
event subscriptions.
Legg inn URLen til lambdaen som ```Request URL```.
Subscribe til eventene `message.channels` og `reaction_added`, som gir tilgang til meldinger sendt
i offentlige kanaler og reactions på dem.

## Lambda
Denne lambdaen blir brukt som et endepunkt for Slack. Lambdaen sjekker at requesten
faktisk er sendt fra Slack ved å regne ut en signatur.
Dette må vi gjøre fordi Slack web hooks ikke kan sende en custom header med en api key slik som
andre datakilder.
Man trenger også en forhåndsdelt ```Signing Secret``` som hentes fra
```Basic settings/App credentials``` til appen. Secreten må legges inn i SSM:
```
aws ssm put-parameter --type String --name dataplattform_slack_shared_secret --tags Key=Project,Value=Dataplattform --value <VERDI>
```
