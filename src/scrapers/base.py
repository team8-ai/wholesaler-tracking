import os
import io
import abc
import json
import base64

import pandas as pd
from dateutil.utils import today
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload


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

    def _save_to_csv(self, data: list[dict]):
        """Saves the provided data to a file in Google Drive."""
        if not data:
            print(f"No data found for {self.scraper_name}.")
            return

        print(f"Found {len(data)} items for {self.scraper_name}.")
        df = pd.DataFrame(data)

        creds_base64 = os.environ.get('GOOGLE_CREDENTIALS_BASE64')
        folder_id = os.environ.get('GOOGLE_DRIVE_FOLDER_ID')

        if not creds_base64 or not folder_id:
            print("Skipping Google Drive upload: Credentials or folder ID not configured.")
            return

        try:
            creds_json_str = base64.b64decode(creds_base64).decode('utf-8')
            creds_info = json.loads(creds_json_str)
            credentials = Credentials.from_service_account_info(
                creds_info, scopes=["https://www.googleapis.com/auth/drive.file"]
            )
            service = build('drive', 'v3', credentials=credentials)

            csv_buffer = io.BytesIO()
            df.to_csv(csv_buffer, index=False)
            csv_buffer.seek(0)

            file_metadata = {'name': self.csv_filename, 'parents': [folder_id]}
            media = MediaIoBaseUpload(
                csv_buffer, mimetype='text/csv', resumable=True
            )
            
            print(f"Uploading {self.csv_filename} to Google Drive...")
            service.files().create(
                body=file_metadata, media_body=media, fields='id'
            ).execute()
            print(f"Successfully uploaded {self.csv_filename} to Google Drive.")

        except Exception as e:
            print(f"An error occurred while uploading to Google Drive: {e}")


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