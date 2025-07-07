import os
import abc
import json
import psycopg2
from psycopg2.extras import execute_values
from dateutil.utils import today
from datetime import datetime, timezone


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

    @abc.abstractmethod
    async def get_data(self) -> list[dict]:
        """
        Fetches and returns data. Must be implemented by subclasses.
        This method should be asynchronous.
        """
        raise NotImplementedError

    def _save_to_postgres(self, data: list[dict]):
        """Saves the provided data to the Postgres database."""
        if not data:
            print(f"No data found for {self.scraper_name}.")
            return

        print(f"Found {len(data)} items for {self.scraper_name}.")

        # Postgres connection string from environment
        pg_conn_str = os.environ.get("POSTGRES_CONNECTION_STRING")
        if not pg_conn_str:
            print("POSTGRES_CONNECTION_STRING is not set in environment variables.")
            return

        # Table and columns per scraper
        if self.scraper_name == "parmed":
            table = '"wholesaler_tracking".parmed'
            columns = [
                "cin", "itemId", "sku", "description", "ndc", "manufacturer", "strength", "packQuantity", "color",
                "unitOfSale", "form", "specialHandling", "labelSize", "brandName", "caseQty", "isCSOS", "gcn",
                "temperature", "isBlocked", "hin", "price", "allocatedQuantity", "gcnCount", "isLowestPriceFlag",
                "onOrder", "isWatchListItem", "isFavListItem", "unavailabilityReason", "ndc2", "isSubscriable",
                "isSubscribed", "isNegotiable", "isNegotiated", "isNegotiatePending", "rtrnable_flg", "remsFlag",
                "gtin", "shape", "he"
            ]
        elif self.scraper_name == "blupax":
            table = '"wholesaler_tracking".blupax'
            columns = [
                "id", "wac", "awp", "unit_price", "price", "website_url", "ndc_formatted", "item_number",
                "display_item_number", "description", "product_size", "manufacturer_name", "brand", "strength",
                "is_available", "short_dated", "manufacturer_short_name", "expiration_date", "extension_date",
                "quantity", "eta", "is_eta_delayed", "active", "is_short_dated", "cloudflare_image_url",
                "branding_type", "generic_name", "can_add_to_cart", "create_date", "display_name", "lot_number",
                "dosage_form", "item_group_filter", "availability_status", "show_short_dated_label",
                "display_dea_class", "hide_dea_icon", "restricted_by_dea", "last_ordered_date", "is_wishlisted",
                "is_gpi_restriction"
            ]
        else:
            print(f"Unknown scraper name: {self.scraper_name}")
            return

        # Prepare rows for insertion
        rows = []
        for item in data:
            row = [item.get(col) for col in columns]
            rows.append(row)

        insert_columns = ", ".join(columns)
        placeholders = ", ".join(["%s"] * len(columns))
        sql = f"INSERT INTO {table} ({insert_columns}, scraped_at) VALUES %s"

        # Add scraped_at timestamp for each row
        now = datetime.now(timezone.utc)
        rows_with_ts = [tuple(row + [now]) for row in rows]

        try:
            conn = psycopg2.connect(dsn=pg_conn_str)
            with conn:
                with conn.cursor() as cur:
                    execute_values(cur, sql, rows_with_ts)
            print(f"Inserted {len(rows)} rows into {table}.")
        except Exception as e:
            print(f"An error occurred while inserting into Postgres: {e}")
        finally:
            if 'conn' in locals():
                conn.close()

    async def run(self):
        """Orchestrates the scraper's execution."""
        print(f"Running {self.scraper_name} scraper...")
        try:
            data = await self.get_data()
            self._save_to_postgres(data)
        except Exception as e:
            print(f"An error occurred while running the {self.scraper_name} scraper: {e}")
        finally:
            print(f"{self.scraper_name} scraper finished.")
