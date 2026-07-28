import asyncio

from pages.base_page import BasePage
from pages.cart_page import CartPage
from pages.login_page import LoginPage
from pages.product_page import ProductPage


class HomePage(BasePage):
    def __init__(self, page):
        # Initialize the HomePage with the Playwright page object
        super().__init__(page)

    async def click_on_url(self, href: str) -> None:
        # Locate the first link element with the specified text and click it
        link = self.page.locator("a", has_text=href).first
        await link.click()

    async def navigate_to_page(self, link_selector: str):
        # Navigate to a specific page based on the link selector
        await self.click_on_url(link_selector)

        # Define routes for navigation and return the corresponding page object
        routes = {
            "cart": lambda: CartPage(self.page),
            "Log in": lambda: LoginPage(self.page),
        }

        for key, page_class in routes.items():
            if key in link_selector:
                return page_class()

        # Raise an error if the route is unknown
        raise ValueError(f"Unknown page route for selector: {link_selector}")

    async def click_category(self, category: str) -> None:
        # Locate and click the category link
        category_link = self.page.locator(f"div a:has-text('{category}')")
        await category_link.wait_for(state="visible")  # Wait until the category link is visible
        await self.page.wait_for_load_state("load")  # Wait for the DOM to fully load
        await category_link.click()  # Click the category link

    async def _extract_matching_products(self, max_price: float, current_count: int, limit: int) -> list[str]:
        # Extract product names that match the price criteria
        results = []
        cards = self.page.locator("div.card")  # Locate all product cards
        await cards.first.wait_for(state="visible")  # Wait for the first card to be visible

        cards_count = await cards.count()  # Get the total number of product cards
        for i in range(cards_count):
            if current_count + len(results) >= limit:
                break  # Stop if the limit is reached

            card = cards.nth(i)  # Get the nth product card

            await card.scroll_into_view_if_needed()  # Scroll to the product card if needed

            price_text = await card.locator("h5").inner_text()  # Get the price text
            clean_price = float(price_text.replace("$", "").replace(",", "").strip())  # Clean and convert the price

            if clean_price <= max_price:
                # If the price is within the limit, get the product name
                product_name = await card.locator("a.hrefch").inner_text()
                results.append(product_name.strip())  # Add the product name to the results

        return results

    async def _navigate_to_next_page(self) -> bool:
        # Navigate to the next page of products
        next_button = self.page.locator("#next2")  # Locate the "Next" button

        if not await next_button.is_visible():
            return False  # Return False if the "Next" button is not visible

        # Get the name of the first product before navigating
        first_product_before = await self.page.locator("div.card").first.locator("a.hrefch").inner_text()
        await next_button.click()  # Click the "Next" button

        # Wait until the first product on the next page is different
        await self.page.wait_for_function(
            """([selector, old_text]) => {
                const el = document.querySelector(selector);
                return el && el.innerText !== old_text;
            }""",
            arg=["div.card a.hrefch", first_product_before],
            timeout=5000,
        )
        return True

    async def search_items_by_name_under_price(self, query: str, max_price: float, limit: int) -> list[str]:
        # Search for items by name under a specified price
        await self.click_category(query)  # Click the category link
        await asyncio.sleep(10)  # Wait for the page to load
        results = []

        while len(results) < limit:
            # Extract matching products on the current page
            page_results = await self._extract_matching_products(max_price, len(results), limit)
            results.extend(page_results)  # Add the results to the list

            if len(results) >= limit:
                break  # Stop if the limit is reached

            has_next = await self._navigate_to_next_page()  # Navigate to the next page
            if not has_next:
                break  # Stop if there are no more pages

        return results

    async def add_items_to_cart(self, product_names: list[str]) -> None:
        # Add specified items to the cart
        for product_name in product_names:
            await self.page.goto("https://www.demoblaze.com/index.html")  # Navigate to the homepage
            await asyncio.sleep(10)  # Wait for the page to load
            product_link = self.page.locator(
                "a.hrefch",
                has_text=product_name
            ).first  # Locate the product link

            await product_link.wait_for(state="visible")  # Wait until the product link is visible
            await product_link.scroll_into_view_if_needed()  # Scroll to the product link if needed
            await product_link.click()  # Click the product link
            await asyncio.sleep(10)  # Wait for the product page to load

            product_page = ProductPage(self.page)  # Create a ProductPage object
            await product_page.add_product_to_cart(product_name)  # Add the product to the cart
