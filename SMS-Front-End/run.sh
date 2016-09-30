#!/usr/bin/env bash

echo -e "\n\033[32m ### Launching UImS Stand Alone Mode ###\033[0m\n"

../google_appengine/dev_appserver.py --port=8080 --admin_port=8082 app.yaml

