from playwright.async_api import async_playwright
import random


async def store_browser_state():
    url = "https://www.shoecarnival.com/"
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False
        )  # Use headful mode to mimic real user
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={
                "width": 1920,
                "height": 1080,
            },
            locale="en-US",
            color_scheme="light",
            geolocation={"latitude": 0, "longitude": 0},  # Dummy location
            permissions=[],  # Block all permissions, including geolocation
        )
        # Explicitly deny geolocation for the site
        await context.grant_permissions([], origin=url)
        page = await context.new_page()
        await page.goto(url)
        # Simulate human-like delay and interaction
        await page.wait_for_timeout(random.randint(2000, 4000))
        await page.mouse.move(random.randint(100, 500), random.randint(100, 500))
        await page.wait_for_timeout(random.randint(1000, 2000))

        # --- Begin codegen actions (converted from TypeScript to Python) ---
        try:
            # Only click cookie popup if visible
            cookie_button = await page.query_selector(
                "button:has-text('Accept All Cookies')"
            )
            if cookie_button:
                await cookie_button.click()
                await page.wait_for_timeout(random.randint(500, 1500))

            # --- New codegen actions (desktop selectors) ---
            await page.wait_for_timeout(random.randint(500, 1500))
            await page.get_by_role("button", name="Mens", exact=True).click()
            await page.wait_for_timeout(random.randint(500, 1500))
            await page.get_by_role("button", name="2", exact=True).click()
            await page.wait_for_timeout(random.randint(500, 1500))
            # Close dialog only if it appears
            dialog_close = await page.query_selector("button:has-text('Close dialog')")
            if dialog_close:
                await dialog_close.click()
                await page.wait_for_timeout(random.randint(500, 1500))
            await page.get_by_role("button", name="Womens").click()
            await page.wait_for_timeout(random.randint(500, 1500))
            # Click the second matching link for Women's Adidas VL Court 3.0
            links = await page.locator(
                "a[role='link']", has_text="Women's Adidas VL Court 3.0"
            ).all()
            if len(links) > 1:
                await links[1].click()
            elif links:
                await links[0].click()
            await page.wait_for_timeout(random.randint(500, 1500))
            # Wait for 'Product Detail' button and click only if present
            try:
                await page.wait_for_selector(
                    "button:has-text('Product Detail')", timeout=10000
                )
                product_detail_btn = await page.query_selector(
                    "button:has-text('Product Detail')"
                )
                if product_detail_btn:
                    await product_detail_btn.click()
                    await page.wait_for_timeout(random.randint(500, 1500))
            except Exception:
                print("'Product Detail' button not found or not clickable.")
        except Exception as e:
            print(f"Some actions failed: {e}")
        # --- End codegen actions ---

        # Save browser state
        await context.storage_state(path="data/browser_state.json")
        await browser.close()
