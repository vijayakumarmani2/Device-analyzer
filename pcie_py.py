
import pyudev
import json
import subprocess
import os

def get_dmesg_logs(filter_str):
    try:
        output = subprocess.check_output(['dmesg'], universal_newlines=True)
        lines = output.split('\n')
       # print(lines);
        return [line for line in lines if filter_str in line]
    except Exception as e:
        print(f"Error occurred while fetching dmesg logs: {str(e)}")
        return []
    
def create_pci_info():
    # Create a context for pyudev
    context = pyudev.Context()

    # Create a dictionary to hold vendor-device data
    vendor_device_data = {}

    
    
    # Print all available subsystems
    subsystems = set()
    for device in context.list_devices():
        subsystems.add(device.subsystem)
   # print("All available subsystems:", subsystems)

    # Iterate over all PCI devices
    for device in context.list_devices(subsystem='pci'):
        # Print all available properties for the device
        # print("Device properties for", device, ":")
        #for prop in device.properties:
           # print(prop, ":", device.get(prop))

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

    # Use the vendor-device data to create the JSON structure
    pci_info = {
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
        for device_name, device_class, slot_id, subsys_id, dev_path, init_time,driver in devices:
            dmesg_logs = get_dmesg_logs(slot_id)  # Get dmesg logs related to this device
            device_node = {
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
                "dname": "\n\n".join(dmesg_logs),
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
                "dname": "Class: "+(device_class if device_class else "")+"\n"+"Slot_ID: "+(slot_id if slot_id else "")+"Subsys_ID: "+(subsys_id if subsys_id else "")+"\n"+"Dev_path: "+(dev_path if dev_path else "")+"\n"+"Init_time: "+(init_time if init_time else "")+"\n"+"Driver: "+(driver if driver else "")+"\n",
                "link": {
                    "name": "Link Logs node to Vendor node",
                    "nodeName": "NODE NAME Logs",
                    "direction": "SYNC"
                },
                "children": []
            }
            
            ]
            }
            vendor_node["children"].append(device_node)
        pci_info["children"].append(vendor_node)
    
    return {"tree": pci_info}

# Get the PCI information
pci_info = create_pci_info()

# Write the JSON to a file
with open('/var/pcie_analyzer/pci_info.json', 'w') as f:
    json.dump(pci_info, f, indent=4)
os.chmod('/var/pcie_analyzer/pci_info.json', 0o777)

