rm dataplattform_ingest.zip
zip -9 dataplattform_ingest.zip lambda_function.py ingest.py filters.py
aws lambda update-function-code --function-name dataplattform_ingest --zip-file fileb://dataplattform_ingest.zip
