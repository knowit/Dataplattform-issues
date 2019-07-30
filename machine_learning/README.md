# Machine learning


## Oppsett av jupyter i Amazon Sagemaker:
1. `Create notebook instance`
2. Lag en ny rolle som har
    * AmazonSageMakerFullAccess
    * AmazonSSMReadOnlyAccess
    * AWSLambdaVPCAccessExecutionRole
3. VPS
    * OsloCloud
    * subnet: ON-LAN1
    * security groups: ON-LAN, ON-PUBLIC, default
    * Under `Direct internet access` sjekk av `Disable — Access the internet through a VPC`
4. Git repository: `https://github.com/knowit/Dataplattform.git`

Etter den er laget og notebooken er skrudd på så er det bare å gå i 
`Dataplattform/machine_learning/day_rating_predicter.ipynb` for å kjøre den.