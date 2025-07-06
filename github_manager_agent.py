"""
GitHub Manager Agent
====================
A lightweight Python helper class that wraps common GitHub repository management
operations (list, clone, create, delete, push, describe). It combines GitHub’s
REST API v3 (via the ``requests`` library) with local ``git`` CLI calls (via
``subprocess``).

Usage example
-------------
>>> from github_manager_agent import GitHubManagerAgent
>>> agent = GitHubManagerAgent()
>>> agent.list_repositories("octocat")
['Spoon-Knife', 'Hello-World', ...]
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional

import requests

__all__ = [
    "GitHubManagerAgent",
    "GitHubAPIError",
]


class GitHubAPIError(RuntimeError):
    """Raised when the GitHub API returns an error response."""

    def __init__(self, status_code: int, message: str):
        super().__init__(f"GitHub API error {status_code}: {message}")
        self.status_code = status_code
        self.message = message


class GitHubManagerAgent:
    """A minimal agent for managing GitHub repositories.

    Parameters
    ----------
    token : str | None, optional
        A GitHub personal-access token. If *None*, the ``GITHUB_TOKEN``
        environment variable is used.
    api_base : str, default "https://api.github.com"
        Base-URL for GitHub’s REST API. Override for GHES / proxies.
    session : requests.Session | None, optional
        Inject an existing requests session (e.g. for retries / caching).
    """

    def __init__(
        self,
        token: Optional[str] = None,
        *,
        api_base: str = "https://api.github.com",
        session: Optional[requests.Session] = None,
    ) -> None:
        self.token = token or os.getenv("GITHUB_TOKEN")
        self.api_base = api_base.rstrip("/")
        self.session = session or requests.Session()
        # Default headers
        self.session.headers.update({
            "Accept": "application/vnd.github+json",
            "User-Agent": "GitHubManagerAgent/1.0",
        })
        # Add auth header only if we have a token (unauthenticated requests are rate-limited)
        if self.token:
            self.session.headers["Authorization"] = f"token {self.token}"

    # ---------------------------------------------------------------------
    # Public API
    # ---------------------------------------------------------------------
    def list_repositories(self, user_or_org: str, *, per_page: int = 100) -> List[str]:
        """Return a list of repository full names (``owner/name``).

        The *user_or_org* may be a user or organisation login.
        """
        # Attempt *users*; fallback to *orgs* if 404.
        for path in (f"/users/{user_or_org}/repos", f"/orgs/{user_or_org}/repos"):
            url = f"{self.api_base}{path}"
            params = {"per_page": per_page, "type": "all"}
            repos, status = self._get_paginated(url, params)
            if status != 404:
                return [repo["full_name"] for repo in repos]
        raise GitHubAPIError(404, f"User or organisation '{user_or_org}' not found")

    def clone_repository(self, repo_url: str, destination: str | Path | None = None) -> None:
        """Clone *repo_url* into *destination* directory (defaults to CWD)."""
        dest = Path(destination or ".").expanduser().resolve()
        cmd = ["git", "clone", repo_url, str(dest)] if dest != Path(".") else ["git", "clone", repo_url]
        self._run(cmd, cwd=Path.cwd())

    def create_repository(self, name: str, *, private: bool = True, org: str | None = None) -> Dict:
        """Create a new repository.

        If *org* is supplied, create under that organisation; otherwise, create under the
        authenticated user.
        """
        path = f"/orgs/{org}/repos" if org else "/user/repos"
        url = f"{self.api_base}{path}"
        payload = {"name": name, "private": private, "auto_init": False}
        response = self.session.post(url, json=payload)
        if not response.ok:
            raise GitHubAPIError(response.status_code, response.text)
        return response.json()

    def delete_repository(self, full_name: str, *, confirm: bool = False) -> None:
        """Delete repository *full_name* (format ``owner/name``).

        The caller **must** pass ``confirm=True`` to actually perform the deletion; otherwise
        a :class:`RuntimeError` is raised as a safeguard.
        """
        if not confirm:
            raise RuntimeError("Deletion not confirmed – pass confirm=True to delete the repository.")
        url = f"{self.api_base}/repos/{full_name}"
        response = self.session.delete(url)
        if response.status_code == 204:
            return
        raise GitHubAPIError(response.status_code, response.text)

    def push_changes(self, local_path: str | Path, commit_message: str = "Automated commit") -> None:
        """Stage, commit and push all changes in *local_path*."""
        path = Path(local_path).expanduser().resolve()
        if not path.is_dir():
            raise ValueError(f"{path} is not a directory")
        self._run(["git", "add", "-A"], cwd=path)
        # commit may fail if nothing to commit – ignore in that case
        self._run(["git", "commit", "-m", commit_message], cwd=path, check=False)
        self._run(["git", "push"], cwd=path)

    def get_repo_details(self, full_name: str) -> Dict:
        """Return metadata for repository *full_name* (``owner/name``)."""
        url = f"{self.api_base}/repos/{full_name}"
        response = self.session.get(url)
        if not response.ok:
            raise GitHubAPIError(response.status_code, response.text)
        data = response.json()
        return {
            "name": data["name"],
            "full_name": data["full_name"],
            "private": data["private"],
            "description": data["description"],
            "language": data["language"],
            "stars": data["stargazers_count"],
            "forks": data["forks_count"],
            "open_issues": data["open_issues_count"],
            "html_url": data["html_url"],
        }

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _get_paginated(self, url: str, params: Dict | None = None):
        results: List[Dict] = []
        page = 1
        while True:
            response = self.session.get(url, params={**(params or {}), "page": page})
            if response.status_code == 404:
                return [], 404
            if not response.ok:
                raise GitHubAPIError(response.status_code, response.text)
            batch = response.json()
            results.extend(batch)
            # GitHub paginates using Link header; stop if less than per_page
            if len(batch) < (params or {}).get("per_page", 30):
                break
            page += 1
        return results, response.status_code

    @staticmethod
    def _run(cmd: List[str], *, cwd: Path, check: bool = True) -> None:
        """Run a subprocess command with inherited stdio."""
        try:
            subprocess.run(cmd, cwd=cwd, check=check)
        except subprocess.CalledProcessError as exc:
            raise RuntimeError(f"Command '{' '.join(cmd)}' failed with exit code {exc.returncode}") from exc


# ---------------------------------------------------------------------------
# Minimal CLI for quick experimentation
# ---------------------------------------------------------------------------

def _main(argv: List[str] | None = None):  # pragma: no cover – helper
    import argparse

    argv = argv or sys.argv[1:]
    parser = argparse.ArgumentParser(description="GitHub Manager Agent")
    sub = parser.add_subparsers(dest="command", required=True)

    # list repos
    p_list = sub.add_parser("list", help="List repositories for a user/org")
    p_list.add_argument("user_or_org")

    # clone
    p_clone = sub.add_parser("clone", help="Clone repository")
    p_clone.add_argument("repo_url")
    p_clone.add_argument("destination", nargs="?", default=".")

    # create
    p_create = sub.add_parser("create", help="Create repository")
    p_create.add_argument("name")
    p_create.add_argument("--public", action="store_true")
    p_create.add_argument("--org")

    # delete
    p_delete = sub.add_parser("delete", help="Delete repository")
    p_delete.add_argument("full_name")
    p_delete.add_argument("--confirm", action="store_true")

    # push
    p_push = sub.add_parser("push", help="Push local changes")
    p_push.add_argument("path")
    p_push.add_argument("-m", "--message", default="Automated commit")

    # details
    p_det = sub.add_parser("details", help="Get repository details")
    p_det.add_argument("full_name")

    args = parser.parse_args(argv)
    agent = GitHubManagerAgent()

    if args.command == "list":
        print(json.dumps(agent.list_repositories(args.user_or_org), indent=2))
    elif args.command == "clone":
        agent.clone_repository(args.repo_url, args.destination)
    elif args.command == "create":
        repo = agent.create_repository(args.name, private=not args.public, org=args.org)
        print(json.dumps(repo, indent=2))
    elif args.command == "delete":
        agent.delete_repository(args.full_name, confirm=args.confirm)
        print("Repository deleted.")
    elif args.command == "push":
        agent.push_changes(args.path, args.message)
    elif args.command == "details":
        print(json.dumps(agent.get_repo_details(args.full_name), indent=2))


if __name__ == "__main__":  # pragma: no cover
    _main()

