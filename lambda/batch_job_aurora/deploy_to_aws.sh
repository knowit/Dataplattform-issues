#!/bin/sh
# Small script that installs virtual environment if you don't have one already and installs all the
# dependecies needed and creates a zip of everything that lambda needs.

if ! [ -d "venv" ]; then 
    virtualenv -p python3 venv
fi
rm batch_job_aurora.zip
. venv/bin/activate
pip install -r requirements.txt

cd venv/lib/python3.6/site-packages
zip -r9 ${OLDPWD}/batch_job_aurora.zip .
cd $OLDPWD
zip -g batch_job_aurora.zip lambda_function.py
zip -g batch_job_aurora.zip batch_job_aurora.py
zip -g batch_job_aurora.zip data_types -r9
aws lambda update-function-code --function-name dataplattform_batch_job_aurora --zip-file fileb://batch_job_aurora.zip
