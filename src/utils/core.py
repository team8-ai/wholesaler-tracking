import os
import requests
from typing import Optional


def setup_proxy(validate_proxy: bool = True, browser_format: bool = False):
    """
    Sets up proxy configuration from environment variables.
    
    Args:
        validate_proxy: Whether to validate the proxy connection
        browser_format: If True, returns format suitable for browser/Playwright launch options
    
    Returns:
        For HTTP requests (browser_format=False): {"proxies": {...}, "auth": None}
        For browser usage (browser_format=True): {"proxy": {...}} or None on error
    """
    username: str | None = os.environ.get('OX_USERNAME')
    password: str | None = os.environ.get('OX_PASSWORD')
    proxy_server_address: str | None = os.environ.get('OX_PROXY_SERVER_ADDRESS')

    if proxy_server_address and username and password:
        # Clean the proxy server address and setup embedded credentials
        clean_proxy_address = proxy_server_address.split('//', 1)[-1]
        proxy_url_with_auth = f"http://{username}:{password}@{clean_proxy_address}"
        proxies = {
            "http": proxy_url_with_auth,
            "https": proxy_url_with_auth,
        }
        
        # For browser format, convert to Playwright-compatible format
        if browser_format:
            try:
                proxy_dict = {
                    "server": f"http://{clean_proxy_address}",
                    "username": username,
                    "password": password
                }
                return {"proxy": proxy_dict}
            except Exception as e:
                print(f"Error setting up proxy for browser: {e}")
                return None
        
        # For HTTP requests format
        if not validate_proxy:
            return {"proxies": proxies, "auth": None}
        
        # Validate proxy by testing connection to example.com
        try:
            print("Validating proxy configuration...")
            test_response = requests.get(
                "http://example.com", 
                proxies=proxies,
                timeout=10
            )
            test_response.raise_for_status()
            print("Proxy validation successful!")
            return {"proxies": proxies, "auth": None}
        except requests.exceptions.RequestException as e:
            print(f"Proxy validation failed: {e}")
            print("⚠️  Returning proxy config anyway - it might still work for actual requests.")
            return {"proxies": proxies, "auth": None}
        
    else:
        raise ValueError("OX_PROXY_SERVER_ADDRESS, OX_USERNAME, and OX_PASSWORD environment variables must be set.")


def make_http_request(method: str, url: str, headers: dict, cookies: Optional[dict] = None, data: Optional[dict] = None):
    """
    Makes an HTTP request (GET or POST) based on the specified method and returns the response.

    Parameters:
    - method (str): The HTTP method to use, either 'GET' or 'POST'.
    - url (str): The URL to send the request to.
    - headers (dict): The headers to include in the request.
    - cookies (dict, optional): The cookies to include in the request.
    - data (dict, optional): The data to send in the request body (for POST requests).
    """
    # Skip validation for actual requests to improve performance
    proxy_config = setup_proxy(validate_proxy=False)

    try:
        response = requests.request(
            method.upper(),
            url,
            headers=headers,
            cookies=cookies,
            json=data if method.upper() == "POST" else None,
            proxies=proxy_config["proxies"]
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


if __name__ == "__main__":
    print("Testing proxy setup...")
    proxy_config = setup_proxy(validate_proxy=True)
    print("Proxy setup completed!")
