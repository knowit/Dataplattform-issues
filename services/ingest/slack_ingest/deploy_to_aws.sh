rm dataplattform_slack_ingest.zip
zip -9 dataplattform_slack_ingest.zip lambda_function.py slack_ingest.py
aws lambda update-function-code --function-name dataplattform_slack_ingest --zip-file fileb://dataplattform_slack_ingest.zip
