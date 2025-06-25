import os
import re
import json
import pandas as pd
from dateutil.utils import today

from utils.core import make_http_request


def get_request_parameters():
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


def extract_and_process_data(response, csv_filename):
    """Extracts JSON data from the response and saves it to a CSV file."""
    if response:
        match = re.search(r"PRELOADED_DATA\.SPECIALS_PRODUCTS_DATA\s*=\s*(\{.*?\});", response.text)
        if match:
            json_data_string = match.group(1)
            try:
                newest_items_data = json.loads(json_data_string)
                data = newest_items_data.get('data', []) # Use .get for safer access
                print(f"Found {len(data)} items")

                # Load data into pandas DataFrame
                df = pd.DataFrame(data)

                # Save DataFrame to CSV
                df.to_csv(f'./data/raw/{csv_filename}', index=False)
                print(f"Data saved to {csv_filename}")

            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
                print(f"Extracted string was: {json_data_string}")
            except KeyError:
                print("The key 'data' was not found in the JSON.")
        else:
            print("Could not find PRELOADED_DATA.SPECIALS_PRODUCTS_DATA in the response.")
    else:
        print("No response to process.")

def main():
    """Main function to orchestrate the script execution."""
    today_timestamp = today().strftime('%Y-%m-%d')
    csv_filename = f'blupax-{today_timestamp}.csv'

    url, headers, cookies = get_request_parameters()
    response = make_http_request(method="GET", url=url, headers=headers, cookies=cookies)
    extract_and_process_data(response, csv_filename)


if __name__ == "__main__":
    import dotenv
    dotenv.load_dotenv()

    main()
