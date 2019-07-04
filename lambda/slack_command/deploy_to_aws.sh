rm slack_command.zip
zip -9 slack_command.zip slack_command.py
aws lambda update-function-code --function-name dataplattform_slack_command --zip-file fileb://slack_command.zip
