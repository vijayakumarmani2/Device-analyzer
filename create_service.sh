#!/bin/bash

# Define variables
COMMON_PATH="/var/"
PYTHON_SCRIPT_PATH="pcie_py.py"

# Create a directory in the common path
mkdir -p "$COMMON_PATH/pcie_log_analyzer"

# Copy the Python script to the common directory
cp "$PYTHON_SCRIPT_PATH" "$COMMON_PATH/pcie_log_analyzer/"

sudo chmod 777 "$COMMON_PATH/pcie_log_analyzer/"

# Create the .service file
echo "[Unit]" > pcie_log_analyzer.service
echo "Description=Your Application Service" >> pcie_log_analyzer.service
echo "" >> pcie_log_analyzer.service
echo "[Service]" >> pcie_log_analyzer.service
echo "ExecStart=/usr/bin/python3 $COMMON_PATH/pcie_log_analyzer/pcie_py.py" >> pcie_log_analyzer.service
echo "Restart=always" >> pcie_log_analyzer.service
echo "" >> pcie_log_analyzer.service
echo "[Install]" >> pcie_log_analyzer.service
echo "WantedBy=multi-user.target" >> pcie_log_analyzer.service

# Move the .service file to the appropriate location
sudo mv pcie_log_analyzer.service /etc/systemd/system/

# Reload systemd to recognize the new service
sudo systemctl daemon-reload

