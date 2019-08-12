# github_ingest
Denne lambdaen blir brukt som et endepunkt for Github. Lambdaen sjekker at requesten
faktisk er sendt fra Github ved å regne ut en signatur.
Dette må vi gjøre fordi Github web hooks ikke kan sende en custom header med en api key slik som
andre datakilder.

Man trenger en forhåndsdelt ```Secret``` som er lagt inn på github.com sammen med URLen
som peker på denne lambdaen. Denne må legges inn i aws ssm som
```dataplattform_github_shared_secret```.
