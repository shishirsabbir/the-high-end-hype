import asyncio
import os
import json
from playwright.async_api import async_playwright
from library.parser import parseProduct
from database.database import SessionLocal
from database.model import Shoe

DATA_PATH = "data/browser_state.json"
URLS_PATH = "output/men_shoes.json"


def load_urls(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [item["url"] for item in data]


# Save product to database using SQLAlchemy


async def save_product(product_data):
    def db_task():
        session = SessionLocal()
        try:
            shoe = Shoe(**product_data)
            session.add(shoe)
            session.commit()
            print(f"[DB LOG] New entry stored: {shoe.title} | ID: {shoe.id}")
        except Exception as e:
            session.rollback()
            print(f"Error saving product: {e}")
        finally:
            session.close()

    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, db_task)


async def main():
    # Check for browser state
    if not os.path.exists(DATA_PATH):
        from library.initialize import store_browser_state
        await store_browser_state()
    urls = load_urls(URLS_PATH)
    total_urls = len(urls)
    print(f"🟢 Loaded {total_urls} URLs to scrape.")


    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(
            storage_state=DATA_PATH,
            viewport={"width": 1920, "height": 1080},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            locale="en-US",
            color_scheme="light",
            geolocation={"latitude": 0, "longitude": 0},
            permissions=[],
        )
        await context.grant_permissions([], origin="https://www.shoecarnival.com/")
        page = await context.new_page()

        print("� Starting scraping...")
        error_urls = []
        bar_length = 30
        for idx, url in enumerate(urls[:5], 1):
            progress = int(bar_length * idx / total_urls)
            bar = "█" * progress + "-" * (bar_length - progress)
            print(f"🟦 [{idx}/{total_urls}] |{bar}| Scraping: {url}")
            try:
                await page.goto(url)
                product_data = await parseProduct(page)
                missing = [
                    k
                    for k, v in product_data.items()
                    if v is None
                    or (isinstance(v, list) and not v)
                    or (isinstance(v, str) and not v)
                ]
                if missing:
                    print(f"⚠️ Missing data for {url}: {missing}")
                    error_urls.append({"url": url, "missing": missing})
                else:
                    print(f"✅ Data parsed for: {url}")
                await save_product(product_data)
            except Exception as e:
                print(f"❌ Error during scraping for {url}: {e}")
                error_urls.append({"url": url, "error": str(e)})
            await page.wait_for_timeout(0.5 * 1000)  # 0.5 seconds for faster iteration

        # Export error URLs to output/error_urls_men.json
        if error_urls:
            os.makedirs("output", exist_ok=True)
            with open("output/error_urls_men.json", "w", encoding="utf-8") as f:
                json.dump(error_urls, f, ensure_ascii=False, indent=2)
            print(
                f"📦 Exported {len(error_urls)} error URLs to output/error_urls_men.json"
            )
        print("🎉 Scraping complete!")

    # ...existing code...


if __name__ == "__main__":
    asyncio.run(main())
