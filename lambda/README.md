# Lambda
Denne mappen inneholder lambda-funksjoner for kjøring på AWS lambda. 
## Delte biblioteker - layers
Det første du må gjøre er å lage et layer som du kan kalle for ```timestamp_random```. Kjør ```layers/create_timestamp_random_module.sh``` for å generere en zip-fil, og last den opp som et layer for ```python3.7```-runtimen.


## Ingest API lambda
Koden for ingest-lambdaen ligger i ```ingest/```. Denne trenger ```timestamp_random```-layeret. AWS-rollen denne kjører i trenger også tilgang til ```PutItem``` for DynamoDB-tabellen som blir brukt.


## API lambdas for fetching
### get_docs API lambda
Denne lambdaen tar inn en type og gir ut alle dokumentene som har denne typen og innenfor et intervall, hvis det er valgt.
Koden ligger i ```fetchers/get_docs```. Denne trenger ```timestamp_random```-layeret. 


## API gateway
ingest- og fetching-lambdaene trenger en API gateway for å være tilgjengelig over HTTPS. Her kan man egentlig strukturere resourcene og methodsene litt som man vil. ingest og fetching trenger ikke å bruke samme API gateway, men de kan gjør det. De trenger begge et path-parameter ```type```. De lages da ved å lage en resource ```[...]/{type}```, med en method (POST/GET) som linker til lambdaene for ingest/fetch.

Hvis du lager et oppsett med proxy paths må du huske å sjekke av for aws proxy integration når du lager en method for å linke til en lambda.

HUSK: Helt til slutt må du trykke på deploy API.
