import unittest
import runpy
from unittest.mock import patch, AsyncMock

from src.main import main


class TestMain(unittest.IsolatedAsyncioTestCase):
    """Test suite for the main coroutine in main.py."""

    @patch('src.main.asyncio.gather', new_callable=AsyncMock)
    @patch('src.main.ParmedScraper')
    @patch('src.main.BlupaxScraper')
    async def test_main_runs_scrapers_concurrently(
        self, mock_blupax_scraper, mock_parmed_scraper, mock_gather
    ):
        """
        Tests that the main function initializes scrapers and runs them
        concurrently using asyncio.gather.
        """
        # Arrange
        # Get the mock instances and their run() method's return value (the coroutine)
        mock_blupax_instance = mock_blupax_scraper.return_value
        blupax_coro = mock_blupax_instance.run.return_value

        mock_parmed_instance = mock_parmed_scraper.return_value
        parmed_coro = mock_parmed_instance.run.return_value

        # Act
        await main()

        # Assert
        # Verify scrapers were initialized
        mock_blupax_scraper.assert_called_once_with()
        mock_parmed_scraper.assert_called_once_with()

        # Verify run() was called on each instance
        mock_blupax_instance.run.assert_called_once_with()
        mock_parmed_instance.run.assert_called_once_with()

        # Verify asyncio.gather was awaited with the coroutines from the scrapers
        mock_gather.assert_awaited_once_with(blupax_coro, parmed_coro)


def test_main_entry_point():
    """
    Tests that the script entry point (`if __name__ == "__main__"`)
    calls asyncio.run with the main coroutine.
    """
    with patch('src.main.asyncio.run') as mock_asyncio_run, \
         patch('src.main.main') as mock_main:

        # Use runpy to execute the module's code in the `__main__` scope
        runpy.run_path('src/main.py', run_name='__main__')

        # Assert that our main async function was called,
        # and that asyncio.run was called with the resulting coroutine.
        mock_main.assert_called_once_with()
        mock_asyncio_run.assert_called_once_with(mock_main.return_value)