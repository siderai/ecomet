import logging
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

from aiochclient import ChClient

logger = logging.getLogger(__name__)


class ClickHouseStorage:
    def __init__(self, client: ChClient, batch_size: int = 100):
        self._client = client
        self._batch_size = batch_size

    async def initialize_database(self, database: str) -> None:
        await self._client.execute(f"CREATE DATABASE IF NOT EXISTS {database}")

        sql_file = Path(__file__).parent / "tables.sql"
        sql_content = sql_file.read_text()

        statements = []
        current_statement = []

        for line in sql_content.split("\n"):
            line = line.strip()
            if not line or line.startswith("--"):
                continue

            current_statement.append(line)

            if line.endswith(";"):
                statement = " ".join(current_statement).strip().rstrip(";")
                if statement.upper().startswith("CREATE"):
                    statements.append(statement)
                current_statement = []

        for statement in statements:
            await self._client.execute(statement)

        logger.info(f"Database '{database}' initialized")

    async def insert_repositories_batch(self, repositories: list[Any]) -> None:
        current_timestamp = datetime.now(timezone.utc)
        current_date = date.today()

        await self._insert_repositories_metadata(repositories, current_timestamp)
        await self._insert_repositories_positions(repositories, current_date)
        await self._insert_authors_commits(repositories, current_date)

    async def _insert_repositories_metadata(
        self,
        repositories: list[Any],
        updated_timestamp: datetime,
    ) -> None:
        for i in range(0, len(repositories), self._batch_size):
            batch = repositories[i : i + self._batch_size]

            rows = [
                (
                    repo.name,
                    repo.owner,
                    repo.stars,
                    repo.watchers,
                    repo.forks,
                    repo.language if repo.language else "Unknown",
                    updated_timestamp.replace(tzinfo=None, microsecond=0),
                )
                for repo in batch
            ]

            await self._client.execute("INSERT INTO test.repositories VALUES", *rows)

    async def _insert_repositories_positions(
        self,
        repositories: list[Any],
        current_date: date,
    ) -> None:
        """Insert repository positions into test.repositories_positions table in batches."""
        for i in range(0, len(repositories), self._batch_size):
            batch = repositories[i : i + self._batch_size]

            rows = [
                (current_date, f"{repo.owner}/{repo.name}", repo.position)
                for repo in batch
            ]

            await self._client.execute("INSERT INTO test.repositories_positions VALUES", *rows)

    async def _insert_authors_commits(
        self,
        repositories: list[Any],
        current_date: date,
    ) -> None:
        all_commits = []
        for repo in repositories:
            repo_name = f"{repo.owner}/{repo.name}"
            for author_commit in repo.authors_commits_num_today:
                all_commits.append(
                    (current_date, repo_name, author_commit.author, author_commit.commits_num)
                )

        for i in range(0, len(all_commits), self._batch_size):
            batch = all_commits[i : i + self._batch_size]
            await self._client.execute("INSERT INTO test.repositories_authors_commits VALUES", *batch)
