import dotenv
import asyncio

from scrapers.blupax_scraper import main as run_blupax_scraper
from scrapers.parmed_scraper import main as run_parmed_scraper

dotenv.load_dotenv()


async def main():
    """Runs both scraping processes."""
    print("Running Blupax scraper...")
    run_blupax_scraper()
    print("\nRunning Parmed scraper...")
    await run_parmed_scraper()
    print("\nAll scraping processes finished.")


if __name__ == "__main__":
    asyncio.run(main())
