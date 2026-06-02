#!/bin/bash
# Bundles forensic assets safely for isolated physical media deployments
echo "Exporting core docker containers into installation payload format..."
docker save redis:7-alpine > redis_airgap_image.tar
