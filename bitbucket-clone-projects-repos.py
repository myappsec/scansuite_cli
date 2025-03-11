import requests
import subprocess
import argparse
import shutil
import os

# Bitbucket Server Configuration
BITBUCKET_URL = "https://bitbucket.yourdomain.local/rest/api/1.0"
SSH_URL_TEMPLATE = "ssh://git@bitbucket.yourdomain.local:7999/{}/{}.git"

# Disable SSL warnings (optional)
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

def get_repositories(project_key, access_token):
    """Fetches all repositories in a project."""
    repos = []
    start = 0

    while True:
        url = f"{BITBUCKET_URL}/projects/{project_key}/repos?start={start}"
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(url, headers=headers, verify=False)
        if response.status_code != 200:
            print(f"Failed to fetch repositories for {project_key}: {response.text}")
            return []

        data = response.json()
        repos.extend(data.get("values", []))

        if data.get("isLastPage", True):
            break

        start = data.get("nextPageStart", start + len(data.get("values", [])))

    return repos

def clone_repository(project_key, repo_slug):
    """Clones a repository over SSH."""
    ssh_url = SSH_URL_TEMPLATE.format(project_key, repo_slug)
    print(f"Cloning {repo_slug} from {ssh_url} ...")

    try:
        subprocess.run(["git", "clone", ssh_url], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to clone {repo_slug}: {e}")

def process_projects(projects_input, repos_input, access_token):
    """Processes project and repo input, then clones accordingly."""
    projects = projects_input.split(",") if projects_input else []
    repos_dict = {
        proj_repo: repos_input.split(",") if repos_input else []
        for proj_repo in (projects_input.split(",") if projects_input else [])
    }

    print (repos_dict)
    all_repos = []

    for project_key in projects:
        print (f"project_key {project_key}")
        repo_list = repos_dict.get(project_key, [])
        print (f"repo_list {repo_list}")
        all_repos = get_repositories(project_key, access_token)

        if not all_repos:
            print(f"No repositories found for project {project_key}.")
            continue

        print (all_repos)
        os.makedirs(project_key, exist_ok=True)
        os.chdir(project_key)

        if repo_list:

            # Clone only specified repositories
            for repo in repo_list:
                print (f"Checking download link for {repo}")
                if any(r["slug"] == repo for r in all_repos):
                    print (f"Cloning {repo}")
                    clone_repository(project_key, repo)
                else:
                    print(f"Repository '{repo}' not found in project '{project_key}'. Skipping.")
        else:
            for repo in all_repos:
                clone_repository(project_key, repo["slug"])

        os.chdir("..")
        zip_path = shutil.make_archive(project_key, 'zip', project_key)
        zip_size = os.path.getsize(zip_path) / (1024 * 1024)
        print (f"{zip_path} created with size {zip_size:.2f} MB")

        if zip_size > 250:
            print ("The file size exceeds 250Mb. Too big to upload to ScanSuite")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clone specific or all repositories from a Bitbucket project.")
    parser.add_argument("--projects", type=str, help="Comma-separated list of project keys.")
    parser.add_argument("--repos", type=str, help="Comma-separated list of repos (format: project:repo1,repo2)")
    parser.add_argument("--token", type=str, help="Bitbucket Access Token")

    args = parser.parse_args()

    projects = args.projects or input("Enter BitBucket project name: ")
    repos = args.repos or ""
    token = args.token or input("BitBucket http access token: ")

    process_projects(projects, repos, token)
