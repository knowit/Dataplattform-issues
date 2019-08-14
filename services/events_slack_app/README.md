# Slack events app
Denne servicen inneholder koden for å kjøre en Slack-app for å generere arrangementkoder for
```event_knapp```.

For å lese om hvordan man tar i bruk denne appen, se
[https://github.com/knowit/Dataplattform/wiki/Lage-et-arrangement-koblet-opp-mot-vurderingssysteme](wiki).

## Oppsett

1. Gå på https://api.slack.com/apps og trykk på `Create New App`
2. Kall den f.eks ArrangementBot og velg hvilket workspace du skal lage appen i.
3.
    Under `Basic Information` er det en `Signing Secret`. Denne må vi lagre i AWS Systems Manager Parameter Store:

    ```bash
    aws ssm put-parameter --type String --name dataplattform_slack_event_app_secret  --tags Key=Project,Value=Dataplattform --value <verdi>
    ```
4.
    Legg til en bot under `Basic Information` og `Add features and functionality` og `Bots`. Kall den `ArrangementBot` og sjekk av for always online, og så lagre.
5.
    Gå til `Basic Information` og `Add features and functionality` og `Permissions` og legg til et nytt permission scope `chat:write:bot` som gjør at du kan sende meldinger som botten du nettopp lagde.

6.
    Lagre Bot brukern sin oauth token i AWS SSM. Du finner tokenen under `OAuth  & Permissions` og `Bot User OAuth Access Token`.

    ```bash
    aws ssm put-parameter --type String --name dataplattform_slack_event_oauth --tags Key=Project,Value=Dataplattform --value xoxb-...
    ```
7.
    For å deploye trenger du en ```creds.json```. Vi har et eget ```Dataplattform```-prosjekt i [Google API console](https://console.developers.google.com/apis/credentials). Lag en service account på prosjektet og velg json når du lagrer credentialsene. Lagre som ```slack_response/creds.json```.
8.
    Deretter må du hente en google calender ID og så lagre den i SSM:
    ```bash
    aws ssm put-parameter --type String --name dataplattform_fagkalender_id  --tags Key=Project,Value=Dataplattform --value ....@group.calendar.google.com
    ```
9.
    Deploy med ```serverless deploy```. Ta vare på endpoint URLen som printes på skjermen når den er ferdig.

10. 
    Nå kan vi lage litt funksjonalitet på Slack appen. Dette gjøres under `Basic Information` og `Add features and functionality`. Skru på `Interactive Components` og lim inn URLen du fikk fra forrige steg under `Request URL`.

11.
    For å lage en slack command så går vi i `Basic Information` og `Add features and functionality` og `Slack Commands` og `Create New Command`. Command er `/arrangement` og Request URL er lik som den i forrige steg. Trykk `Save`.

12.
    Installer appen i ditt workspace.


## slack_command virkemåte
Slik det funker er at når en bruker skriver ```/arrangement``` eller svarer på en interaktiv
melding sendes det en request til ```slack_command``` som invoker ```slack_response``` og
returnerer med en tekst som ber brukeren om å vente eller bekrefter innsendingen.


## slack_response virkemåte
Denne funker ved at den først henter ut de 10 neste fagarrangementene fra knowit sin google
kalender, deretter ser den på requesten som kom inn for å finne ut hva slags event som gjorde at
lambdaen ble kjørt og sender et passende svar. Om noen trykket på ```Få kode```-knappen så
genereres en tilfeldig kode som ikke er i bruk allerede. Når koden blir gitt ut blir det også
schedulet en melding fra slack som sier at du må registrere
arrangementet. Når arrangementet er ferdig får personen som genererte koden en melding fra
slack-botten om å fylle inn hvor mange som kom der og hvilken faggruppe som stod for dette
arrangementet.
