GitHub Manager Agent
====================

This repository contains `github_manager_agent.py`, a lightweight Python helper class for common GitHub operations (list, clone, create, delete, push, describe) using the GitHub REST API and git CLI.

Quick start:
1. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```
2. Export a Personal Access Token (with `repo` scope):
   ```bash
   export GITHUB_TOKEN=<your_token>
   ```
3. List your repositories
   ```bash
   python github_manager_agent.py list <your_user>
   ```

