rm dataplattform_fetch.zip
zip -9 dataplattform_fetch.zip lambda_function.py get_docs.py
aws lambda update-function-code --function-name dataplattform_fetch --zip-file fileb://dataplattform_fetch.zip