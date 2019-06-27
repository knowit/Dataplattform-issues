if ! [ -d "venv" ]; then 
    virtualenv -p python3 venv
fi
source venv/bin/activate
pip install -r requirements.txt
pip install layers/python/
pip install batch_job_aurora/
pip install ingest/
pip install fetchers/get_docs/
