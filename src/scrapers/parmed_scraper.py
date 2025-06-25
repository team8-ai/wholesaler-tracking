import json
import asyncio

from ..utils.core import make_http_request
from ..utils.browser import get_parmed_token
from .base import BaseScraper


class ParmedScraper(BaseScraper):
    def __init__(self):
        super().__init__('parmed')

    def _get_request_parameters(self, access_token):
        """Defines and returns the URL, headers, and data payload for the API request."""
        url = 'https://api.cardinalhealth.com/pharmacon/product/kinray/external/v1/product'

        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9',
            'access-token': access_token,
            'agent-type': 'Desktop, Mac, Chrome 136.0.0.0',
            'content-type': 'application/json',
            'origin': 'https://www.parmed.com',
            'priority': 'u=1, i',
            'referer': 'https://www.parmed.com/',
            'sec-ch-ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
            'x-api-key': 't6qj1ODohFa5IQXazo8DcRudG8yN3pMF',
        }

        data = {
            "pageSize": 10,
            "searchKeyword": "",
            "shipToNum": "2057158677",
            "soldToNum": "2057158677",
            "userDetailNum": 53981,
            "pageNo": 0,
            "facets": {
                "manufacturer": [],
                "strength": [],
                "form": [],
                "labelsize": []
            },
            "sortOrder": None,
            "sortParam": None
        }

        return url, headers, data

    async def get_data(self) -> list[dict]:
        """Fetches and returns data from the ParMed API."""
        access_token = await get_parmed_token()
        url, headers, data = self._get_request_parameters(access_token)
        response = make_http_request(method="POST", url=url, headers=headers, data=data)

        if not response:
            print("No response from ParMed.")
            return []

        try:
            json_response = response.json()
            return json_response.get('itemList', [])
        except json.JSONDecodeError:
            print("Response content (not JSON):", response.text)
            return []


async def main():
    """Main function to orchestrate the script execution."""
    scraper = ParmedScraper()
    await scraper.run()


if __name__ == "__main__":
    import dotenv
    dotenv.load_dotenv()

    asyncio.run(main())
