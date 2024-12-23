import scansuite_cli
import sys
import time
import argparse

def get_user_input(prompt):
    return input(prompt)

# Set up argument parser
parser = argparse.ArgumentParser(description="Run a static code scan using scansuite_cli.")
parser.add_argument("-s", "--server_url", type=str, help="Target server URL")
parser.add_argument("-u", "--username", type=str, help="Username for authentication")
parser.add_argument("-p", "--password", type=str, help="Password for authentication")
parser.add_argument("-l", "--lang", type=str, help="Programming language of the scan")
parser.add_argument("-f", "--file_path", type=str, help="Path to the file to be scanned including the filename")

args = parser.parse_args()

# Prompt for missing arguments
server_url = args.server_url or get_user_input("Enter server URL: ")
username = args.username or get_user_input("Enter username: ")
password = args.password or get_user_input("Enter password: ")
lang = args.lang or get_user_input("Enter programming language: ")
file_path = args.file_path or get_user_input("Enter file path: ")

# Scanners configuration
scanners_list = {
    "semgrep_local": "on",
    "semgrep_gitlab": "on",
    "gitleaks": "on",
    "trufflehog": "on",
    "parker": "on",
    "dep_trivy": "on",
    "dep_osv": "on",
    "iacs_kics": "on"
}

# Login
cookie = scansuite_cli.login(server_url, username, password)
if not cookie:
    sys.exit("Login failed. Exiting.")

file_name = scansuite_cli.extract_file_name(file_path)

# Create new product
product_name = file_name
engid = scansuite_cli.create_product(server_url, cookie, product_name)
if not engid:
    sys.exit("Failed to create product. Exiting.")

# Initiate new static scan
scanid = scansuite_cli.static_scan_file(server_url, cookie, lang, engid, file_path, scanners_list)
if not scanid:
    sys.exit("Failed to initiate static scan. Exiting.")

# Example of the new scan status check
scan_status = scansuite_cli.get_scan_status(server_url, cookie, scanid)
if scan_status:
    print(f"Scan {scanid} is with status {scan_status}")
