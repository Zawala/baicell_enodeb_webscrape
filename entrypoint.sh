#!/bin/bash

# Set strict mode
set -euo pipefail

# Function to log messages
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Clean up APT cache
log "Cleaning up APT cache..."
rm -rf /var/lib/apt/lists/*
mkdir -p /var/lib/apt/lists

# Update package lists and upgrade existing packages
log "Updating package lists..."
apt-get update || exit 1
apt-get upgrade -y || exit 1

# Install essential packages
log "Installing essential packages..."
apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common \
    systemd \
    systemd-sysv-utils \
    procps \
    net-tools \
    iputils-ping \
    htop \
    vim \
    nano \
    wget \
    unzip \
    zip \
    git \
    && rm -rf /var/lib/apt/lists/*

# Configure systemd
log "Configuring systemd..."
mkdir -p /etc/systemd/system
mkdir -p /var/log/systemd

# Create a systemd service file
cat << EOF > /etc/systemd/system/wall-e.service

[Unit]
Description=Scrape Data from from baicell enodebs

[Service]
Type=simple
ExecStart=${HOME}/wall-e.bin
Restart=always
RestartSec=1

[Install]
WantedBy=multi-user.target
EOF

# Enable and start the service
log "Enabling and starting the service..."
systemctl daemon-reload || exit 1
systemctl enable wall-e.service || exit 1
systemctl start wall-e.service || exit 1

# Set up logging
log "Setting up logging..."
mkdir -p /var/log/systemd
touch /var/log/systemd/wall-e.log

# Set up environment variables
log "Setting up environment variables..."
cat << EOF > /etc/environment
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games
LANG=en_US.UTF-8
EOF

# Clean up
log "Cleaning up..."
apt-get autoremove -y || exit 1
apt-get clean || exit 1

# Exit successfully
exit 0