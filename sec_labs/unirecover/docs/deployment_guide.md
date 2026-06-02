# Air-Gapped Deployment Guidelines
To safely configure the server on physically isolated machines:
- Mount the static `docker-compose.airgap.yml`.
- Disable all outbound networking constraints explicitly.
- Run `airgap_bundle.sh` to extract offline payloads.
