# azure_backup.py
import os
import subprocess
import json
import time
from az_auto.utils.logger_config import setup_logger
from az_auto.git_handler import GitHandler

logger = setup_logger(__name__)


class AzureDevOpsHandler:
    def __init__(self, organization_url, clone_directory, log_directory):
        self.organization_url = organization_url
        self.clone_directory = clone_directory
        # Setup logger with the specified log directory
        self.logger = setup_logger(__name__, log_directory)

    def run_az_command(self, command):
        self.logger.info(f"Executing command: {command}")
        try:
            time.sleep(3)  # Pause for 3 seconds
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True)
            if result.returncode == 0:
                self.logger.info(f"Command output:\n{json.dumps(json.loads(result.stdout), indent=4)}")
                return result.stdout
            else:
                self.logger.error(f"Command failed: {result.stderr}")
                raise Exception(f"Command failed: {result.stderr}")
        except Exception as e:
            self.logger.error(f"Error executing command: {command}\n{e}")
            raise e

    def list_projects(self):
        command = f'az devops project list --organization "{self.organization_url}" --query "value[].name" -o json'
        output = self.run_az_command(command)
        return json.loads(output)

    def clone_repositories(self, project_name):
        repos_command = f'az repos list --organization "{self.organization_url}" --project "{project_name}" --query "[].remoteUrl" -o json'
        repos_output = self.run_az_command(repos_command)
        repos = json.loads(repos_output)

        git_handler = GitHandler(logger)  # Instantiate GitHandler

        for repo_url in repos:
            repo_url = repo_url.strip("'")
            repo_name = repo_url.split('/')[-1]

            project_directory = os.path.join(self.clone_directory, project_name)
            clone_directory = os.path.join(project_directory, repo_name)
            git_handler.run_git_command(f"clone {repo_url} {clone_directory}", cwd=".")

            # Set the repository path in GitHandler to the cloned repository's directory
            git_handler.repo_path = clone_directory

            # Fetch all branches
            git_handler.fetch_all_branches()

            # Get list of remote branches
            remote_branches = git_handler.get_remote_branches()

            # Checkout each remote branch as local
            git_handler.checkout_branches_as_local(remote_branches)
