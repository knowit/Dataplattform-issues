# Machine learning
Her ligger noen filer som kan bli kjørt for å lære hva som gir utslag på en DayRating. 
DayRating er knappen de ansatte kan trykke på i kontoret på om de synes det har vært en bra dag
 eller en dårlig dag, altså 👍 eller 👎.

Så her lager vi et tall fra 0 til 1, hvor 1 er at alle trykket på 👍, mens 0 er at alle trykket på 👎.
Dette er vår label og er det vi da prøver å predikere. Så spørsmålet er hvordan blir det en dag
de ansatte liker? 

Som input har vi en del data som vi har samlet i dataplattformen, noen eksempler her:
 * Hvor mange slack meldinger det var tidlig om morningen, midt på dagen og sent på kvelden.
 * Hvilken hverdag det er.
 * Hvor mange commits til knowit sitt offentlige repo.
 * Av alle slack reactionsene hvor mange blir sett på som positive, negative og nøytrale?
    (Emoji sentiment liste er hentet fra 
    https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0144296)
      

## Oppsett av jupyter i Amazon Sagemaker:
1. `Create notebook instance`
2. Lag en ny rolle som har
    * AmazonSageMakerFullAccess
    * AmazonSSMReadOnlyAccess
    * AWSLambdaVPCAccessExecutionRole
3. VPC
    * OsloCloud
    * subnet: ON-LAN1
    * security groups: ON-LAN
    * Under `Direct internet access` sjekk av `Disable — Access the internet through a VPC`
4. Git repository: `https://github.com/knowit/Dataplattform.git`

Etter den er laget og notebooken er skrudd på så er det bare å gå i 
`Dataplattform/machine_learning/day_rating_predicter.ipynb` for å kjøre den.