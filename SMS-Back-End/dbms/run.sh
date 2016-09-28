#!/usr/bin/env bash

echo -e "\n\033[32m ### Launching DBmS Stand Alone Mode ###\033[0m\n"

../../google_appengine/dev_appserver.py --port=8001 --admin_port=8082 dbms.yaml

