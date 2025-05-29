import dotenv
dotenv.load_dotenv()

from blupax import main as run_blupax_scraper
from parmed import main as run_parmed_scraper


def main():
    """Runs both scraping processes."""
    print("Running Blupax scraper...")
    run_blupax_scraper()
    print("\nRunning Parmed scraper...")
    run_parmed_scraper()
    print("\nAll scraping processes finished.")


if __name__ == "__main__":
    main()
