# Device-analyzer

# PCIe Log Analyzer Application

The PCIe Log Analyzer Application is a web-based tool that allows you to analyze and visualize PCIe devices and their log information. It provides a user-friendly interface for viewing PCIe devices and driver details. The application also comes with an automatic setup script that installs necessary dependencies, sets up a service for boot-time information retrieval, and creates a desktop shortcut for easy access.

## Features

- View detailed PCIe devices and log information.
- Interactive visualization of PCIe device data.
- Easy-to-use interface.
- Automatic setup script for easy installation and configuration.

## Getting Started

### Prerequisites

- Python3: The script requires Python3 to run. If it's not already installed, the script will attempt to install it using `apt-get`.
- npm: npm is required for package management. If it's not already installed, the script will attempt to install it using `apt-get`.
- Node.js: This application uses Node.js to run the Live Server. If Node.js is not installed, you need to install it manually. You can download it from [the official Node.js website](https://nodejs.org/).
- live-server (npm packages)
  
### Installation

1. Clone the repository to your local machine:

   
   git clone https://github.com/vijayakumarmani2/Device-analyzer.git
   
   cd pcie-analyzer
   

3. Install the necessary dependencies and set up the application:

   ./start_app.sh
   

   This script will:
   - Create a `.service` to provide PCIe information at boot time.
   - Install necessary dependencies including Node.js and Live Server.
   - Start the application using Live Server.
   - Create a desktop shortcut for easy access.

4. Open your web browser and navigate to `http://localhost:8080` to access the application.

## Running in the Background

To run the application in the background (without displaying console output), use the following command:

./start_app.sh

## Debugging Mode

You can run the application in debugging mode with the -d argument. The benefit of using this mode is that it displays all console output, which can be helpful for troubleshooting and monitoring the application.

./start_app.sh -d

## Directory Structure

- `/var/pcie_analyzer/`: Directory for hosting the application and data.
- `/usr/share/applications/`: Location of the desktop shortcut for launching the application.
- `start_app.sh`: Bash script to start the application, set up services, and create the desktop shortcut.

## Contributing

Contributions are welcome! If you find a bug or have a feature request, please create an issue in the repository. Pull requests are also encouraged.

## License

This project is licensed under the [MIT License](LICENSE).

---

Developed by [vijayakumarmani2](https://github.com/your-username)
```

Feel free to customize the above template with your specific details and adjust any paths or descriptions to match your project structure.
