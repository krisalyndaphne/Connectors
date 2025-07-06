# GitHub Manager Agent

A lightweight Python helper class that wraps common GitHub repository management operations (list, clone, create, delete, push, describe). It combines GitHub's REST API v3 (via the `requests` library) with local `git` CLI calls (via `subprocess`).

## 🎯 Features

- ✅ **List** all repositories under a GitHub user or organization
- 📁 **Clone** repositories to local disk
- 📝 **Create** a new repository
- 🗑️ **Delete** a repository (with confirmation)
- 🔄 **Push** local code changes to a specified repository
- 🔍 **Display** repo details (description, stars, forks, language, etc.)

## 📋 Requirements

- **Python 3.8+**
- **Git CLI** installed and accessible in PATH
- **GitHub Personal Access Token** (for authenticated operations)

## 🚀 Installation

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set your GitHub Personal Access Token:**
   ```bash
   # Linux/Mac
   export GITHUB_TOKEN=your_token_here
   
   # Windows PowerShell
   $env:GITHUB_TOKEN = "your_token_here"
   ```

## 💻 Usage

### Command Line Interface

```bash
# List repositories for a user/organization
python github_manager_agent.py list octocat

# Clone a repository
python github_manager_agent.py clone https://github.com/owner/repo.git [destination]

# Create a new repository
python github_manager_agent.py create my-new-repo --public

# Delete a repository (requires confirmation)
python github_manager_agent.py delete owner/repo --confirm

# Push local changes
python github_manager_agent.py push ./my-project -m "My commit message"

# Get repository details
python github_manager_agent.py details owner/repo
```

### Python API

```python
from github_manager_agent import GitHubManagerAgent

# Initialize agent (uses GITHUB_TOKEN env var)
agent = GitHubManagerAgent()

# List repositories
repos = agent.list_repositories("octocat")
print(repos)

# Get repository details
details = agent.get_repo_details("octocat/Hello-World")
print(f"Stars: {details['stars']}, Language: {details['language']}")

# Clone repository
agent.clone_repository("https://github.com/octocat/Hello-World.git", "./hello-world")

# Create repository
repo = agent.create_repository("my-new-repo", private=False)
print(f"Created: {repo['html_url']}")
```

## 🔐 Authentication

Most operations require a **GitHub Personal Access Token** with appropriate scopes:

- `public_repo` scope for public repositories
- `repo` scope for private repositories  
- `delete_repo` scope for repository deletion

**Create a token at:** `https://github.com/settings/tokens`

## ⚠️ Error Handling

The agent raises `GitHubAPIError` for API-related issues and `RuntimeError` for git command failures. All destructive operations (like delete) require explicit confirmation.

## 📖 API Reference

### GitHubManagerAgent Methods

| Method | Description | Parameters |
|--------|-------------|------------|
| `list_repositories(user_or_org)` | List all repos for user/org | `user_or_org`: GitHub username or org name |
| `clone_repository(repo_url, destination)` | Clone repo to local disk | `repo_url`: GitHub repo URL, `destination`: local path |
| `create_repository(name, private, org)` | Create new repository | `name`: repo name, `private`: bool, `org`: org name (optional) |
| `delete_repository(full_name, confirm)` | Delete repository | `full_name`: owner/repo, `confirm`: must be True |
| `push_changes(local_path, commit_message)` | Push local changes | `local_path`: git repo path, `commit_message`: commit msg |
| `get_repo_details(full_name)` | Get repository metadata | `full_name`: owner/repo format |

---

**Made with ❤️ for GitHub automation**

