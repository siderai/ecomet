import asyncio
import logging
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, Final
from urllib.parse import parse_qs, urlparse

from aiohttp import ClientSession
from aiolimiter import AsyncLimiter

from models import GitHubCommit, GitHubRepository

GITHUB_API_BASE_URL: Final[str] = "https://api.github.com"
MAX_REPOS_PER_REQUEST: Final[int] = 100


@dataclass
class RepositoryAuthorCommitsNum:
    author: str
    commits_num: int


@dataclass
class Repository:
    name: str
    owner: str
    position: int
    stars: int
    watchers: int
    forks: int
    language: str
    authors_commits_num_today: list[RepositoryAuthorCommitsNum]


class GithubReposScrapper:
    def __init__(
        self,
        access_token: str,
        max_concurrent_requests: int = 10,
        requests_per_second: int = 5,
    ):
        self._session = ClientSession(
            headers={
                "Accept": "application/vnd.github.v3+json",
                "Authorization": f"Bearer {access_token}",
            }
        )
        self._semaphore = asyncio.Semaphore(max_concurrent_requests)
        self._rate_limiter = AsyncLimiter(max_rate=requests_per_second, time_period=1.0)

    async def _make_request(self, endpoint: str, method: str = "GET", params: dict[str, Any] | None = None) -> tuple[Any, dict[str, str]]:
        async with self._semaphore:
            await self._rate_limiter.acquire()
            async with self._session.request(method, f"{GITHUB_API_BASE_URL}/{endpoint}", params=params) as response:
                response.raise_for_status()
                return await response.json(), dict(response.headers)

    def _parse_link_header(self, link_header: str) -> dict[str, str]:
        """
        Parse Link header to extract pagination URLs.
        Format: '<url>; rel="first", <url>; rel="next", <url>; rel="last"'
        Returns: {"first": url, "next": url, "last": url}
        """
        links = {}
        if not link_header:
            return links

        for link in link_header.split(","):
            link = link.strip()
            if not link:
                continue

            parts = link.split(";")
            if len(parts) < 2:
                continue

            url = parts[0].strip().strip("<>")
            for part in parts[1:]:
                if "rel=" in part:
                    rel = part.split("=")[1].strip().strip('"')
                    links[rel] = url
                    break

        return links

    def _extract_items(self, data: dict | list) -> list[dict[str, Any]]:
        """
        Extract items from API response.
        Handles both {"items": [...]} and [...] formats.
        """
        if isinstance(data, dict) and "items" in data:
            return data["items"]
        elif isinstance(data, list):
            return data
        return []

    async def _fetch_paginated(self, endpoint: str, params: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        """
        Fetch paginated results from GitHub API concurrently.
        First page is fetched to discover total pages, then remaining pages are fetched in parallel.
        """
        current_params = params or {}

        data, headers = await self._make_request(endpoint, params=current_params)
        all_items = self._extract_items(data)

        link_header = headers.get("Link", "")
        links = self._parse_link_header(link_header)

        last_url = links.get("last")
        if not last_url:
            return all_items

        parsed = urlparse(last_url)
        query_params = parse_qs(parsed.query)
        last_page = int(query_params.get("page", ["1"])[0])

        if last_page > 1:
            tasks = []
            for page_num in range(2, last_page + 1):
                page_params = {**current_params, "page": page_num}
                tasks.append(self._make_request(endpoint, params=page_params))

            results = await asyncio.gather(*tasks)

            for data, _ in results:
                all_items.extend(self._extract_items(data))

        return all_items

    async def _get_top_repositories(self, limit: int = 100) -> list[GitHubRepository]:
        """
        GitHub REST API: https://docs.github.com/en/rest/search/search?apiVersion=2022-11-28#search-repositories
        """
        per_page = min(limit, MAX_REPOS_PER_REQUEST)
        data, _ = await self._make_request(
            endpoint="search/repositories",
            params={"q": "stars:>1", "sort": "stars", "order": "desc", "per_page": per_page},
        )
        repos = data.get("items", [])
        return [GitHubRepository(**repo) for repo in repos]

    async def _get_repository_commits(self, owner: str, repo: str) -> list[GitHubCommit]:
        """
        GitHub REST API: https://docs.github.com/en/rest/commits/commits?apiVersion=2022-11-28#list-commits
        """
        since = (datetime.now(timezone.utc) - timedelta(days=1)).isoformat()
        all_commits = await self._fetch_paginated(  # number of commits may exceed github fetch limit (100)
            endpoint=f"repos/{owner}/{repo}/commits",
            params={"since": since, "per_page": 100},
        )
        return [GitHubCommit(**commit) for commit in all_commits]

    async def get_repositories(self, limit: int = 100) -> list[Repository]:
        top_repos = await self._get_top_repositories(limit)

        async def process_repository(repo_data: GitHubRepository, position: int) -> Repository:
            owner = repo_data.owner.login
            repo_name = repo_data.name

            try:
                commits = await self._get_repository_commits(owner, repo_name)
            except Exception as e:
                logging.error(f"Failed to fetch commits for {owner}/{repo_name}: {e}")
                commits = []

            author_commits: defaultdict[str, int] = defaultdict(int)
            for commit in commits:
                if commit.commit.author and commit.commit.author.name:
                    author_name = commit.commit.author.name
                    author_commits[author_name] += 1

            authors_commits_num_today = [
                RepositoryAuthorCommitsNum(author=author, commits_num=count)
                for author, count in author_commits.items()
            ]

            return Repository(
                name=repo_name,
                owner=owner,
                position=position,
                stars=repo_data.stargazers_count,
                watchers=repo_data.watchers_count,
                forks=repo_data.forks_count,
                language=repo_data.language or "Unknown",
                authors_commits_num_today=authors_commits_num_today,
            )

        tasks = [
            process_repository(repo, position + 1)
            for position, repo in enumerate(top_repos)
        ]
        repositories = await asyncio.gather(*tasks)
        return list(repositories)

    async def close(self):
        await self._session.close()
