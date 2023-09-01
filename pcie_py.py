import pyudev
import json
import subprocess
import re

# Function to categorize PCI devices based on their names
def categorize_pcie_device(device_name):
    # Define patterns for different categories
    network_patterns = [r'Ethernet', r'NIC', r'LAN', r'WLAN']
    cpu_patterns = [r'CPU', r'Processor']
    gpu_patterns = [r'GPU', r'Graphics', r'UHD', r'HD']
    usb_patterns = [r'USB', r'Hub']
    wifi_patterns = [r'WiFi', r'Wireless', r'Wi-Fi']
    harddisk_patterns = [r'SSD', r'HDD']
    pcicard_patterns = [r'PCI', r'PCIe']
    audio_patterns = [r'Audio', r'Sound']
    mem_patterns = [r'RAM', r'ROM',r'SRAM', r'DRAM']

    # Check if the device name matches any category pattern
    for pattern in network_patterns:
        if re.search(pattern, device_name, re.IGNORECASE):
            return "Network Device"

    for pattern in cpu_patterns:
        if re.search(pattern, device_name, re.IGNORECASE):
            return "CPU Device"

    for pattern in gpu_patterns:
        if re.search(pattern, device_name, re.IGNORECASE):
            return "GPU Device"

    for pattern in usb_patterns:
        if re.search(pattern, device_name, re.IGNORECASE):
            return "USB Device"

    for pattern in wifi_patterns:
        if re.search(pattern, device_name, re.IGNORECASE):
            return "Wi-Fi Device"
            
    for pattern in harddisk_patterns:
        if re.search(pattern, device_name, re.IGNORECASE):
            return "Hard Disk"
            
    for pattern in pcicard_patterns:
        if re.search(pattern, device_name, re.IGNORECASE):
            return "PCI Card"
            
    for pattern in audio_patterns:
        if re.search(pattern, device_name, re.IGNORECASE):
            return "Audio Device"

    for pattern in mem_patterns:
        if re.search(pattern, device_name, re.IGNORECASE):
            return "Memory Device"
            
    # If no specific category is matched, return "Uncategorized"
    return "Uncategorized"

# Function to fetch dmesg logs with a filter string
def get_dmesg_logs(filter_str):
    try:
        output = subprocess.check_output(['dmesg'], universal_newlines=True)
        lines = output.split('\n')
        return [line for line in lines if filter_str in line]
    except Exception as e:
        print(f"Error occurred while fetching dmesg logs: {str(e)}")
        return []

# Create a context for pyudev
context = pyudev.Context()

# Create a dictionary to hold vendor-device data
vendor_device_data = {}

# Print all available subsystems
subsystems = set()
for device in context.list_devices():
    subsystems.add(device.subsystem)

# Iterate over all PCI devices
for device in context.list_devices(subsystem='pci'):
    # Retrieve vendor, device, slot ID, and class information
    vendor = device.get('ID_VENDOR_FROM_DATABASE')
    device_name = device.get('ID_MODEL_FROM_DATABASE')
    device_class = device.get('ID_PCI_CLASS_FROM_DATABASE')
    slot_id = device.get('PCI_SLOT_NAME')
    subsys_id = device.get('PCI_SUBSYS_ID')
    dev_path = device.get('DEVPATH')
    init_time = device.get('USEC_INITIALIZED')
    driver = device.get('DRIVER')

    # If vendor and device information is available, add to dictionary
    if vendor and device_name:
        if vendor not in vendor_device_data:
            vendor_device_data[vendor] = []
        vendor_device_data[vendor].append((device_name, device_class, slot_id, subsys_id, dev_path, init_time, driver))

# Function to create the PCI device information JSON structure
def create_pci_info():
    pci_info = {
        "tree": {
            "nodeName": "PCI info",
            "name": "PCI info",
            "type": "type3",
            "dname": "",
            "class": "",
            "slotID": "",
            "subsys_id": "",
            "dev_path": "",
            "init_time": "",
            "driver": "",
            "link": {
                "name": "",
                "nodeName": "PCI info"
            },
            "children": []
        }
    }

    for vendor, devices in vendor_device_data.items():
        vendor_node = {
            "nodeName": "Vendor",
            "name": "Vendor",
            "type": "type1",
            "dname": vendor,
            "class": "",
            "slotID": "",
            "subsys_id": "",
            "dev_path": "",
            "init_time": "",
            "driver": "",
            "link": {
                "name": f"Link node 1 to {vendor}",
                "nodeName": f"NODE NAME {vendor}",
                "direction": "SYNC"
            },
            "children": []
        }

        # Create a dictionary to hold devices categorized by their names for this vendor
        categorized_devices = {}

        for device_name, device_class, slot_id, subsys_id, dev_path, init_time, driver in devices:
            # Categorize devices based on their names for this vendor
            category = categorize_pcie_device(device_name)

            if category not in categorized_devices:
                categorized_devices[category] = []

            categorized_devices[category].append({
                "nodeName": "Device",
                "name": "Device",
                "type": "type2",
                "dname": device_name,
                "class": device_class if device_class else "",
                "slotID": slot_id if slot_id else "",
                "subsys_id": subsys_id if subsys_id else "",
                "dev_path": dev_path if dev_path else "",
                "init_time": init_time if init_time else "",
                "driver": driver if driver else "",
                "link": {
                    "name": f"Link node {vendor} to {device_name}",
                    "nodeName": f"NODE NAME {device_name}",
                    "direction": "ASYN"
                },
                "children": [
                    {
                        "nodeName": "Logs",
                        "name": "Logs",
                        "type": "type4",
                        "dname": "\n\n".join(get_dmesg_logs(slot_id)),  # Get dmesg logs related to this device
                        "link": {
                            "name": "Link Logs node to Vendor node",
                            "nodeName": "NODE NAME Logs",
                            "direction": "SYNC"
                        },
                        "children": []
                    },
                    {
                        "nodeName": "More info",
                        "name": "More info",
                        "type": "type4",
                        "dname": "Class: " + (device_class if device_class else "") + "\n" + "Slot_ID: " + (
                            slot_id if slot_id else "") + "Subsys_ID: " + (subsys_id if subsys_id else "") + "\n" + "Dev_path: " + (
                                            dev_path if dev_path else "") + "\n" + "Init_time: " + (
                                            init_time if init_time else "") + "\n" + "Driver: " + (
                                            driver if driver else "") + "\n",
                        "link": {
                            "name": "Link Logs node to Vendor node",
                            "nodeName": "NODE NAME Logs",
                            "direction": "SYNC"
                        },
                        "children": []
                    }

                ]
            })

        # Create "Category" nodes and add categorized devices under them for this vendor
        for category, devices in categorized_devices.items():
            category_node = {
                "nodeName": "Category",
                "name": "Category",
                "type": "type1",
                "dname": category,
                "class": "",
                "slotID": "",
                "subsys_id": "",
                "dev_path": "",
                "init_time": "",
                "driver": "",
                "link": {
                    "name": f"Link node 1 to {category}",
                    "nodeName": f"NODE NAME {category}",
                    "direction": "SYNC"
                },
                "children": devices  # Add categorized devices as children of the "Category" node
            }

            vendor_node["children"].append(category_node)

        pci_info["tree"]["children"].append(vendor_node)

    return pci_info

# Get the PCI information
pci_info = create_pci_info()

# Write the JSON to a file
with open('pci_info.json', 'w') as f:
    json.dump(pci_info, f, indent=4)

