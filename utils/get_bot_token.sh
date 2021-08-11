#!/bin/bash

CURRENT_DIR=$(dirname $(readlink -f "$0"))

export $(xargs < $CURRENT_DIR/../.env)

AZURE_AD_TOKEN=$(curl -s \
    --location --request POST "https://login.microsoftonline.com/${TENANT_ID}/oauth2/v2.0/token" \
    --form "grant_type=client_credentials" \
    --form "client_id=${APP_ID}" \
    --form "client_secret=${CLIENT_KEY}" \
    --form "scope=https://vault.azure.net/.default" | jq -r .access_token)

curl -s --location --request GET "https://${AKV_URL}/secrets/SharegoodToken?api-version=2016-10-01" \
--header "Authorization: Bearer ${AZURE_AD_TOKEN}" | jq -r .value