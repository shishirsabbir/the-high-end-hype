### Selectors

```
title: h1[data-element="Heading"] (text)
brand: div[data-element="Skeleton"] > div[data-element="VStack"] > a (text)
colors: div[data-element="Flex"] div[data-selector^="pdp-group-color-"] > picture > img (href value and alt value (attributes))
sizes: div[data-element="Flex"] div[data-selector^="pdp-group-size-"] (text)
width: div[data-element="Flex"] div[data-selector^="pdp-group-width-"] (text)
price: div.css-xnrxd4 h2:not(h2[aria-label="Starting at"]) (text)
images: it will be the same as colors href value
description: check the note below
hightlights: check the note below
type: 'men'
category: nav[aria-label="breadcrumb"] > ol > li:nth-child(2) > a (text)
sub_category: nav[aria-label="breadcrumb"] > ol > li:nth-child(3) > a (text)
```


#### Note
> Product description scraping

```python
# Store the button locator
button = page.locator("button:has-text('Product Detail')")

# Click the button
await button.click()

# Get the parent region of the button
description_tag = button.locator("xpath=ancestor::div[@role='region']")

# Get the description inside that region
description = await description_tag.locator("div.css-0").text_content()

# for the highlights
# Get the parent region of the button
hightlight_tags = button.locator("xpath=ancestor::div[@role='region']")

# Get the description
description = await region.locator("div.css-0").text_content()

# Get the product highlights as a list
highlights = await region.locator("ul.css-pxlwga > li").all_text_contents()
```