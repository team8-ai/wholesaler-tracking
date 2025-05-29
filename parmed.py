import os
import json
import pandas as pd
from dateutil.utils import today

from utils import make_http_request


def get_request_parameters():
    """Defines and returns the URL, headers, and data payload for the API request."""
    url = 'https://api.cardinalhealth.com/pharmacon/product/kinray/external/v1/product'

    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'access-token': os.getenv('PARMED_ACCESS_TOKEN'),
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

def process_response_and_save(response, csv_filename):
    """Processes the API response and saves the item list to a CSV file."""
    if response:
        try:
            json_response = response.json()
            item_list = json_response.get('itemList', []) # Use .get for safer access
            print(f"Found {len(item_list)} items under 'itemList'.")
            df = pd.DataFrame(item_list)

            df.to_csv(f'./data/{csv_filename}', index=False)
            print(f"Data saved to {csv_filename}")

        except json.JSONDecodeError:
            print("Response content (not JSON):", response.text)
    else:
        print("No response to process.")

def main():
    """Main function to orchestrate the script execution."""
    today_timestamp = today().strftime('%Y-%m-%d')
    csv_filename = f'parmed-{today_timestamp}.csv'

    url, headers, data = get_request_parameters()
    response = make_http_request(method="POST", url=url, headers=headers, data=data)
    process_response_and_save(response, csv_filename)


if __name__ == "__main__":
    import dotenv
    dotenv.load_dotenv()

    main()
