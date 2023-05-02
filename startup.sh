#!/bin/bash
set -euo pipefail

# startup script to determine which service(s) to launch at runtime

# generate ASCII banner
figlet -t "safers-dashboard-api"

# ensure "app" user in the container has same ids as local user outside the container
# (this allows them to both edit files in the mounted volume(s))
usermod --uid $RUN_AS_UID app
groupmod --gid $RUN_AS_GID app

# install dependencies
cd "${APP_HOME}/server"
setuser app pdm install

if [[ "${ENABLE_DJANGO}" -eq 1 ]]; then  
    echo -e "\n### STARTING DJANGO ###\n"
    mkdir -p /etc/service/django
    cp ../run-django.sh /etc/service/django/run
fi
