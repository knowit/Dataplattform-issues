# get_docs

Denne lambdaen henter ut data for en data type og innenfor et intervall og returnerer en link som 
er presigned med AWS slik at den bare funker i 5 minutter.
Deretter må du kjøre en ny get request på den presigned URLen. 

Måten dette funker på er at når du requester f.eks ```get_docs/GithubType``` så
henter denne lambdaen all dataen som er av type GithubType og så laster opp til en s3 bucket.
Dette må blir gjort fordi originalt så har lambda en 6MB limit på payloads. Og så signerer denne
lambdaen en url som får lov å laste ned akuratt denne dataen fra s3 bucket i 5 minutter. Og så blir
denne linken returnert. Dataen i s3 blir automatisk slettet etter 1 døgn fordi denne dataen er en
kopi som bare blir brukt en gang. 
