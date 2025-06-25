import abc
import pandas as pd
from dateutil.utils import today


class BaseScraper(abc.ABC):
    """An abstract base class for scrapers."""

    def __init__(self, scraper_name: str):
        """
        Initializes the scraper with a name.

        Args:
            scraper_name: The name of the scraper, used for filenames.
        """
        self.scraper_name = scraper_name
        self.today_timestamp = today().strftime('%Y-%m-%d')
        self.csv_filename = f'{self.scraper_name}-{self.today_timestamp}.csv'
        self.filepath = f'./data/raw/{self.csv_filename}'

    @abc.abstractmethod
    async def get_data(self) -> list[dict]:
        """
        Fetches and returns data. Must be implemented by subclasses.
        This method should be asynchronous.
        """
        raise NotImplementedError

    def _save_to_csv(self, data: list[dict]):
        """Saves the provided data to a CSV file."""
        if not data:
            print(f"No data found for {self.scraper_name}.")
            return

        print(f"Found {len(data)} items for {self.scraper_name}.")
        df = pd.DataFrame(data)
        df.to_csv(self.filepath, index=False)
        print(f"Data for {self.scraper_name} saved to {self.csv_filename}")

    async def run(self):
        """Orchestrates the scraper's execution."""
        print(f"Running {self.scraper_name} scraper...")
        try:
            data = await self.get_data()
            self._save_to_csv(data)
        except Exception as e:
            print(f"An error occurred while running the {self.scraper_name} scraper: {e}")
        finally:
            print(f"{self.scraper_name} scraper finished.") 