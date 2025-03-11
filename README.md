## ScanSuite Command Line Tool

This tool allows to interact with ScanSuite server remotely, submit scans, query scan statuses, retrieve reports etc.

### Executing the scripts

Every .py script automates specific task and expects at least the ScanSuite server URL, username and password to be provided.

Password can be provided either inline with `-p` parameter or entered via promped field, same as other mandatory fields.

List of the invoked scanners are hardcoded in the scripts and should be amended there.

Execute `python scansuite-scan-...py -h` for each script to list all accepted parameters and expected values.

### Static code analysis

Provide the code archive in ZIP format:

```
python scansuite-scan-zip.py -s "https://my-scansuite-server.com" -u user -l java -f /path/to/test.zip
```

Scan the Git repository:

```
python scansuite-scan-git.py -s "https://my-scansuite-server.com" -u user -l python -g "https://github.com/NetSPI/django.nV"
```

### Dynamic web scan

```
python scansuite-scan-web.py -s "https://my-scansuite-server.com" -u user -w "https://scanthisserver.com, https://anotherserver.edu"

```

### Infrastructure scan

```
python scansuite-scan-infra.py -s "https://my-scansuite-server.com" -u admin -t "192.168.23.3, 192.168.24.0/24" --ping "No" --ports "All TCP" --scan_type "vulnerability_scan" --product_name "DMZ Scan January"
```

### Dumping BitBucket repositories

Script serves specific usecase when local BitBucket server is in use, containing projects with code repositories.

* Specify local BitBucket server name in the script.
* Obtain the HTTP key/token from the BitBucket user profile.
* Submit it to the script along with the comma separated list of project names and, optionally, specific repositories.

The script will download required repositories from the given project and make and archive from them, suitable to upload to ScanSuite for further static code analysis.
BitBucket token can be provided either inline with `--token` parameter or entered via promped field, same as other mandatory fields.

This will clone and ZIP all repos from given projects:

```
python bitbucket-clone-projects-repos.py --token YOUR_TOKEN --projects PROJONE,PROJTWO
```

This will clone and ZIP specified repos from given projects:

```
python bitbucket-clone-projects-repos.py --token YOUR_TOKEN --projects PROJONE --repos mycode-repository,another-repository,
```

