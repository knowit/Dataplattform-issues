# integration_tests

Denne mappen inneholder integrasjonstester som kan kjøres fra utviklermaskiner eller fra Travis.
Testene kjøres mot `test`-staget hvis Travis kjører dem, ellers mot `dev`.
For å få tilgang til URLer, nøkler, osv som trengs for å kjøre tester lagres
CloudFormation-outputsene til en lokal fil ved hjelp av serverless-pluginen
`serverless-stack-output`. Se `services/ingest/serverless.yml` for eksempel med eksportering av
URL, API-nøkkel, og hvordan output-filen er definert under `custom`. For eksempler på hvordan
disse outputsene kan brukes se de eksisterende testene. Merk at for å få verdier i disse
filene må staget du skal kjøre tester mot ha vært deploya fra din maskin, men det trenger
ikke være nyeste deploy.
