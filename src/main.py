import dotenv
import asyncio

from .scrapers import BlupaxScraper, ParmedScraper

dotenv.load_dotenv()


async def main():
    """Runs both scraping processes concurrently."""
    scrapers = [
        BlupaxScraper(),
        ParmedScraper()
    ]

    tasks = [scraper.run() for scraper in scrapers]
    await asyncio.gather(*tasks)

    print("\nAll scraping processes finished.")


if __name__ == "__main__":
    asyncio.run(main())
