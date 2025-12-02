import asyncio
import re
from datetime import datetime, timedelta, timezone
from typing import Any

import pytest
from aioresponses import aioresponses

from main import GithubReposScrapper, Repository, RepositoryAuthorCommitsNum


class TestGithubReposScrapper:
    @pytest.mark.asyncio
    async def test_scrapper_initialization(self, mock_github_token: str) -> None:
        """Test that scrapper initializes correctly."""
        # Arrange
        max_concurrent = 5
        rps = 3

        # Act
        scrapper = GithubReposScrapper(
            access_token=mock_github_token,
            max_concurrent_requests=max_concurrent,
            requests_per_second=rps,
        )

        # Assert
        assert scrapper._session is not None
        assert scrapper._semaphore._value == max_concurrent

        await scrapper.close()

    @pytest.mark.asyncio
    async def test_get_repositories_structure(
        self,
        mock_github_token: str,
        mock_repositories_data: list[dict[str, Any]],
        mock_commits_data: dict[str, list[dict[str, Any]]],
    ) -> None:
        """Test that get_repositories returns valid Repository objects."""
        # Arrange
        limit = 3

        with aioresponses() as m:
            m.get(
                re.compile(r"https://api\.github\.com/search/repositories\?.*"),
                payload={"items": mock_repositories_data[:limit]},
                status=200,
            )

            for repo in mock_repositories_data[:limit]:
                owner = repo["owner"]["login"]
                name = repo["name"]
                repo_key = f"{owner}/{name}"
                m.get(
                    re.compile(rf"https://api\.github\.com/repos/{owner}/{name}/commits\?since=.+&per_page=100"),
                    payload=mock_commits_data.get(repo_key, []),
                    status=200,
                )

            scrapper = GithubReposScrapper(
                access_token=mock_github_token,
                max_concurrent_requests=5,
                requests_per_second=2,
            )

            try:
                # Act
                repositories = await scrapper.get_repositories(limit=limit)

                # Assert
                assert isinstance(repositories, list)
                assert len(repositories) == limit

                for repo in repositories:
                    assert isinstance(repo, Repository)
                    assert isinstance(repo.name, str)
                    assert isinstance(repo.owner, str)
                    assert isinstance(repo.position, int)
                    assert isinstance(repo.stars, int)
                    assert isinstance(repo.watchers, int)
                    assert isinstance(repo.forks, int)
                    assert isinstance(repo.language, str)
                    assert isinstance(repo.authors_commits_num_today, list)

                    for author_commit in repo.authors_commits_num_today:
                        assert isinstance(author_commit, RepositoryAuthorCommitsNum)
                        assert isinstance(author_commit.author, str)
                        assert isinstance(author_commit.commits_num, int)
                        assert author_commit.commits_num > 0
            finally:
                await scrapper.close()

    @pytest.mark.asyncio
    async def test_get_repositories_positions(
        self,
        mock_github_token: str,
        mock_repositories_data: list[dict[str, Any]],
        mock_commits_data: dict[str, list[dict[str, Any]]],
    ) -> None:
        """Test that repositories have correct positions."""
        # Arrange
        limit = 5
        expected_positions = list(range(1, limit + 1))

        with aioresponses() as m:
            m.get(
                re.compile(r"https://api\.github\.com/search/repositories\?.*"),
                payload={"items": mock_repositories_data[:limit]},
                status=200,
            )

            for repo in mock_repositories_data[:limit]:
                owner = repo["owner"]["login"]
                name = repo["name"]
                repo_key = f"{owner}/{name}"
                m.get(
                    re.compile(rf"https://api\.github\.com/repos/{owner}/{name}/commits\?since=.+&per_page=100"),
                    payload=mock_commits_data.get(repo_key, []),
                    status=200,
                )

            scrapper = GithubReposScrapper(
                access_token=mock_github_token,
                max_concurrent_requests=5,
                requests_per_second=2,
            )

            try:
                # Act
                repositories = await scrapper.get_repositories(limit=limit)

                # Assert
                positions = [repo.position for repo in repositories]
                assert positions == expected_positions
            finally:
                await scrapper.close()

    @pytest.mark.asyncio
    async def test_concurrent_requests_limit(
        self,
        mock_github_token: str,
        mock_repositories_data: list[dict[str, Any]],
        mock_commits_data: dict[str, list[dict[str, Any]]],
    ) -> None:
        """Test that concurrent requests are limited."""
        # Arrange
        max_concurrent = 3
        limit = 5

        with aioresponses() as m:
            m.get(
                re.compile(r"https://api\.github\.com/search/repositories\?.*"),
                payload={"items": mock_repositories_data[:limit]},
                status=200,
            )

            for repo in mock_repositories_data[:limit]:
                owner = repo["owner"]["login"]
                name = repo["name"]
                repo_key = f"{owner}/{name}"
                m.get(
                    re.compile(rf"https://api\.github\.com/repos/{owner}/{name}/commits\?since=.+&per_page=100"),
                    payload=mock_commits_data.get(repo_key, []),
                    status=200,
                )

            scrapper = GithubReposScrapper(
                access_token=mock_github_token,
                max_concurrent_requests=max_concurrent,
                requests_per_second=10,
            )

            try:
                # Act
                repositories = await scrapper.get_repositories(limit=limit)

                # Assert
                assert scrapper._semaphore._value == max_concurrent
                assert len(repositories) == limit
            finally:
                await scrapper.close()

    @pytest.mark.asyncio
    async def test_rate_limiting_applied(
        self,
        mock_github_token: str,
        mock_repositories_data: list[dict[str, Any]],
        mock_commits_data: dict[str, list[dict[str, Any]]],
    ) -> None:
        """Test that rate limiting is applied during execution."""
        # Arrange
        limit = 3
        rps = 2

        with aioresponses() as m:
            m.get(
                re.compile(r"https://api\.github\.com/search/repositories\?.*"),
                payload={"items": mock_repositories_data[:limit]},
                status=200,
            )

            for repo in mock_repositories_data[:limit]:
                owner = repo["owner"]["login"]
                name = repo["name"]
                repo_key = f"{owner}/{name}"
                m.get(
                    re.compile(rf"https://api\.github\.com/repos/{owner}/{name}/commits\?since=.+&per_page=100"),
                    payload=mock_commits_data.get(repo_key, []),
                    status=200,
                )

            scrapper = GithubReposScrapper(
                access_token=mock_github_token,
                max_concurrent_requests=10,
                requests_per_second=rps,
            )

            try:
                # Act
                start_time = asyncio.get_event_loop().time()
                repositories = await scrapper.get_repositories(limit=limit)
                elapsed = asyncio.get_event_loop().time() - start_time

                # Assert
                assert len(repositories) == limit
                assert elapsed > 0
            finally:
                await scrapper.close()

    @pytest.mark.asyncio
    async def test_repositories_sorted_by_stars(
        self,
        mock_github_token: str,
        mock_repositories_data: list[dict[str, Any]],
        mock_commits_data: dict[str, list[dict[str, Any]]],
    ) -> None:
        """Test that repositories are sorted by stars (descending)."""
        # Arrange
        limit = 5

        with aioresponses() as m:
            m.get(
                re.compile(r"https://api\.github\.com/search/repositories\?.*"),
                payload={"items": mock_repositories_data[:limit]},
                status=200,
            )

            for repo in mock_repositories_data[:limit]:
                owner = repo["owner"]["login"]
                name = repo["name"]
                repo_key = f"{owner}/{name}"
                m.get(
                    re.compile(rf"https://api\.github\.com/repos/{owner}/{name}/commits\?since=.+&per_page=100"),
                    payload=mock_commits_data.get(repo_key, []),
                    status=200,
                )

            scrapper = GithubReposScrapper(
                access_token=mock_github_token,
                max_concurrent_requests=5,
                requests_per_second=2,
            )

            try:
                # Act
                repositories = await scrapper.get_repositories(limit=limit)

                # Assert
                stars = [repo.stars for repo in repositories]
                assert stars == sorted(stars, reverse=True)
            finally:
                await scrapper.close()


class TestPagination:
    @pytest.mark.asyncio
    async def test_fetch_paginated_concurrent_requests(
        self,
        mock_github_token: str,
    ) -> None:
        """Test that multiple pages are fetched concurrently."""
        # Arrange
        owner = "testowner"
        repo = "testrepo"
        today = datetime.now(timezone.utc).isoformat()

        # Create 3 pages of commits
        page1_commits = [
            {
                "sha": f"sha{i}",
                "commit": {
                    "author": {
                        "name": f"Author {i}",
                        "email": f"author{i}@example.com",
                        "date": today,
                    }
                },
            }
            for i in range(100)
        ]

        page2_commits = [
            {
                "sha": f"sha{i}",
                "commit": {
                    "author": {
                        "name": f"Author {i}",
                        "email": f"author{i}@example.com",
                        "date": today,
                    }
                },
            }
            for i in range(100, 200)
        ]

        page3_commits = [
            {
                "sha": f"sha{i}",
                "commit": {
                    "author": {
                        "name": f"Author {i}",
                        "email": f"author{i}@example.com",
                        "date": today,
                    }
                },
            }
            for i in range(200, 250)
        ]

        with aioresponses() as m:
            # Mock page 1 with Link header pointing to page 3 as last
            m.get(
                re.compile(rf"https://api\.github\.com/repos/{owner}/{repo}/commits\?.*"),
                payload=page1_commits,
                status=200,
                headers={
                    "Link": f'<https://api.github.com/repos/{owner}/{repo}/commits?page=2>; rel="next", '
                    f'<https://api.github.com/repos/{owner}/{repo}/commits?page=3>; rel="last"'
                },
            )

            # Mock page 2
            m.get(
                re.compile(rf"https://api\.github\.com/repos/{owner}/{repo}/commits\?.*page=2.*"),
                payload=page2_commits,
                status=200,
                headers={
                    "Link": f'<https://api.github.com/repos/{owner}/{repo}/commits?page=3>; rel="next", '
                    f'<https://api.github.com/repos/{owner}/{repo}/commits?page=1>; rel="prev"'
                },
            )

            # Mock page 3 (final page)
            m.get(
                re.compile(rf"https://api\.github\.com/repos/{owner}/{repo}/commits\?.*page=3.*"),
                payload=page3_commits,
                status=200,
                headers={
                    "Link": f'<https://api.github.com/repos/{owner}/{repo}/commits?page=2>; rel="prev"'
                },
            )

            scrapper = GithubReposScrapper(
                access_token=mock_github_token,
                max_concurrent_requests=10,
                requests_per_second=10,
            )

            try:
                # Act
                commits = await scrapper._get_repository_commits(owner, repo)

                # Assert
                assert len(commits) == 250
                # Verify order is maintained (page 1, then page 2, then page 3)
                assert commits[0].sha == "sha0"
                assert commits[99].sha == "sha99"
                assert commits[100].sha == "sha100"
                assert commits[199].sha == "sha199"
                assert commits[200].sha == "sha200"
                assert commits[249].sha == "sha249"
            finally:
                await scrapper.close()

    @pytest.mark.asyncio
    async def test_fetch_paginated_single_page(
        self,
        mock_github_token: str,
    ) -> None:
        """Test that single page responses work correctly without pagination."""
        # Arrange
        owner = "testowner"
        repo = "testrepo"
        today = datetime.now(timezone.utc).isoformat()

        commits = [
            {
                "sha": f"sha{i}",
                "commit": {
                    "author": {
                        "name": f"Author {i}",
                        "email": f"author{i}@example.com",
                        "date": today,
                    }
                },
            }
            for i in range(10)
        ]

        with aioresponses() as m:
            # Mock single page response (no Link header)
            m.get(
                re.compile(rf"https://api\.github\.com/repos/{owner}/{repo}/commits\?.*"),
                payload=commits,
                status=200,
                headers={},
            )

            scrapper = GithubReposScrapper(
                access_token=mock_github_token,
                max_concurrent_requests=10,
                requests_per_second=10,
            )

            try:
                # Act
                result = await scrapper._get_repository_commits(owner, repo)

                # Assert
                assert len(result) == 10
                assert result[0].sha == "sha0"
                assert result[9].sha == "sha9"
            finally:
                await scrapper.close()

    @pytest.mark.asyncio
    async def test_fetch_paginated_empty_link_header(
        self,
        mock_github_token: str,
    ) -> None:
        """Test that empty Link header is handled correctly."""
        # Arrange
        owner = "testowner"
        repo = "testrepo"
        today = datetime.now(timezone.utc).isoformat()

        commits = [
            {
                "sha": f"sha{i}",
                "commit": {
                    "author": {
                        "name": f"Author {i}",
                        "email": f"author{i}@example.com",
                        "date": today,
                    }
                },
            }
            for i in range(5)
        ]

        with aioresponses() as m:
            # Mock with empty Link header
            m.get(
                re.compile(rf"https://api\.github\.com/repos/{owner}/{repo}/commits\?.*"),
                payload=commits,
                status=200,
                headers={"Link": ""},
            )

            scrapper = GithubReposScrapper(
                access_token=mock_github_token,
                max_concurrent_requests=10,
                requests_per_second=10,
            )

            try:
                # Act
                result = await scrapper._get_repository_commits(owner, repo)

                # Assert
                assert len(result) == 5
            finally:
                await scrapper.close()

    @pytest.mark.asyncio
    async def test_parse_link_header(self, mock_github_token: str) -> None:
        """Test Link header parsing logic."""
        # Arrange
        scrapper = GithubReposScrapper(
            access_token=mock_github_token,
            max_concurrent_requests=10,
            requests_per_second=10,
        )

        try:
            # Act & Assert - Test full Link header
            link_header = (
                '<https://api.github.com/repos/owner/repo/commits?page=2>; rel="next", '
                '<https://api.github.com/repos/owner/repo/commits?page=5>; rel="last", '
                '<https://api.github.com/repos/owner/repo/commits?page=1>; rel="first"'
            )
            result = scrapper._parse_link_header(link_header)
            assert result["next"] == "https://api.github.com/repos/owner/repo/commits?page=2"
            assert result["last"] == "https://api.github.com/repos/owner/repo/commits?page=5"
            assert result["first"] == "https://api.github.com/repos/owner/repo/commits?page=1"

            # Test empty header
            result = scrapper._parse_link_header("")
            assert result == {}

            # Test malformed header
            result = scrapper._parse_link_header("invalid")
            assert result == {}
        finally:
            await scrapper.close()

    @pytest.mark.asyncio
    async def test_extract_items(self, mock_github_token: str) -> None:
        """Test item extraction from different response formats."""
        # Arrange
        scrapper = GithubReposScrapper(
            access_token=mock_github_token,
            max_concurrent_requests=10,
            requests_per_second=10,
        )

        try:
            # Act & Assert - Test dict with items
            result = scrapper._extract_items({"items": [1, 2, 3], "total": 3})
            assert result == [1, 2, 3]

            # Test list
            result = scrapper._extract_items([4, 5, 6])
            assert result == [4, 5, 6]

            # Test empty dict
            result = scrapper._extract_items({})
            assert result == []

            # Test dict without items
            result = scrapper._extract_items({"data": [7, 8, 9]})
            assert result == []
        finally:
            await scrapper.close()
