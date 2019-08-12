# fetch

Denne servicen inneholder funksjoner for å hente ut data av DynamoDB. Til nå finnes bare `get_docs`
som er lagd for å hente ut data basert på type og tid. `get_docs` er bare beskyttet av api-nøkler
på API gateway-nivå, så hvis man trenger mer finjustert tilgang til forskjellige datatyper
kan det gi mening å lage en funksjon i denne servicen.
