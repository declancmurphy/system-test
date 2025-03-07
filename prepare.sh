#!/bin/bash

# Setup framework dependencies (docker), as a temporary manual workaround prior to use of poetry/pyenv (see "Improvements" in README)
# Will attempt to automatically install docker if the host OS is debian/ubuntu, will check if already installed before attempting
# Please see https://docs.docker.com/engine/install/ubuntu/ for reference

if ! command -v docker &> /dev/null; then

    echo "Docker is not installed. Installing now..."

    # Check for Ubuntu OS is Ubuntu as per official docs listed compatibility: https://docs.docker.com/engine/install/ubuntu/
    HOST_OS=$(lsb_release -is)
    if [[ "$HOST_OS" != "Ubuntu" ]]; then
        echo "Please install docker manually, host OS not Ubuntu."
        exit 1
    fi

    # Uninstall conflicting packages
    # WARNING: This modifies your system. The lines below will require user input to confirm this action
    read -p "Uninstalling potential docker package conflicts. Proceed? (y/n): " CONFIRM
    if [[ "$CONFIRM" =~ ^[Yy]$ ]]; then
        for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do sudo apt-get remove $pkg; done
    else
        echo "Auto install cancelled. Please install framework pre-requisites manually (see README.md)"
        exit 1
    fi

    # Install pre-requisites
    sudo apt update -y
    sudo apt install apt-transport-https ca-certificates curl software-properties-common

    # Add Docker GPG key
    sudo install -m 0755 -d /etc/apt/keyrings
    sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
    sudo chmod a+r /etc/apt/keyrings/docker.asc

    # Add the repository to Apt sources:
    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
      $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
      sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    sudo apt-get update -y

    # Install required docker packages
    sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

    # Add user to docker group
    sudo usermod -aG docker ${USER}

    # Verify successful install
    if ! command -v docker &> /dev/null; then
        echo "Failed to install docker, please try manually."
        exit 1
    fi
fi

# # Install Docker Compose if not installed (double check, can have issues with docker-compose install)
if ! command -v docker-compose &> /dev/null; then
    echo "Docker Compose not found. Installing..."
    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    echo "Docker Compose installed successfully!"
else
    echo "Docker Compose is already installed."
fi

# Install python3/pip
sudo apt-get install -y python3 python3-pip

# Install browsers and their respective webdrivers
sudo apt-get update && apt-get install -y \
    wget unzip xvfb \
    chromium chromium-driver 

# Install pip dependencies from 'apt_dependencies.txt'
pip install -r apt_dependencies.txt