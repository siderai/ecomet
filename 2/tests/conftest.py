from datetime import datetime, timezone
from typing import Any

import pytest


@pytest.fixture
def mock_github_token() -> str:
    return "ghp_mock_token_for_testing"


@pytest.fixture
def mock_repositories_data() -> list[dict[str, Any]]:
    """Mock data for GitHub repositories search response based on API documentation."""
    return [
        {
            "id": 21289110,
            "node_id": "MDEwOlJlcG9zaXRvcnkyMTI4OTExMA==",
            "name": "awesome-python",
            "full_name": "vinta/awesome-python",
            "owner": {
                "login": "vinta",
                "id": 652070,
                "node_id": "MDQ6VXNlcjY1MjA3MA==",
                "avatar_url": "https://avatars.githubusercontent.com/u/652070",
                "type": "User",
                "site_admin": False,
            },
            "private": False,
            "html_url": "https://github.com/vinta/awesome-python",
            "description": "A curated list of awesome Python frameworks, libraries, software and resources",
            "fork": False,
            "created_at": "2014-06-27T21:00:06Z",
            "updated_at": "2024-11-01T10:30:00Z",
            "pushed_at": "2024-11-01T09:15:00Z",
            "homepage": "https://awesome-python.com",
            "size": 8420,
            "stargazers_count": 5000,
            "watchers_count": 3000,
            "language": "Python",
            "forks_count": 1000,
            "open_issues_count": 150,
            "default_branch": "master",
        },
        {
            "id": 28457823,
            "node_id": "MDEwOlJlcG9zaXRvcnkyODQ1NzgyMw==",
            "name": "free-programming-books",
            "full_name": "EbookFoundation/free-programming-books",
            "owner": {
                "login": "EbookFoundation",
                "id": 14127308,
                "node_id": "MDEyOk9yZ2FuaXphdGlvbjE0MTI3MzA4",
                "avatar_url": "https://avatars.githubusercontent.com/u/14127308",
                "type": "Organization",
                "site_admin": False,
            },
            "private": False,
            "html_url": "https://github.com/EbookFoundation/free-programming-books",
            "description": "Freely available programming books",
            "fork": False,
            "created_at": "2014-12-28T20:39:24Z",
            "updated_at": "2024-11-01T11:00:00Z",
            "pushed_at": "2024-11-01T10:45:00Z",
            "homepage": "",
            "size": 12560,
            "stargazers_count": 4000,
            "watchers_count": 2500,
            "language": "Markdown",
            "forks_count": 800,
            "open_issues_count": 45,
            "default_branch": "main",
        },
        {
            "id": 54346799,
            "node_id": "MDEwOlJlcG9zaXRvcnk1NDM0Njc5OQ==",
            "name": "public-apis",
            "full_name": "public-apis/public-apis",
            "owner": {
                "login": "public-apis",
                "id": 51121562,
                "node_id": "MDEyOk9yZ2FuaXphdGlvbjUxMTIxNTYy",
                "avatar_url": "https://avatars.githubusercontent.com/u/51121562",
                "type": "Organization",
                "site_admin": False,
            },
            "private": False,
            "html_url": "https://github.com/public-apis/public-apis",
            "description": "A collective list of free APIs",
            "fork": False,
            "created_at": "2016-03-20T23:49:42Z",
            "updated_at": "2024-11-01T09:30:00Z",
            "pushed_at": "2024-11-01T08:20:00Z",
            "homepage": "http://public-apis.org",
            "size": 3240,
            "stargazers_count": 3000,
            "watchers_count": 2000,
            "language": "Python",
            "forks_count": 600,
            "open_issues_count": 78,
            "default_branch": "master",
        },
        {
            "id": 123456789,
            "node_id": "MDEwOlJlcG9zaXRvcnkxMjM0NTY3ODk=",
            "name": "the-book-of-secret-knowledge",
            "full_name": "trimstray/the-book-of-secret-knowledge",
            "owner": {
                "login": "trimstray",
                "id": 18256763,
                "node_id": "MDQ6VXNlcjE4MjU2NzYz",
                "avatar_url": "https://avatars.githubusercontent.com/u/18256763",
                "type": "User",
                "site_admin": False,
            },
            "private": False,
            "html_url": "https://github.com/trimstray/the-book-of-secret-knowledge",
            "description": "A collection of inspiring lists, manuals, cheatsheets, blogs, hacks, one-liners, cli/web tools and more",
            "fork": False,
            "created_at": "2018-06-23T22:00:00Z",
            "updated_at": "2024-11-01T08:00:00Z",
            "pushed_at": "2024-11-01T07:30:00Z",
            "homepage": "",
            "size": 5600,
            "stargazers_count": 2000,
            "watchers_count": 1500,
            "language": "Shell",
            "forks_count": 400,
            "open_issues_count": 12,
            "default_branch": "master",
        },
        {
            "id": 85077558,
            "node_id": "MDEwOlJlcG9zaXRvcnk4NTA3NzU1OA==",
            "name": "developer-roadmap",
            "full_name": "kamranahmedse/developer-roadmap",
            "owner": {
                "login": "kamranahmedse",
                "id": 4921183,
                "node_id": "MDQ6VXNlcjQ5MjExODM=",
                "avatar_url": "https://avatars.githubusercontent.com/u/4921183",
                "type": "User",
                "site_admin": False,
            },
            "private": False,
            "html_url": "https://github.com/kamranahmedse/developer-roadmap",
            "description": "Interactive roadmaps, guides and other educational content to help developers grow in their careers",
            "fork": False,
            "created_at": "2017-03-15T03:24:00Z",
            "updated_at": "2024-11-01T12:00:00Z",
            "pushed_at": "2024-11-01T11:45:00Z",
            "homepage": "https://roadmap.sh",
            "size": 9870,
            "stargazers_count": 1000,
            "watchers_count": 1000,
            "language": "TypeScript",
            "forks_count": 200,
            "open_issues_count": 89,
            "default_branch": "master",
        },
    ]


@pytest.fixture
def mock_commits_data() -> dict[str, list[dict[str, Any]]]:
    """Mock data for GitHub commits by repository based on API documentation."""
    today = datetime.now(timezone.utc).isoformat()

    return {
        "vinta/awesome-python": [
            {
                "sha": "6dcb09b5b57875f334f61aebed695e2e4193db5e",
                "node_id": "MDY6Q29tbWl0NmRjYjA5YjViNTc4NzVmMzM0ZjYxYWViZWQ2OTVlMmU0MTkzZGI1ZQ==",
                "url": "https://api.github.com/repos/vinta/awesome-python/commits/6dcb09b5b57875f334f61aebed695e2e4193db5e",
                "html_url": "https://github.com/vinta/awesome-python/commit/6dcb09b5b57875f334f61aebed695e2e4193db5e",
                "comments_url": "https://api.github.com/repos/vinta/awesome-python/commits/6dcb09b5b57875f334f61aebed695e2e4193db5e/comments",
                "commit": {
                    "url": "https://api.github.com/repos/vinta/awesome-python/git/commits/6dcb09b5b57875f334f61aebed695e2e4193db5e",
                    "author": {
                        "name": "Alice Developer",
                        "email": "alice@example.com",
                        "date": today,
                    },
                    "committer": {
                        "name": "Alice Developer",
                        "email": "alice@example.com",
                        "date": today,
                    },
                    "message": "Add new Python libraries",
                    "comment_count": 0,
                },
            },
            {
                "sha": "7ecb19c6c68976e445f72fbbe806a29f5284ec6f",
                "node_id": "MDY6Q29tbWl0N2VjYjE5YzZjNjg5NzZlNDQ1ZjcyZmJiZTgwNmEyOWY1Mjg0ZWM2Zg==",
                "url": "https://api.github.com/repos/vinta/awesome-python/commits/7ecb19c6c68976e445f72fbbe806a29f5284ec6f",
                "html_url": "https://github.com/vinta/awesome-python/commit/7ecb19c6c68976e445f72fbbe806a29f5284ec6f",
                "comments_url": "https://api.github.com/repos/vinta/awesome-python/commits/7ecb19c6c68976e445f72fbbe806a29f5284ec6f/comments",
                "commit": {
                    "url": "https://api.github.com/repos/vinta/awesome-python/git/commits/7ecb19c6c68976e445f72fbbe806a29f5284ec6f",
                    "author": {
                        "name": "Bob Contributor",
                        "email": "bob@example.com",
                        "date": today,
                    },
                    "committer": {
                        "name": "Bob Contributor",
                        "email": "bob@example.com",
                        "date": today,
                    },
                    "message": "Update documentation",
                    "comment_count": 2,
                },
            },
            {
                "sha": "8fdc2ae7d79087ae6f83ba5c0ceaf6f9b3e8fa7a",
                "node_id": "MDY6Q29tbWl0OGZkYzJhZTdkNzkwODdhZTZmODNiYTVjMGNlYWY2ZjliM2U4ZmE3YQ==",
                "url": "https://api.github.com/repos/vinta/awesome-python/commits/8fdc2ae7d79087ae6f83ba5c0ceaf6f9b3e8fa7a",
                "html_url": "https://github.com/vinta/awesome-python/commit/8fdc2ae7d79087ae6f83ba5c0ceaf6f9b3e8fa7a",
                "comments_url": "https://api.github.com/repos/vinta/awesome-python/commits/8fdc2ae7d79087ae6f83ba5c0ceaf6f9b3e8fa7a/comments",
                "commit": {
                    "url": "https://api.github.com/repos/vinta/awesome-python/git/commits/8fdc2ae7d79087ae6f83ba5c0ceaf6f9b3e8fa7a",
                    "author": {
                        "name": "Alice Developer",
                        "email": "alice@example.com",
                        "date": today,
                    },
                    "committer": {
                        "name": "Alice Developer",
                        "email": "alice@example.com",
                        "date": today,
                    },
                    "message": "Fix typos in README",
                    "comment_count": 0,
                },
            },
        ],
        "EbookFoundation/free-programming-books": [
            {
                "sha": "9aeb3cf8e98197bf6a2f0e5c3d4b5a6e7f8c9d0a",
                "node_id": "MDY6Q29tbWl0OWFlYjNjZjhlOTgxOTdiZjZhMmYwZTVjM2Q0YjVhNmU3ZjhjOWQwYQ==",
                "url": "https://api.github.com/repos/EbookFoundation/free-programming-books/commits/9aeb3cf8e98197bf6a2f0e5c3d4b5a6e7f8c9d0a",
                "html_url": "https://github.com/EbookFoundation/free-programming-books/commit/9aeb3cf8e98197bf6a2f0e5c3d4b5a6e7f8c9d0a",
                "comments_url": "https://api.github.com/repos/EbookFoundation/free-programming-books/commits/9aeb3cf8e98197bf6a2f0e5c3d4b5a6e7f8c9d0a/comments",
                "commit": {
                    "url": "https://api.github.com/repos/EbookFoundation/free-programming-books/git/commits/9aeb3cf8e98197bf6a2f0e5c3d4b5a6e7f8c9d0a",
                    "author": {
                        "name": "Charlie Author",
                        "email": "charlie@example.com",
                        "date": today,
                    },
                    "committer": {
                        "name": "Charlie Author",
                        "email": "charlie@example.com",
                        "date": today,
                    },
                    "message": "Add new free books",
                    "comment_count": 1,
                },
            },
        ],
        "public-apis/public-apis": [
            {
                "sha": "1bfc4da9f10298ce7b3f1e6a8d9c0b1e2f3a4b5c",
                "node_id": "MDY6Q29tbWl0MWJmYzRkYTlmMTAyOThjZTdiM2YxZTZhOGQ5YzBiMWUyZjNhNGI1Yw==",
                "url": "https://api.github.com/repos/public-apis/public-apis/commits/1bfc4da9f10298ce7b3f1e6a8d9c0b1e2f3a4b5c",
                "html_url": "https://github.com/public-apis/public-apis/commit/1bfc4da9f10298ce7b3f1e6a8d9c0b1e2f3a4b5c",
                "comments_url": "https://api.github.com/repos/public-apis/public-apis/commits/1bfc4da9f10298ce7b3f1e6a8d9c0b1e2f3a4b5c/comments",
                "commit": {
                    "url": "https://api.github.com/repos/public-apis/public-apis/git/commits/1bfc4da9f10298ce7b3f1e6a8d9c0b1e2f3a4b5c",
                    "author": {
                        "name": "Dave Maintainer",
                        "email": "dave@example.com",
                        "date": today,
                    },
                    "committer": {
                        "name": "Dave Maintainer",
                        "email": "dave@example.com",
                        "date": today,
                    },
                    "message": "Add weather API",
                    "comment_count": 0,
                },
            },
            {
                "sha": "2cbd5eb0e21309df8c4g2f7b9e0d1c2f4b5d6e7f",
                "node_id": "MDY6Q29tbWl0MmNiZDVlYjBlMjEzMDlkZjhjNGcyZjdiOWUwZDFjMmY0YjVkNmU3Zg==",
                "url": "https://api.github.com/repos/public-apis/public-apis/commits/2cbd5eb0e21309df8c4g2f7b9e0d1c2f4b5d6e7f",
                "html_url": "https://github.com/public-apis/public-apis/commit/2cbd5eb0e21309df8c4g2f7b9e0d1c2f4b5d6e7f",
                "comments_url": "https://api.github.com/repos/public-apis/public-apis/commits/2cbd5eb0e21309df8c4g2f7b9e0d1c2f4b5d6e7f/comments",
                "commit": {
                    "url": "https://api.github.com/repos/public-apis/public-apis/git/commits/2cbd5eb0e21309df8c4g2f7b9e0d1c2f4b5d6e7f",
                    "author": {
                        "name": "Dave Maintainer",
                        "email": "dave@example.com",
                        "date": today,
                    },
                    "committer": {
                        "name": "Dave Maintainer",
                        "email": "dave@example.com",
                        "date": today,
                    },
                    "message": "Update API documentation",
                    "comment_count": 0,
                },
            },
        ],
        "trimstray/the-book-of-secret-knowledge": [],
        "kamranahmedse/developer-roadmap": [
            {
                "sha": "3dce6fc1f32410eg9d5h3g8c0f1e2d3g5c6e8f9a",
                "node_id": "MDY6Q29tbWl0M2RjZTZmYzFmMzI0MTBlZzlkNWgzZzhjMGYxZTJkM2c1YzZlOGY5YQ==",
                "url": "https://api.github.com/repos/kamranahmedse/developer-roadmap/commits/3dce6fc1f32410eg9d5h3g8c0f1e2d3g5c6e8f9a",
                "html_url": "https://github.com/kamranahmedse/developer-roadmap/commit/3dce6fc1f32410eg9d5h3g8c0f1e2d3g5c6e8f9a",
                "comments_url": "https://api.github.com/repos/kamranahmedse/developer-roadmap/commits/3dce6fc1f32410eg9d5h3g8c0f1e2d3g5c6e8f9a/comments",
                "commit": {
                    "url": "https://api.github.com/repos/kamranahmedse/developer-roadmap/git/commits/3dce6fc1f32410eg9d5h3g8c0f1e2d3g5c6e8f9a",
                    "author": {
                        "name": "Eve Reviewer",
                        "email": "eve@example.com",
                        "date": today,
                    },
                    "committer": {
                        "name": "Eve Reviewer",
                        "email": "eve@example.com",
                        "date": today,
                    },
                    "message": "Update frontend roadmap",
                    "comment_count": 3,
                },
            },
        ],
    }
