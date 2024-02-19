# git_handler.py
import subprocess
import time


class GitHandler:
    def __init__(self, logger = None, repo_path=''):
        self.repo_path = repo_path
        # Setup logger with the specified log directory if provided
        self.logger = logger

    def run_git_command(self, command, cwd=None):
        if cwd is None:
            cwd = self.repo_path
        self.logger.info(f"Executing command: git {command}")
        try:
            output = subprocess.check_output(["git"] + command.split(), cwd=cwd, stderr=subprocess.STDOUT, text=True)
            self.logger.info("Command output:\n" + output)
            return output
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Error running git command {command} in {cwd}: {e.output}")
            return None
        finally:
            self.logger.info("Waiting for 3 seconds...")
            time.sleep(3)  # Pause for 3 seconds

    def fetch_all_branches(self):
        return self.run_git_command("fetch --all")

    def get_remote_branches(self):
        branches = self.run_git_command("branch -r")
        if branches:
            branch_list = [branch.strip() for branch in branches.split("\n") if "->" not in branch]
            return [branch.split("/", 1)[1] for branch in branch_list if branch.startswith("origin/")]
        return []

    def checkout_branches_as_local(self, branches):
        existing_branches = self.get_local_branches()
        for branch in branches:
            if branch not in existing_branches:
                self.run_git_command(f"checkout -b {branch} origin/{branch}")
            else:
                self.logger.info(f"Branch {branch} already exists locally, skipping checkout.")

    def get_local_branches(self):
        branches = self.run_git_command("branch")
        if branches:
            return [branch.strip().lstrip('* ') for branch in branches.splitlines()]
        return []
