
FROM phusion/baseimage:jammy-1.0.1

# Create the app user
# Best practice is that processes within containers shouldn't run as root
# because there are often bugs found in the Linux kernel which allows container-escape exploits by "root" users inside
# the container. So we run our services as this user instead.
ENV APP_HOME=/home/app
RUN useradd -ms /bin/bash app && usermod -aG www-data app

# install dependencies...
RUN install_clean build-essential postgresql-client \
    software-properties-common figlet toilet tmux \
    python3 python3-dev python3-setuptools python3-wheel python3-pip \
    python3-gdal python3-venv nginx curl htop less git gpg
RUN pip install pdm --no-cache-dir

USER app
WORKDIR $APP_HOME

# set all services to be off (0); they can be explicitly enabled (1) at runtime
ENV ENABLE_DJANGO=0

# copy runtime scripts...
COPY --chown=root:root run-django.sh $APP_HOME/

# run startup script as per https://github.com/phusion/baseimage-docker#running_startup_scripts
USER root
RUN mkdir -p /etc/my_init.d
COPY startup.sh /etc/my_init.d/startup.sh