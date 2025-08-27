# imports
import httpx
import asyncio
from typing import Callable, Awaitable

# target url
target_url = "https://www.shoecarnival.com/womens"

# http header
custom_header = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"
}


# async client (for session)
client: httpx.AsyncClient = httpx.AsyncClient(headers=custom_header)


# request async function
async def getResponse(url, client: httpx.AsyncClient):
    try:
        response = await client.get(url)
        print(response.status_code)
    except Exception as e:
        print(f"Error! {e}")
    finally:
        await client.aclose()


# the main crawl function
async def runSpider(callback: Callable[[str, httpx.AsyncClient], Awaitable[None]]):
    await callback(target_url, client)


# running the script
if __name__ == "__main__":
    asyncio.run(runSpider(getResponse))
