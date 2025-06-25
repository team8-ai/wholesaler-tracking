import os
import re
import json
import asyncio

from utils.core import make_http_request
from .base import BaseScraper


class BlupaxScraper(BaseScraper):
    def __init__(self):
        super().__init__('blupax')

    def _get_request_parameters(self):
        """Defines and returns the URL, headers, and cookies for the HTTP request."""
        base_url = "https://www.blupaxpharma.com/specials"

        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
            'Referer': 'https://www.blupaxpharma.com/portal_home'
        }

        # Cookies from cURL command
        cookie_string = f"""_ga=GA1.1.379245868.1746610826; frontend_lang=en_US; tz=Asia/Jerusalem; im_livechat_session={{"folded":false,"id":467,"message_unread_counter":0,"operator_pid":[37685,"Nate  Baker",false],"name":"Chat with Nate  Baker","uuid":"x8UNRxURud"}}; im_livechat_auto_popup=false; im_livechat_previous_operator_pid=37685; session_id={os.getenv('BLUPAX_SESSION_ID')}; *ga*KSNYCY0H2M=GS2.1.s1747983040$o3$g1$t1747987489$j0$l0$h0"""
        cookies = {}
        for cookie_pair in cookie_string.split('; '):
            if '=' in cookie_pair: # ensure there is a key-value pair
                name, value = cookie_pair.split('=', 1)
                cookies[name] = value

        return base_url, headers, cookies

    async def get_data(self) -> list[dict]:
        """Extracts JSON data from the response and returns it as a list of dictionaries."""
        url, headers, cookies = self._get_request_parameters()
        response = make_http_request(method="GET", url=url, headers=headers, cookies=cookies)

        if not response:
            print("No response from Blupax.")
            return []

        match = re.search(r"PRELOADED_DATA\.SPECIALS_PRODUCTS_DATA\s*=\s*(\{.*?\});", response.text)
        if not match:
            print("Could not find PRELOADED_DATA.SPECIALS_PRODUCTS_DATA in the response.")
            return []

        json_data_string = match.group(1)
        try:
            newest_items_data = json.loads(json_data_string)
            return newest_items_data.get('data', [])
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            print(f"Extracted string was: {json_data_string}")
            return []
        except KeyError:
            print("The key 'data' was not found in the JSON.")
            return []


async def main():
    """Main function to orchestrate the script execution."""
    scraper = BlupaxScraper()
    await scraper.run()


if __name__ == "__main__":
    import dotenv
    dotenv.load_dotenv()

    asyncio.run(main())
