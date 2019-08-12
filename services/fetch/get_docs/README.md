# get_docs

[Swagger](https://knowit.github.io/Dataplattform/)

Denne lambdaen henter ut data for en datatype innenfor et intervall og returnerer en 
presigned URL til et dokument i en S3 bucket som bare funker i 5 minutter.
Deretter må du kjøre en ny get request på den presigned URLen. 

Måten dette funker på er at når du requester f.eks ```get_docs/GithubType``` så
henter denne lambdaen all dataen som er av type GithubType og så laster opp til en S3 bucket.
Dette må blir gjort fordi lambda har en 6MB limit på payloads. 
Denne lambdaen signerer en url som får lov å laste ned akuratt denne dataen fra s3 bucketen i
5 minutter. Dataen i s3 blir automatisk slettet etter 1 døgn fordi denne dataen er en
kopi som bare blir brukt en gang. 
