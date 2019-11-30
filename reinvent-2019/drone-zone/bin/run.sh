python3 ground-control.py -e $(cat /greengrass/config/config.json | jq -r '.coreThing.iotHost') \
-c /greengrass/certs/core.cert.pem \
-k /greengrass/certs/core.private.key \
-r /greengrass/certs/root.ca.pem \
-id $(cat /greengrass/config/config.json | jq -r '.coreThing.thingName') \
-t $(cat /greengrass/config/config.json | jq -r '.coreThing.thingName') \
-m both
