# github_authorizer
Denne lambdaen blir brukt som et endepunkt for Github. Lambdaen sjekker at requesten
faktisk er sendt fra Github ved å regne ut en signatur.
Dette må vi gjøre fordi Github web hooks ikke kan sende en custom header med en api key slik som
andre datakilder.

Denne lambdaen trenger ikke å være beskyttet av en api key i AWS API gatewayen, men må ha en
gyldig URL og api key til ingest-apiet i environment variables ```DATAPLATTFORM_INGEST_URL```
og ```DATAPLATTFORM_INGEST_APIKEY```.



Man trenger også en forhåndsdelt ```Secret``` som er lagt inn på github.com sammen med URLen
som peker på denne lambdaen. Denne må også legges som en environment variable
```DATAPLATTFORM_GITHUB_SECRET```.