import os
import string
import random

keys = [
    "dataplattform_STAGE_slack_ingest_apikey",
    "dataplattform_STAGE_github_ingest_apikey",
    "dataplattform_STAGE_slack_event_app_ingest_apikey",
    "dataplattform_STAGE_polling_ingest_apikey",
    "dataplattform_STAGE_travis_ingest_apikey",

    "dataplattform_STAGE_fetch_apikey",
    "dataplattform_STAGE_batch_job_apikey",
]

default_stages = ["prod", "test", "dev"]


def generate_apikey(keylength=40):
    alphabet = string.ascii_letters + string.digits
    return ''.join(random.choice(alphabet) for _ in range(keylength))


stage = input("Velg et stage å lage api-nøkler for: ")
if stage not in default_stages:
    confirmation = input(
        f"{stage} er ikke et standard stage (prod/test/dev), er du sikker på at du "
        f"vil fortsette? [y/N]: ")
    if not confirmation.lower() == "y":
        exit()

generated = []
fails = []
for key in keys:
    name = key.replace("STAGE", stage)
    value = generate_apikey()
    command = f"aws ssm put-parameter --type String --name {name} --value {value} " \
        f"--tags Key=Project,Value=Dataplattform"
    exit_code = os.system(command)
    if exit_code == 0:
        generated.append((name, value))
    else:
        fails.append(name)

if len(generated) > 0:
    print("---- Generated keys ----")
    for (name, val) in generated:
        print(f"{name}: {val}")

if len(fails) > 0:
    print("---- FAILED creating keys ----")
    for name in fails:
        print(name)

print()
if len(fails) == 0:
    print(f"\nAll {len(keys)} keys successfully created. Deploy services use the new keys.")
else:
    print(f"Some keys could not be created.")
