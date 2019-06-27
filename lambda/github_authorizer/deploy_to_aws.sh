rm dataplattform_github_ingest.zip
zip -9 dataplattform_github_ingest.zip lambda_function.py github_authorizer.py
aws lambda update-function-code --function-name dataplattform_github_ingest --zip-file fileb://dataplattform_github_ingest.zip