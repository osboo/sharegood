#!/bin/bash

CURRENT_DIR=$(dirname $(readlink -f "$0"))
# export $(xargs < $CURRENT_DIR/../.env) && \
#     BOT_TOKEN=$(bash $CURRENT_DIR/get_bot_token.sh) && \
#     curl -X POST --data-raw \
#     "{\"url\": \"${NGROK_URL}/api/lebowski\"}" -H "Content-Type: application/json" \
#     "https://api.telegram.org/bot${BOT_TOKEN}/setWebhook"

source $CURRENT_DIR/../.env && export $(cut -d= -f1 $CURRENT_DIR/../.env) && \
    curl -X POST --data-raw \
    "{\"url\": \"${NGROK_URL}/api/lebowski\"}" -H "Content-Type: application/json" \
    "https://api.telegram.org/bot${SharegoodToken}/setWebhook"
    