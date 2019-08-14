# ingest

Denne lambdaen er ansvarlig for innsetting i DynamoDB. Ved å `HTTP POST`e til denne lambdaen
med url `dataplattform_ingest/{type}` der `{type}` er datatypen til datapunktet
blir et nytt datapunkt lagt inn i DynamoDB. Lambdaen svarer med `timestamp` og generert `id`
(`timestamp_random` i DynamoDB) i JSON-format.
