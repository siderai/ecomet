import asyncio

from config import Settings
from main import GithubReposScrapper


async def main():
    settings = Settings()
    scrapper = GithubReposScrapper(
        access_token=settings.github_token,
        max_concurrent_requests=settings.max_concurrent_requests,
        requests_per_second=settings.requests_per_second,
    )

    try:
        repositories = await scrapper.get_repositories(limit=settings.top_repositories_limit)

        for repo in repositories:
            print(f"\n{repo.position}. {repo.owner}/{repo.name}")
            print(f"   Stars: {repo.stars}, Language: {repo.language}")
            print(f"   Commits today: {len(repo.authors_commits_num_today)}")
            for author_commit in repo.authors_commits_num_today[:5]:
                print(f"     - {author_commit.author}: {author_commit.commits_num} commits")
    finally:
        await scrapper.close()


if __name__ == "__main__":
    asyncio.run(main())
