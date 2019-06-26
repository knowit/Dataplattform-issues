# github_authorizer
Denne lambdaen blir brukt som en authorizer for Github-endepunktet i ingest API gatewayen.
Dette er fordi Github web hooks ikke kan sende en custom header med en api key slik som
andre datakilder. Derfor trenger man en egen API gateway resource som ikke er beskyttet med
en api key, men som bruker denne lambdaen som authorizer.

Authorizeren virker ved å beregne en sjekksum av innholdet i ingest-API-kallet og en
forhåndsdelt ```Secret``` som er lagt inn på github.com sammen med URLen til endepunktet.
Dette secreten må også legges som en environment variable
```DATAPLATTFORM_GITHUB_SECRET```.