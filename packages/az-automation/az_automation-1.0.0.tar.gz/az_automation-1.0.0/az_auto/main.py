# main.py
import argparse
import colorama
import os
from az_auto.azure_backup import AzureDevOpsHandler

def main():
    colorama.init()

    parser = argparse.ArgumentParser(description="Azure DevOps Backup CLI")
    parser.add_argument("org_url", help="URL of the Azure DevOps organization")
    parser.add_argument("dir", help="Name of the backup directory")
    args = parser.parse_args()

    organization_url = args.org_url
    backup_directory = args.dir

    azure_devops_handler = AzureDevOpsHandler(organization_url, backup_directory, backup_directory)
    projects = azure_devops_handler.list_projects()

    for project in projects:
        azure_devops_handler.clone_repositories(project)

if __name__ == "__main__":
    main()
