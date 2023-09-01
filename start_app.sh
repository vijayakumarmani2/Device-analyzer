#!/bin/bash


# Function to start the application
start_application() {
# Check if myapp.service is already running
if ! systemctl is-active --quiet pcie_analyzer.service; then
    echo "myapp.service is not running. Setting up the service..."
    
    # Run the script to create and enable the service
    bash create_service.sh
    echo "now, myapp.service is running."
else
    echo "myapp.service is already running."
fi

# Get the directory path of the script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Check if Node.js is installed
if ! command -v node &>/dev/null; then
    echo "Node.js is required to run this application. Please install Node.js and try again."
    exit 1
fi

# Check if live-server is installed globally
if ! command -v live-server &>/dev/null; then
    echo "Installing live-server globally..."
    apt-get install npm
    npm install -g live-server
fi

# Navigate to the application directory
cd "$SCRIPT_DIR"

# Copy all files from the current folder to /var/pcie_analyzer/
cp -r . /var/pcie_analyzer/

chmod -R 777 /var/pcie_analyzer/*

# Navigate to /var/pcie_analyzer/
cd /var/pcie_analyzer/

cp /var/pcie_analyzer/pci_card.png /usr/share/icons/

echo "Your application is now running. Open your web browser and navigate to http://localhost:8080"

# Create the desktop shortcut script
DESKTOP_FILE="PCIe_Analyzer.desktop"

echo "[Desktop Entry]" >> "$DESKTOP_FILE"
echo "Version=1.0" >> "$DESKTOP_FILE"
echo "Name=PCIe_Analyzer" >> "$DESKTOP_FILE"
echo "Comment=Launch PCIe_Analyzer Application" >> "$DESKTOP_FILE"
echo "Exec=xdg-open http://localhost:8080" >> "$DESKTOP_FILE"
echo "Icon=pci_card" >> "$DESKTOP_FILE"
echo "Terminal=false" >> "$DESKTOP_FILE"
echo "Type=Application" >> "$DESKTOP_FILE"
echo "Categories=Utility;Application;" >> "$DESKTOP_FILE"
# Make the desktop shortcut script executable
chmod +x "$DESKTOP_FILE"


cp /var/pcie_analyzer/$DESKTOP_FILE /usr/share/applications/
echo "Executed the desktop shortcut"
# Start the live-server on a specific port (e.g., 8080)
live-server --port=8080 &

}

# Check for the '-d' argument
if [[ "$1" == "-d" ]]; then
    # Run the application with debug mode (show all console output)
    start_application
else
    # Run the application in the background (suppress console output)
    start_application > /dev/null 2>&1 &
    echo "Application started in the background."
fi
