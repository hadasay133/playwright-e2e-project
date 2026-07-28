import asyncio

from pages.base_page import BasePage
from pages.cart_page import CartPage
from pages.login_page import LoginPage
from pages.product_page import ProductPage


class HomePage(BasePage):
    def __init__(self, page):
        super().__init__(page)

    async def click_on_url(self, href: str) -> None:
        link = self.page.locator("a", has_text=href).first
        await link.click()

    async def navigate_to_page(self, link_selector: str):
        await self.click_on_url(link_selector)

        routes = {
            "cart": lambda: CartPage(self.page),
            "Log in": lambda: LoginPage(self.page),
        }

        for key, page_class in routes.items():
            if key in link_selector:
                return page_class()

        raise ValueError(f"Unknown page route for selector: {link_selector}")

    async def click_category(self, category: str) -> None:
        # Locate and click the category link
        category_link = self.page.locator(f"div a:has-text('{category}')")
        await category_link.wait_for(state="visible")
        await self.page.wait_for_load_state("load")  # Wait for the DOM to fully load
        await category_link.click()

    async def _extract_matching_products(self, max_price: float, current_count: int, limit: int) -> list[str]:
        results = []
        cards = self.page.locator("div.card")
        await cards.first.wait_for(state="visible")

        cards_count = await cards.count()
        for i in range(cards_count):
            if current_count + len(results) >= limit:
                break

            card = cards.nth(i)

            await card.scroll_into_view_if_needed()

            price_text = await card.locator("h5").inner_text()
            clean_price = float(price_text.replace("$", "").replace(",", "").strip())

            if clean_price <= max_price:
                product_name = await card.locator("a.hrefch").inner_text()
                results.append(product_name.strip())

        return results

    async def _navigate_to_next_page(self) -> bool:
        next_button = self.page.locator("#next2")

        if not await next_button.is_visible():
            return False

        first_product_before = await self.page.locator("div.card").first.locator("a.hrefch").inner_text()
        await next_button.click()

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
        await self.click_category(query)
        await asyncio.sleep(10)
        results = []

        while len(results) < limit:
            page_results = await self._extract_matching_products(max_price, len(results), limit)
            results.extend(page_results)

            if len(results) >= limit:
                break

            has_next = await self._navigate_to_next_page()
            if not has_next:
                break

        return results

    async def add_items_to_cart(self, product_names: list[str]) -> None:
        for product_name in product_names:
            await self.page.goto("https://www.demoblaze.com/index.html")
            await asyncio.sleep(10)
            product_link = self.page.locator(
                "a.hrefch",
                has_text=product_name
            ).first

            await product_link.wait_for(state="visible")
            await product_link.scroll_into_view_if_needed()
            await product_link.click()
            await asyncio.sleep(10)

            product_page = ProductPage(self.page)
            await product_page.add_product_to_cart(product_name)

