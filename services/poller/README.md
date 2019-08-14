# Poller

Her ligger kode for lambdaer som skal kjøres periodisk for å polle fra en datakilde og POSTe
dataen til det vanlige ingest-endepunktet. Dette må gjøres for datakilder som ikke selv sender
et event til dataplattformen når noe skjer.

Hvis du skal lage en ny poller som kjøres daglig kan du legge den inn i `daily_poller`, som
allerede har kode for UBW og knowitlabs. Hvis dette ikke passer kan du lage en ny lambda med
et annet rate-uttryk eller lignende.

## Oppsett

Det er 4 environment variables som trenger data fra SSM.

```
UBW_CLIENT: dataplattform_ubw_client (heltall, men lagre som string)
UBW_PASSWORD: dataplattform_ubw_password
UBW_URL: dataplattform_ubw_url (på formen https://ubw.[..].com/[...]_webservices/service.svc)
UBW_USERNAME: dataplattform_ubw_username
```

```
aws ssm put-parameter --type String --name dataplattform_ubw_client  --tags Key=Project,Value=Dataplattform --value <VERDI>
aws ssm put-parameter --type String --name dataplattform_ubw_password --tags Key=Project,Value=Dataplattform --value <VERDI>
aws ssm put-parameter --type String --name dataplattform_ubw_url  --tags Key=Project,Value=Dataplattform --value <VERDI>
aws ssm put-parameter --type String --name dataplattform_ubw_username --tags Key=Project,Value=Dataplattform --value <VERDI>
```
