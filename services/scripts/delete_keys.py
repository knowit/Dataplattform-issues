import os
import sys

keys = [
    "dataplattform_STAGE_slack_ingest_apikey",
    "dataplattform_STAGE_github_ingest_apikey",
    "dataplattform_STAGE_slack_event_app_ingest_apikey",
    "dataplattform_STAGE_polling_ingest_apikey",
    "dataplattform_STAGE_travis_ingest_apikey",
    "dataplattform_STAGE_jira_ingest_apikey"

    "dataplattform_STAGE_fetch_apikey",
    "dataplattform_STAGE_batch_job_apikey",
]

stage = "yeehawstage"

confirmation = input(f"Du er i ferd med å slette nøkler i SSM for {stage}-staget\n"
                     f"Er du helt sikker på hva du driver med?\n"
                     f"Fortsett? [y/N]: ")
if not confirmation.lower() == "y":
    sys.exit()

confirmation = input("Er du HELT SIKKER? [JA/NEI]: ")
if not confirmation.lower() == "ja":
    sys.exit()

for k in keys:
    key = k.replace("STAGE", stage)
    command = f"aws ssm delete-parameter --name {key}"
    exit_code = os.system(command)
    print(exit_code)
