#!/bin/sh
curl -X PUT -H "Content-Type: application/json" -d @userHit_index.json https://xxxxxx.us-east-1.es.amazonaws.com/userhits
curl -X PUT -H "Content-Type: application/json" -d @referencehit_index.json https://xxxxxxxxxxxxxx.us-east-1.es.amazonaws.com/referencehits

