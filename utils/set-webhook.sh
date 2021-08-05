#!/bin/bash

CURRENT_DIR=$(dirname $(readlink -f "$0"))
export $(xargs < $CURRENT_DIR/../.env) && curl -X POST --data-raw \
    "{\"url\": \"${NGROK_URL}/api/echo_function\"}" -H "Content-Type: application/json" \
    "https://api.telegram.org/bot${BOT_TOKEN}/setWebhook"