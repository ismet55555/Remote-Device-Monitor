#################################################################################
#
# This DOCKERFILE can be used with balena to deploy to a device.
# It's designed for a raspberry pi 3, however can be adjusted for
# any other device.
#
# 1. Create a balena application and flash image to device:
#      - https://www.balena.io/docs/learn/getting-started/raspberrypi3/python/
# 2. Install balena CLI:
#      - https://github.com/balena-io/balena-cli/blob/master/INSTALL.md
# 3. Use balena CLI to push current repo directory onto application:
#      - balena push <Name-of-your-belena-applicatio>
#
#################################################################################

# Raspberry PI 3 Debian Base Image
#   - https://hub.docker.com/r/balenalib/raspberry-pi-debian-python
#FROM balenalib/raspberry-pi-debian-python
FROM ubuntu:bionic
#FROM python:3.7-alpine


# Install base OS tools and dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    netcat \
    curl \
    git \
    net-tools \
    openssh-server \
    vim \
    wget \
    python3-venv \
    python3-pip \
    libpython-dev

# Clearing out local repo of retrieved OS tools and dependencies
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Installing/Upgrading pip
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && \
    python3 get-pip.py

RUN pip install wheel

# Create the application directory
RUN mkdir -p /device-monitor

# Copy all files in current directory into application directory (container)
COPY . /device-monitor

# Define working directory
WORKDIR /device-monitor

EXPOSE 7777

# Give execture permission to start-up script
RUN ["chmod", "+x", "/device-monitor/start"]

# Run the start-up script
CMD [ "bash", "/device-monitor/start" ]
