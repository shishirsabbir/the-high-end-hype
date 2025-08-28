import re


async def parseProduct(page):
    # Helper to close feedback popup if present
    type_ = "men"
    async def close_feedback_popup():
        popup_close = page.locator('button[aria-label="Close dialog"]')
        if await popup_close.is_visible():
            await popup_close.click()

    # Try parsing, retry once if popup appears
    for attempt in range(2):
        try:
            await close_feedback_popup()
            # Title
            t = await page.locator('h1[data-element="Heading"]').text_content()
            if t:
                title = t.strip()
            # Brand
            b = await page.locator(
                'div[data-element="Skeleton"] > div[data-element="VStack"] > a'
            ).text_content()
            if b:
                brand = b.strip()
            # Colors & Images (robust extraction)
            color_imgs = page.locator(
                'div[data-element="Flex"] div[data-selector^="pdp-group-color-"] > picture > img'
            )
            count = await color_imgs.count()
            color_image_pairs = []
            for i in range(count):
                img = color_imgs.nth(i)
                alt = await img.get_attribute("alt")
                src = await img.get_attribute("src")
                if alt and src and src.startswith("http"):
                    color_image_pairs.append((alt, src))
            colors = [pair[0] for pair in color_image_pairs]
            images = [pair[1] for pair in color_image_pairs]
            # Sizes
            sizes = [
                s
                for s in await page.locator(
                    'div[data-element="Flex"] div[data-selector^="pdp-group-size-"]'
                ).all_text_contents()
                if s
            ]
            # Width
            width = [
                w
                for w in await page.locator(
                    'div[data-element="Flex"] div[data-selector^="pdp-group-width-"]'
                ).all_text_contents()
                if w
            ]
            # Price
            try:
                price_text = await page.locator("div.css-xnrxd4 h2").text_content()
                if price_text:
                    price_match = re.search(r"[\d,.]+", price_text)
                    if price_match:
                        price = float(price_match.group(0).replace(",", ""))
            except Exception:
                pass
            # Product Detail (description and highlights)
            d = await page.locator(
                'div[data-element="AccordionItem"] div.chakra-collapse > div[role="region"] > div.css-0'
            ).text_content()
            if d:
                description = d.strip()
            highlights = [
                h
                for h in await page.locator(
                    'div[data-element="AccordionItem"] div.chakra-collapse > div[role="region"] > ul.css-pxlwga > li'
                ).all_text_contents()
                if h
            ]
            # Category and Sub-category
            try:
                c = await page.locator(
                    'nav[aria-label="breadcrumb"] > ol > li:nth-child(2) > a'
                ).text_content(timeout=5000)
                if c:
                    category = c.strip()
            except Exception:
                category = ""
            try:
                sc = await page.locator(
                    'nav[aria-label="breadcrumb"] > ol > li:nth-child(3) > a'
                ).text_content(timeout=5000)
                if sc:
                    sub_category = sc.strip()
            except Exception:
                sub_category = ""
            # If parsing succeeded, return product
            product = {
                "title": title,
                "brand": brand,
                "colors": colors,
                "sizes": sizes,
                "width": width,
                "price": price,
                "images": images,
                "description": description,
                "highlights": highlights,
                "type": type_,
                "category": category,
                "sub_category": sub_category,
            }
            return product
        except Exception as e:
            await close_feedback_popup()
            if attempt == 1:
                print(f"Error during parsing: {e}")
                # Log missing fields for debugging
                missing = []
                if not title:
                    missing.append("title")
                if not brand:
                    missing.append("brand")
                if not colors:
                    missing.append("colors")
                if not sizes:
                    missing.append("sizes")
                if not width:
                    missing.append("width")
                if not price:
                    missing.append("price")
                if not images:
                    missing.append("images")
                if not description:
                    missing.append("description")
                if not highlights:
                    missing.append("highlights")
                if not type_:
                    missing.append("type")
                if not category:
                    missing.append("category")
                if not sub_category:
                    missing.append("sub_category")
                print(f"Missing fields: {missing}")

    # If both attempts fail, return default product dict
    product = {
        "title": title,
        "brand": brand,
        "colors": colors,
        "sizes": sizes,
        "width": width,
        "price": price,
        "images": images,
        "description": description,
        "highlights": highlights,
        "type": type_,
        "category": category,
        "sub_category": sub_category,
    }
    return product

async def parseProductTest(page):
    # Initialize all fields to safe defaults
    title = brand = description = category = sub_category = ""
    colors = sizes = width = images = highlights = []
    price = 0.0
    type_ = "men"

    # Helper to close feedback popup if present
    async def close_feedback_popup():
        popup_close = page.locator('button[aria-label="Close dialog"]')
        if await popup_close.is_visible():
            await popup_close.click()

    # Try parsing, retry once if popup appears
    for attempt in range(2):
        try:
            # Title
            t = await page.locator('h1[data-element="Heading"]').text_content()
            if t:
                title = t.strip()

            # Brand
            b = await page.locator(
                'div[data-element="Skeleton"] > div[data-element="VStack"] > a'
            ).text_content()
            if b:
                brand = b.strip()

            # Colors & Images (robust extraction)
            color_imgs = page.locator(
                'div[data-element="Flex"] div[data-selector^="pdp-group-color-"] > picture > img'
            )
            count = await color_imgs.count()
            color_image_pairs = []
            for i in range(count):
                img = color_imgs.nth(i)
                alt = await img.get_attribute("alt")
                src = await img.get_attribute("src")
                if alt and src and src.startswith("http"):
                    color_image_pairs.append((alt, src))
            colors = [pair[0] for pair in color_image_pairs]
            images = [pair[1] for pair in color_image_pairs]

            # Sizes
            sizes = [
                s
                for s in await page.locator(
                    'div[data-element="Flex"] div[data-selector^="pdp-group-size-"]'
                ).all_text_contents()
                if s
            ]

            # Width
            width = [
                w
                for w in await page.locator(
                    'div[data-element="Flex"] div[data-selector^="pdp-group-width-"]'
                ).all_text_contents()
                if w
            ]

            # Price (skip if any error)
            try:
                price_text = await page.locator("div.css-xnrxd4 h2").text_content()
                if price_text:
                    price_match = re.search(r"[\d,.]+", price_text)
                    if price_match:
                        price = float(price_match.group(0).replace(",", ""))
            except Exception:
                pass

            # Product Detail (description and highlights) - extract directly
            d = await page.locator(
                'div[data-element="AccordionItem"] div.chakra-collapse > div[role="region"] > div.css-0'
            ).text_content()
            if d:
                description = d.strip()
            highlights = [
                h
                for h in await page.locator(
                    'div[data-element="AccordionItem"] div.chakra-collapse > div[role="region"] > ul.css-pxlwga > li'
                ).all_text_contents()
                if h
            ]

            # Category and Sub-category (with timeout and fallback)
            try:
                c = await page.locator(
                    'nav[aria-label="breadcrumb"] > ol > li:nth-child(2) > a'
                ).text_content(timeout=5000)
                if c:
                    category = c.strip()
            except Exception:
                category = ""
            try:
                sc = await page.locator(
                    'nav[aria-label="breadcrumb"] > ol > li:nth-child(3) > a'
                ).text_content(timeout=5000)
                if sc:
                    sub_category = sc.strip()
            except Exception:
                sub_category = ""

            break  # Success, exit retry loop
        except Exception as e:
            await close_feedback_popup()
            if attempt == 1:
                print(f"Error during parsing: {e}")
                # Log missing fields for debugging
                missing = []
                if not title:
                    missing.append("title")
                if not brand:
                    missing.append("brand")
                if not colors:
                    missing.append("colors")
                if not sizes:
                    missing.append("sizes")
                if not width:
                    missing.append("width")
                if not price:
                    missing.append("price")
                if not images:
                    missing.append("images")
                if not description:
                    missing.append("description")
                if not highlights:
                    missing.append("highlights")
                if not type_:
                    missing.append("type")
                if not category:
                    missing.append("category")
                if not sub_category:
                    missing.append("sub_category")
                print(f"Missing fields: {missing}")

    # Build product dict with defaults for missing fields
    product = {
        "title": title,
        "brand": brand,
        "colors": colors,
        "sizes": sizes,
        "width": width,
        "price": price,
        "images": images,
        "description": description,
        "highlights": highlights,
        "type": type_,
        "category": category,
        "sub_category": sub_category,
    }

    return product
