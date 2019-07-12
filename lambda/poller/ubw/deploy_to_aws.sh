#!/bin/sh
# Small script that installs virtual environment if you don't have one already and installs all the
# dependencies needed and creates a zip of everything that lambda needs.

if ! [ -d "venv" ]; then
    virtualenv -p python3 venv
fi
rm ubw_poller.zip
. venv/bin/activate && pip install -r requirements.txt

cd venv/lib/python3.6/site-packages
zip -r9 ${OLDPWD}/ubw_poller.zip .
cd $OLDPWD
zip -g ubw_poller.zip ubw_poller.py
echo "Uploading"
aws lambda update-function-code --function-name dataplattform_ubw_poller --zip-file fileb://ubw_poller.zip
