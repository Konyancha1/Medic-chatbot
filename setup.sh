#!/bin/bash

# Install Python and pip
apt-get update
apt-get install -y python3 python3-pip

# Create virtual environment
python3 -m venv env

# Activate virtual environment
source env/bin/activate

# Install dependencies
pip install -r requirements.txt