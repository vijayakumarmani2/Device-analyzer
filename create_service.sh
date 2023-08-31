#!/bin/bash

# Define variables
COMMON_PATH="/var/"
PYTHON_SCRIPT_PATH="pcie_py.py"

# Create a directory in the common path
mkdir -p "$COMMON_PATH/pcie_analyzer"

# Copy the Python script to the common directory
cp "$PYTHON_SCRIPT_PATH" "$COMMON_PATH/pcie_analyzer/"

sudo chmod 777 "$COMMON_PATH/pcie_analyzer/"

# Create the .service file
echo "[Unit]" > pcie_analyzer.service
echo "Description=Your Application Service" >> pcie_analyzer.service
echo "" >> pcie_analyzer.service
echo "[Service]" >> pcie_analyzer.service
echo "ExecStart=/usr/bin/python3 $COMMON_PATH/pcie_analyzer/pcie_py.py" >> pcie_analyzer.service
echo "Restart=always" >> pcie_analyzer.service
echo "" >> pcie_analyzer.service
echo "[Install]" >> pcie_analyzer.service
echo "WantedBy=multi-user.target" >> pcie_analyzer.service

# Move the .service file to the appropriate location
sudo mv pcie_analyzer.service /etc/systemd/system/

# Reload systemd to recognize the new service
sudo systemctl daemon-reload

