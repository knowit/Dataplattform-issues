# slack_response
Denne lambdaen skal ta imot en request fra ```slack_command```-lambdaen og lage en response og gi
den til slack sin response_url.

## Virkemåte
Denne funker ved at den først henter ut de 10 neste fagarrangementene til knowit fra knowit sin
kalender, deretter ser den på requesten som kom inn for å finne ut hva slags event som gjorde at
lambdaen ble kjørt, er det noen som skal ha en ny kode til et arrangement eller skal man bare vise
alle uten å lage nye koder? Om noen trykket på ```Få kode```-knappen så må man generere en 
tilfeldig kode og så sjekke om den blir alt brukt eller ikke. Og så er det bare å bygge
json-objektet som skal returnes og vises fram som en Slack interactive block app og sende den 
til ```response_url```-en. 

Når koden blir gitt ut blir det også schedulet en melding fra slack som sier at du må registrere
 arrangementet. Så når arrangementet er ferdig så får du en melding fra slack-botten og du kan 
 da trykke på ```Registrer arrangement``` knappen og fylle inn hvor mange som kom der og hvilken 
 faggruppe som stod for dette arrangementet.

## Setup

For å sette opp denne lambdaen må du først lage en ```creds.json```.
Vi har et eget ```Dataplattform```-prosjekt i Google API console.
Lag en service account på prosjektet og velg json når du lagrer credentialsene.
Lagre som ```creds.json``` i denne mappen før du kjører ```deploy_to_aws.sh``` for å deploye
lambdaen.

HUSK: ```slack_response``` trenger tilgang til en ny tabell i DynamoDB
```dataplattform_event_codes```.

Environment variabler du trenger for denne lambdaen er:
* SLACK_BOT_TOKEN
* DATAPLATTFORM_FAGKALENDER_ID
* DATAPLATTFORM_INGEST_APIKEY
* DATAPLATTFORM_INGEST_URL


## Setup Slack-appen
1. Gå på https://api.slack.com/apps og trykk på `Create New App`
2. Kall den f.eks ArrangementBot og velg hvilket workspace du skal lage appen i.
3. 
    Hent din `slack_command` endepunkt url. Kjør denne commanden.
    ```bash
    cd services/events_slack_app/
    sls info
    ```
    Så vil du se at det er en URL under endpoints. Ta vare på den URLen.
4.
    Tilbake til api.slack nettsiden, under `Basic Information` så er det en `Signing Secret`. Denne må vi lagre i Amazon sin SSM. Dette gjøres med denne commanden:

    ```bash
    ssn ... TODO!!
    ```
5. 
    Nå kan vi lage litt funksjonalitet på Slack appen. Dette gjøres under `Basic Information` og `Add features and functionality` og `Interactive Components`. Skru på denne og lim inn URLen du fikk fra steg 3 under `Request URL`. 
6.
    Så får å lage en slack command så går vi i `Basic Information` og `Add features and functionality` og `Slack Commands` og `Create New Command`. Command er `/arrangement` og Request URL er lik som den i forrige steg, altså den fra steg 3. Trykk `Save`.
7.
    Legg til en bot under `Basic Information` og `Add features and functionality` og `Bots`. Kall den `ArrangementBot` og always online om du vil det, og så lagre. 
8.
    Gå til `Basic Information` og `Add features and functionality` og `Permissions` og legg til et nytt permission scope `chat:write:bot` som gjør at du kan sende meldinger som botten du nettopp lagde.
9. 
    Trykk installer app i workspacet ditt.
10. 
    Lagre Bot brukern sin token i Amazon ssn. Du finner tokenen under `OAuth  & Permissions` og `Bot User OAuth Access Token` og så skriv denne commanden for å lagre den i Amazon SSN:

    ```bash
    ssn ... TODO!!
    ```
