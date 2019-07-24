# Poller

Her ligger kode for lambdaer som skal kjøres periodisk for å polle fra en datakilde og POSTe
dataen til det vanlige ingest-endepunktet. Dette må gjøres for datakilder som ikke selv sender
et event til dataplattformen når noe skjer.

Hvis du skal lage en ny poller som kjøres daglig kan du legge den inn i `daily_poller`, som
allerede har kode for UBW og knowitlabs. Hvis dette ikke passer kan du lage en ny lambda med
et annet rate-uttryk eller lignende.
