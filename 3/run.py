import asyncio
import logging

from aiohttp import ClientSession
from aiochclient import ChClient

from config import Settings
from scraper import GithubReposScrapper
from storage import ClickHouseStorage

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


async def main():
    ch_session = None
    scrapper = None

    try:
        settings = Settings()

        scrapper = GithubReposScrapper(
            access_token=settings.github_token,
            max_concurrent_requests=settings.max_concurrent_requests,
            requests_per_second=settings.requests_per_second,
        )

        ch_session = ClientSession()
        client = ChClient(
            ch_session,
            url=settings.clickhouse_url,
            user=settings.clickhouse_user,
            password=settings.clickhouse_password,
            database=settings.clickhouse_db,
            compress_response=True,
        )

        storage = ClickHouseStorage(client, batch_size=settings.batch_size)
        await storage.initialize_database(settings.clickhouse_db)

        logger.info(f"Fetching top {settings.top_repositories_limit} repositories...")
        repositories = await scrapper.get_repositories(limit=settings.top_repositories_limit)
        logger.info(f"Fetched {len(repositories)} repositories")

        logger.info("Inserting data into ClickHouse...")
        await storage.insert_repositories_batch(repositories)
        logger.info("ETL pipeline completed successfully")

    except Exception as e:
        logger.error(f"ETL pipeline failed: {e}", exc_info=True)
        raise
    finally:
        if scrapper:
            await scrapper.close()
        if ch_session:
            await ch_session.close()


if __name__ == "__main__":
    asyncio.run(main())
