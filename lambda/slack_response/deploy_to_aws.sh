#!/bin/sh
# Small script that installs virtual environment if you don't have one already and installs all the
# dependencies needed and creates a zip of everything that lambda needs.

if ! [ -d "venv" ]; then
    virtualenv -p python3 venv
fi
rm slack_response.zip
. venv/bin/activate && pip install -r requirements.txt

cd venv/lib/python3.6/site-packages
zip -r9 ${OLDPWD}/slack_response.zip .
cd $OLDPWD
zip -g slack_response.zip slack_response.py
zip -g slack_response.zip token.pickle
echo "Uploading"
aws lambda update-function-code --function-name dataplattform_slack_response --zip-file fileb://slack_response.zip
