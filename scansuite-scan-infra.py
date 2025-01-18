import scansuite_cli
import time
import sys
import argparse
from datetime import datetime

def get_user_input(prompt):
    return input(prompt)

# Set up argument parser
parser = argparse.ArgumentParser(description="Run an infrastructure scan using scansuite_cli.")
parser.add_argument("-s", "--server_url", type=str, help="Target server URL")
parser.add_argument("-u", "--username", type=str, help="Username for authentication")
parser.add_argument("-p", "--password", type=str, help="Password for authentication")
parser.add_argument("-t", "--targets", type=str, help="Targets to scan")
parser.add_argument("-g", "--ping", type=str, default="No", help="Ping options (default: No)")
parser.add_argument("-r", "--ports", type=str, default="All TCP", help="Ports to scan (default: All TCP)")
parser.add_argument("-y", "--scan_type", type=str, default="vulnerability_scan", help="Type of scan to perform")
parser.add_argument("-n", "--product_name", type=str, help="Product name (optional, defaults to current date and time)")

# Possible scan_type values (specify via command line parameter):
# vulnerability_scan
# nmap_scan
# nmap_linux_patching
# subdomain_enum
# docker_image_scan

args = parser.parse_args()

# Prompt for missing arguments
server_url = args.server_url or get_user_input("Enter server URL: ")
username = args.username or get_user_input("Enter username: ")
password = args.password or get_user_input("Enter password: ")
targets = args.targets or get_user_input("Enter comma separated targets list: ")
ping = args.ping
ports = args.ports
scan_type = args.scan_type or get_user_input("Enter scan type: ")
product_name = args.product_name or datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

# Scanners configuration

# All available scanners for vulnerability_scan type:
# vuln_scanners = {
#     "openvas":"on",
#     "nessus":"on",
#     "nuclei_local":"on",
#     "nuclei_custom":"on"
#     }

vuln_scanners = {
    "openvas":"on",
    "nessus":"on",
    "nuclei_local":"on",
    "nuclei_custom":"on"
}

# Login
cookie = scansuite_cli.login(server_url, username, password)
if not cookie:
    sys.exit("Login failed. Exiting.")

# Create new product
# Product name should be unique
engid = scansuite_cli.create_product(server_url, cookie, product_name)
if not engid:
    sys.exit("Failed to create product. Exiting.")

# Start infrastructure scan
scanid = scansuite_cli.infra_scan(
    server_url, cookie, targets, engid.split(",")[1], ping, ports, scan_type, vuln_scanners
)
if not scanid:
    sys.exit("Failed to initiate infrastructure scan. Exiting.")

# Example of the new scan status check
scan_status = scansuite_cli.get_scan_status(server_url, cookie, scanid)
if scan_status:
    print(f"Scan {scanid} is with status {scan_status}")
