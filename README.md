## ScanSuite Command Line Tool

This tool allows to interact with ScanSuite server remotely, submit scans, query scan statuses, retrieve reports etc.

### Static code analysis

Provide the code archive in ZIP format:

```
python scansuite-scan-zip.py -s "https://my-scansuite-server.com" -u user -l python -f /path/to/test.zip
```

Use `python scansuite-scan-zip.py -h` for all accepted parameters and expected values.

Scan the Git repository:

```
python .\scansuite-scan-git.py -s "https://eval.scansuite.ru" -u user -l python -g "https://github.com/NetSPI/django.nV"
```

Password can be provided inline with `-p` parameter or entered via promped field, same as other mandatory fields.

List of the invoked scanners are hardcoded in the scripts and should be amended there.

### Dynamic web scan

```
python scansuite-scan-web.py -s "https://my-scansuite-server.com" -u user -w "https://scanthisserver.com, https://anotherserver.edu"

```

### Infrastructure scan

```
python .\scansuite-scan-infra.py -s "https://eval.scansuite.ru" -u admin -t "192.168.23.3, 192.168.24.0/24" --ping "No" --ports "All TCP" --scan_type "vulnerability_scan" --product_name "DMZ Scan January"
```

Possible scan_type options:
vulnerability_scan
nmap_scan
nmap_linux_patching
subdomain_enum
docker_image_scan