# ingest

Denne servicen inneholder funksjonene som er endepunkt for datainnsetting.
De fleste datatyper blir sendt inn via hoved-ingestlambdaen: `ingest/ingest.py`.
Se `slack_ingest/README.md` og `github_ingest/README.md` for oppsett av de spesifikke
integrasjonene som ikke går via hoved-lambdaen og trenger litt ekstra oppsett.

API-nøklene må forhåndsgenereres og legges inn i SSM før et gitt stage kan bli deploya.
Se `services/README.md`.
