# Poller
Disse modulene legger inn data på en litt annerledes måte enn ingest-modulene. Disse må bli 
regelmessig kjørt for å så hente ut data fra datakilden og så huske hvor mye av dataen som har
allerede blitt lastet opp i dataplattformen. Dette må bli gjort fordi det er en del datakilder som
ikke har ting som webhooks og må dermed gjøre det på denne måten.
Til nå så er det bare UBW data som må bli pollet, men om det kommer flere datakilder så burde alle
samles til en stor lambda for å gjøre det litt mer effektivt.