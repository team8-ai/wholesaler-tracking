import os
import dotenv
import asyncio
from langchain_openai import ChatOpenAI
from browser_use import Agent, BrowserSession
from playwright.async_api import async_playwright, BrowserContext

from .core import setup_proxy

dotenv.load_dotenv()

llm = ChatOpenAI(model="gpt-4.1", temperature=0.0)

captured_token = None
token_found = False

async def handle_request(route, browser_context: BrowserContext | None):
    global captured_token
    global token_found
    request = route.request
    if "https://api.cardinalhealth.com/" in request.url:
        headers = await request.all_headers()
        if "access-token" in headers and not token_found:
            captured_token = headers["access-token"]
            token_found = True
            print(f"Access Token captured (access-token): {captured_token}")
            if browser_context:
                await browser_context.close()
            return
        print(f"Token not found in header.")
    await route.continue_()


def get_proxy_settings():
    proxies = setup_proxy()
    launch_options = {}
    proxy_string = proxies["http"]
    address_part = proxy_string[len("http://"):]
    server_address = address_part.split('@', 1)[-1]
    proxy_dict = {"server": server_address}
    proxy_dict["username"] = proxies['username']
    proxy_dict["password"] = proxies['password']
    launch_options['proxy'] = proxy_dict
    return launch_options


async def get_parmed_token():
    global captured_token
    async with async_playwright() as p:
        launch_options = get_proxy_settings()

        if launch_options is None:
            return None # Stop execution if proxy settings are not available

        browser_session_instance = BrowserSession(
            playwright=p,
            headless=True,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
            launch_options=launch_options
        )

        await browser_session_instance.start()

        page = await browser_session_instance.get_current_page()

        if not page:
            print("ERROR: Could not get current page from browser_session after start().")
            await browser_session_instance.stop() # Ensure browser is closed
            return None

        # Use the page object to set up route handling
        await page.route("https://api.cardinalhealth.com/**", lambda route: handle_request(route, page.context))

        print(f"Navigating to https://www.parmed.com/home using page from BrowserSession...")
        await page.goto(
            'https://www.parmed.com/home',
            # wait_until='domcontentloaded'
        )

        agent = Agent(
            browser_session=browser_session_instance,
            task=f"You are on the Parmed website. Login to the website via the 'Sign In' button on the top right of the page. Use the username {os.getenv('PARMED_USERNAME')} and the password {os.getenv('PARMED_PASSWORD')}. If you are already loggend in to the website - do nothing.",
            llm=llm,
            use_vision=False,
            enable_memory=False
        )

        print("Running agent to log in...")
        await agent.run()
        print("Agent finished.")

        # Ensure the browser session is stopped after the task is complete
        await browser_session_instance.stop()

        print(f"Final captured token: {captured_token}")
        return captured_token


if __name__ == "__main__":
    asyncio.run(get_parmed_token())
