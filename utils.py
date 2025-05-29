import os
import requests


def setup_proxy():
    """Sets up proxy configuration from environment variables."""
    username = os.getenv('OX_USERNAME')
    password = os.getenv('OX_PASSWORD')
    proxy_server_address = os.getenv('OX_PROXY_SERVER_ADDRESS')

    if proxy_server_address:
        proxy_string = f"http://{username}:{password}@{proxy_server_address.split('//', 1)[-1]}"
        proxies = {
            "http": proxy_string,
            "https": proxy_string,
            'username': username,
            'password': password
        }
        return proxies
    else:
        print("Warning: OX_PROXY_SERVER_ADDRESS environment variable not set. Proceeding without proxy.")
        return None

def make_http_request(method: str, url: str, headers: dict, cookies: dict = None, data: dict = None):
    """
    Makes an HTTP request (GET or POST) based on the specified method and returns the response.

    Parameters:
    - method (str): The HTTP method to use, either 'GET' or 'POST'.
    - url (str): The URL to send the request to.
    - headers (dict): The headers to include in the request.
    - cookies (dict, optional): The cookies to include in the request.
    - data (dict, optional): The data to send in the request body (for POST requests).
    - proxies (dict, optional): The proxy configuration to use for the request.
    """
    """Makes an HTTP request (GET or POST) based on the specified method and returns the response."""
    proxies = setup_proxy()

    try:
        response = requests.request(
            method.upper(),
            url,
            headers=headers,
            cookies=cookies,
            json=data if method.upper() == "POST" else None,
            proxies=proxies
        )

        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        print("Request successful!")
        print("Response status code:", response.status_code)
        return response
    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the HTTP request: {e}")
        return None
    except ValueError as ve:
        print(ve)
        return None
