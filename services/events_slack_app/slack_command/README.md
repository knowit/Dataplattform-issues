# slack_command
For å sette opp en knapp for et event skriv ```/arrangement```. Der kan du trykke på ```få kode```
og så kan du stille inn din boks på denne koden.

For å lage en slack app må du først lage to AWS lambdaer, de er kalt ```slack_command``` og 
```slack_response```.
Så kan du lage en ny slack app og gå til ```Slash Commands``` og putt inn 
```slack_command```-lambda API gateway sitt endepunkt på ```Request Url```. Etter det gå til 
```Interactive Components``` og legg inn ```slack_command```-lambda API gateway sitt endepunkt 
på ```Request Url```.

Slik det funker er at når en bruker skriver ```/arrangement``` så kommer det en request til 
```slack_command``` som invoker ```slack_response``` og returnerer med en tekst som ber brukeren
om å vente til ```slack_response``` har fullført. Når ```slack_response``` lambdaen har 
fullført så blir det sendt enda et svar til brukeren i slack. Dette svaret er interaktivt og 
man kan trykke på ```få kode``` for å få en tildelt kode. Denne koden blir generet i 
```../slack_response/slack_response.py``` og blir da lagret i DynamoDB. 
 
```slack_command``` trenger tilgang til å invoke ```slack_response```-lambdaen. 
